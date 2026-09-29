"""Bridge between listbuild and the AlgoSourcing repo conventions (sourcing/pipeline.md).

    seeds   build the exclusion CSV from every vertical's contacted_ledger.csv (LinkedIn URL), enriched with
            first/last/domain from the per-run people CSVs so name+domain matching also works
    import  copy a finished listbuild run into sourcing/data/<vertical>/{people,companies,reports}/ using our
            file naming and column conventions, re-checking every row against the contacted ledgers

Run from the repo root:
    python .claude/skills/listbuild/scripts/algo_bridge.py seeds
    python .claude/skills/listbuild/scripts/algo_bridge.py import --vertical vertical-1-staffing-recruitment \
        --icp sourcing/listbuild/config/v1_staffing.yaml --label full-tam
"""
import argparse
import csv
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR))

import yaml  # noqa: E402

from listbuild.identity import normalize_domain, normalize_linkedin_url  # noqa: E402
from listbuild.seeds import detect_columns  # noqa: E402

csv.field_size_limit(10**8)

PEOPLE_COLS = ["first_name", "last_name", "full_name", "title", "company_name", "company_domain", "linkedin_url", "email",
               "seniority", "source", "company_linkedin_url", "industry", "person_country", "company_country",
               "title_check", "icp_fit", "fit_reason"]
COMPANY_COLS = ["company_name", "domain", "linkedin_url", "hq_city", "hq_country", "employee_count", "estimated_revenue",
                "industry", "signal(s)", "qualified", "notes"]


def repo_root():
    here = Path.cwd().resolve()
    for p in [here, *here.parents]:
        if (p / "sourcing" / "data").is_dir():
            return p
    sys.exit("run this from inside the AlgoSourcing repo (no sourcing/data/ found)")


def contacted_urls(root):
    """Normalised LinkedIn URLs of everyone ever pushed, across every vertical's ledger."""
    urls = {}
    for ledger in sorted((root / "sourcing" / "data").glob("*/contacted_ledger.csv")):
        with ledger.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                u = normalize_linkedin_url(row.get("linkedin_url"))
                if u:
                    urls.setdefault(u, {"full_name": row.get("full_name") or "", "vertical": ledger.parent.name})
    return urls


def cmd_seeds(args):
    root = repo_root()
    urls = contacted_urls(root)
    names = {}
    for people in sorted((root / "sourcing" / "data").glob("*/people/*.csv")):
        with people.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            cols = detect_columns(reader.fieldnames or [])
            if not cols["linkedin"]:
                continue
            for row in reader:
                u = normalize_linkedin_url(row.get(cols["linkedin"]))
                if u in urls and u not in names:
                    names[u] = (row.get(cols["first"]) or "", row.get(cols["last"]) or "",
                                normalize_domain(row.get(cols["domain"])) or "" if cols["domain"] else "")
    out = Path(args.out) if args.out else root / "sourcing" / "listbuild" / "seeds" / "contacted_all.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["linkedin_url", "first_name", "last_name", "company_domain", "full_name", "vertical"])
        for u, meta in sorted(urls.items()):
            first, last, dom = names.get(u, ("", "", ""))
            w.writerow(["https://www." + u, first, last, dom, meta["full_name"], meta["vertical"]])
    print(f"wrote {out}: {len(urls):,} contacted people ({len(names):,} with name+domain for the second match key)")


def cmd_import(args):
    root = repo_root()
    icp = yaml.safe_load(Path(args.icp).read_text(encoding="utf-8"))
    run_dir = root / "sourcing" / "listbuild" / "out" / icp["name"]
    db = run_dir / "ledger.sqlite"
    if not db.exists():
        sys.exit(f"no listbuild ledger at {db}; run listbuild first")
    vdir = root / "sourcing" / "data" / args.vertical
    if not (vdir / "contacted_ledger.csv").exists():
        sys.exit(f"{vdir} is not a vertical data folder (no contacted_ledger.csv)")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    base = f"{stamp}_listbuild-{args.label}"
    contacted = contacted_urls(root)

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    where = "title_check != 'fail'"
    buckets = {"fit": "", "candidate": "_candidates", "unknown": "_unverified"}
    (vdir / "people").mkdir(exist_ok=True)
    summary = {}
    for fit, suffix in buckets.items():
        path = vdir / "people" / f"{base}{suffix}.csv"
        n = dropped = 0
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=PEOPLE_COLS, extrasaction="ignore")
            w.writeheader()
            for r in conn.execute(f"SELECT * FROM contacts WHERE {where} AND icp_fit = ? ORDER BY key", (fit,)):
                r = dict(r)
                if normalize_linkedin_url(r.get("linkedin_url")) in contacted:
                    dropped += 1
                    continue
                r["title"], r["source"], r["email"] = r.get("job_title"), r.get("all_sources"), ""
                w.writerow(r)
                n += 1
        if n == 0:
            path.unlink()
        summary[fit] = (n, dropped, path.name if n else None)

    comp_path = vdir / "companies" / f"{base}.csv"
    comp_path.parent.mkdir(exist_ok=True)
    sys.path.insert(0, str(SKILL_DIR))
    from listbuild.icp_fit import classify_company_fit
    nc = 0
    with comp_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COMPANY_COLS)
        w.writeheader()
        for c in conn.execute("SELECT * FROM companies ORDER BY domain"):
            c = dict(c)
            kw = None if c.get("keyword_fit") is None else bool(c["keyword_fit"])
            status, reason = classify_company_fit(icp, c.get("industry"), kw)
            w.writerow({"company_name": c.get("name"), "domain": c.get("domain"), "linkedin_url": c.get("linkedin_url"),
                        "hq_country": c.get("country"), "employee_count": c.get("size"), "industry": c.get("industry"),
                        "qualified": status, "notes": f"{reason}; first seen via {c.get('first_source')}"})
            nc += 1

    rep = vdir / "reports"
    rep.mkdir(exist_ok=True)
    for name in ("cost_report.md", "preview.md"):
        if (run_dir / name).exists():
            shutil.copy(run_dir / name, rep / f"{base}_{name}")

    print(f"imported listbuild run '{icp['name']}' into {vdir.relative_to(root)}")
    for fit, (n, dropped, fname) in summary.items():
        print(f"  {fit:9}: {n:,} people -> people/{fname}" + (f"  ({dropped:,} dropped: already in a contacted ledger)" if dropped else ""))
    print(f"  companies: {nc:,} -> companies/{comp_path.name}")
    print("next: add the TAM + Progress Log entries to the vertical file (sourcing/pipeline.md formats), commit, then push "
          "only the main (fit) file per the current-phase rules.")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("seeds", help="build the exclusion CSV from every contacted ledger")
    s.add_argument("--out")
    i = sub.add_parser("import", help="copy a finished listbuild run into sourcing/data/<vertical>/")
    i.add_argument("--vertical", required=True, help="e.g. vertical-1-staffing-recruitment")
    i.add_argument("--icp", required=True, help="the listbuild config used for the run")
    i.add_argument("--label", required=True, help="short run label for the file names, e.g. full-tam")
    args = p.parse_args(argv)
    {"seeds": cmd_seeds, "import": cmd_import}[args.cmd](args)


if __name__ == "__main__":
    main()
