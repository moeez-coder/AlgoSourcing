"""Combine every vertical's listbuild run into ONE deduplicated ALGO universe, with checks and a report.

Standalone (no AlgoSourcing repo needed). Run from the bundle's workspace/ folder after the listbuild runs:
    python ../algo_universe.py --out ../universe_output
Reads  config/u_*.yaml and out/<name>/ledger.sqlite for every config that has been run,
       seeds/contacted_all.csv (everyone already contacted) and dnc_clients.csv (Algo clients, never contacted).
Writes <out>/algo-universe_partNN.csv.gz (main list, <= 250k rows each), <out>/algo-universe_review.csv.gz
       (keyword-gated candidates + unverified industry; review before use) and <out>/REPORT.md.
"""
import argparse, csv, glob, gzip, json, os, sqlite3, sys, collections
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "listbuild"))
import yaml  # noqa: E402
from listbuild.identity import normalize_linkedin_url as nli, normalize_company_linkedin_url as nco, normalize_domain  # noqa: E402
from listbuild.seniority import classify_title  # noqa: E402

ORDER = ["u_v1_staffing_recruitment", "u_v2_marketing", "u_v3_ma_advisory", "u_v4_b2b_saas", "u_v1b_boutique_exec_search",
         "u_v5_it_services", "u_v6_life_sciences_services", "u_v7_nearshore_dev", "u_v8_fractional_consulting", "u_v9_peo_eor_hr_tech"]
PLACEHOLDER_EMPLOYERS = {"private company", "confidential", "confidential company", "stealth", "stealth mode", "stealth startup",
                         "stealth mode startup", "self-employed", "self employed", "freelance", "freelancer", "independent",
                         "independent consultant", "n/a", "na", "none", "-", "self-employed contractor", "undisclosed",
                         "undisclosed company", "family office", "private investor", "retired"}
COLS = ["linkedin_url", "first_name", "last_name", "full_name", "job_title", "seniority", "company_name", "company_domain",
        "company_linkedin_url", "industry", "person_country", "company_country", "vertical", "all_verticals", "icp_fit", "fit_reason"]
PART = 250_000
csv.field_size_limit(10**8)


def load_dnc(path):
    doms, urls = set(), set()
    if path.exists():
        for r in csv.DictReader(open(path, encoding="utf-8-sig", newline="")):
            for d in (r.get("domains") or "").split(";"):
                d = normalize_domain(d)
                if d: doms.add(d)
            u = nco(r.get("company_linkedin_url"))
            if u: urls.add(u)
    return doms, urls


def load_contacted(path):
    s = set()
    for r in csv.DictReader(open(path, encoding="utf-8-sig", newline="")):
        u = nli(r.get("linkedin_url"))
        if u: s.add(u)
    return s


def write_parts(rows, out, stem):
    files = []
    for i in range(0, max(len(rows), 1), PART):
        chunk = rows[i:i + PART]
        if not chunk: break
        name = f"{stem}_part{i // PART + 1:02d}.csv.gz" if len(rows) > PART else f"{stem}.csv.gz"
        with gzip.open(out / name, "wt", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore"); w.writeheader(); w.writerows(chunk)
        files.append(name)
    return files


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", required=True)
    p.add_argument("--workspace", default=".")
    a = p.parse_args(argv)
    ws, out = Path(a.workspace).resolve(), Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    contacted = load_contacted(ws / "seeds" / "contacted_all.csv")
    dnc_d, dnc_u = load_dnc(ws / "dnc_clients.csv")
    allowed = {}
    main, review = {}, {}
    stats = collections.OrderedDict()
    for name in ORDER:
        cfg_path, db = ws / "config" / f"{name}.yaml", ws / "out" / name / "ledger.sqlite"
        if not cfg_path.exists() or not db.exists():
            continue
        cfg = yaml.safe_load(open(cfg_path))
        allowed[name] = (set(cfg["company_hq_countries"]), set(cfg["person_countries"]))
        con = sqlite3.connect(db); con.row_factory = sqlite3.Row
        st = collections.Counter()
        for r in con.execute("SELECT * FROM contacts"):
            r = dict(r); st["total_in_ledger"] += 1
            u = nli(r.get("linkedin_url"))
            if not u: st["no_linkedin"] += 1; continue
            if classify_title(r.get("job_title")) == "fail": st["title_guard_fail"] += 1; continue
            if u in contacted: st["already_contacted"] += 1; continue
            if normalize_domain(r.get("company_domain")) in dnc_d or nco(r.get("company_linkedin_url")) in dnc_u:
                st["algo_client"] += 1; continue
            if (r.get("company_name") or "").strip().lower() in PLACEHOLDER_EMPLOYERS: st["placeholder_employer"] += 1; continue
            fit = r.get("icp_fit")
            target = main if fit == "fit" else review if fit in ("candidate", "unknown") else None
            if target is None: st[f"held_back_{fit or 'unclassified'}"] += 1; continue
            st["main" if fit == "fit" else "review"] += 1
            r["linkedin_url"] = "https://www." + u
            if u in target:
                target[u]["all_verticals"] += ";" + name
            else:
                r["vertical"], r["all_verticals"] = name, name
                target[u] = r
        stats[name] = st
    for u in list(review):            # a person in any main list is not also a review row
        if u in main: del review[u]
    main_rows, review_rows = list(main.values()), list(review.values())
    # checks
    def countries_ok(r):
        hq, pc = allowed[r["vertical"]]
        return (not r.get("company_country") or r["company_country"] in hq) and (not r.get("person_country") or r["person_country"] in pc)
    checks = {
        "duplicate_urls_in_main": len(main_rows) - len({r["linkedin_url"] for r in main_rows}),
        "main_rows_in_contacted": sum(nli(r["linkedin_url"]) in contacted for r in main_rows),
        "main_rows_at_clients": sum(normalize_domain(r.get("company_domain")) in dnc_d for r in main_rows),
        "main_rows_title_fail": sum(classify_title(r.get("job_title")) == "fail" for r in main_rows),
        "main_rows_country_outside_allowed": sum(not countries_ok(r) for r in main_rows),
    }
    files = write_parts(main_rows, out, "algo-universe")
    rfiles = write_parts(review_rows, out, "algo-universe_review")
    by_v = collections.Counter(r["vertical"] for r in main_rows)
    by_c = collections.Counter(r.get("person_country") for r in main_rows)
    by_s = collections.Counter(r.get("seniority") for r in main_rows)
    top_co = collections.Counter(r.get("company_name") for r in main_rows).most_common(20)
    companies = len({r.get("company_domain") or r.get("company_linkedin_url") for r in main_rows})
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"# ALGO universe — combined report ({now})", "",
             f"- **Main list: {len(main_rows):,} people at {companies:,} companies** (target 1,500,000).",
             f"- Review file (keyword-gated candidates + unverified industry): {len(review_rows):,} people.",
             f"- Files: {', '.join(files)}; review: {', '.join(rfiles)}", "",
             "## Per vertical (before cross-vertical dedup)", "",
             "| Vertical | in ledger | main | review | title fail | already contacted | Algo client | placeholder | held back |",
             "|---|---|---|---|---|---|---|---|---|"]
    for n, st in stats.items():
        held = sum(v for k, v in st.items() if k.startswith("held_back"))
        lines.append(f"| {n} | {st['total_in_ledger']:,} | {st['main']:,} | {st['review']:,} | {st['title_guard_fail']:,} | "
                     f"{st['already_contacted']:,} | {st['algo_client']:,} | {st['placeholder_employer']:,} | {held:,} |")
    lines += ["", "## Main list by primary vertical (after dedup)", ""] + [f"- {k}: {v:,}" for k, v in by_v.most_common()]
    lines += ["", "## Person country (top 15)", ""] + [f"- {k}: {v:,}" for k, v in by_c.most_common(15)]
    lines += ["", "## Seniority", ""] + [f"- {k}: {v:,}" for k, v in by_s.most_common()]
    lines += ["", "## Top 20 companies by people (flag large enterprises)", ""] + [f"- {k}: {v:,}" for k, v in top_co]
    lines += ["", "## Checks (all must be 0)", ""] + [f"- {k}: {v}" for k, v in checks.items()]
    (out / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    if any(checks.values()):
        sys.exit("CHECK FAILED: see REPORT.md")


if __name__ == "__main__":
    main()
