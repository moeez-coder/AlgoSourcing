"""Build algo-universe-bundle.zip: a self-contained kit for a Claude Code session OUTSIDE this repo.

    python sourcing/universe/make_bundle.py --out <dir>      (run from the repo root)

Contents: BRIEF.md, PROMPT.md, algo_universe.py, listbuild/ (the skill's code, tests, providers.yaml),
workspace/config/u_*.yaml (each vertical config with the 2026-10-14 universe ICP applied: Canada added to HQ and
person countries, employee_count_min 11, revenue > $1M), workspace/seeds/contacted_all.csv (every contacted
ledger), workspace/dnc_clients.csv.
"""
import argparse, shutil, subprocess, sys, zipfile
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / ".claude" / "skills" / "listbuild"
HERE = Path(__file__).resolve().parent


def universe_config(src):
    cfg = yaml.safe_load(src.read_text(encoding="utf-8"))
    name = cfg["name"]
    cfg["name"] = "u_" + name
    for key in ("company_hq_countries", "person_countries"):
        if "CA" not in cfg[key]:
            cfg[key] = list(cfg[key]) + ["CA"]
    cfg.setdefault("clay_country_names", {})["CA"] = "Canada"
    cfg["revenue_min_usd"] = 1_000_000
    if name != "v1b_boutique_exec_search":
        cfg["employee_count_min"] = 11
    head = (f"# ALGO universe run (2026-10-14) — generated from {name}.yaml by make_bundle.py.\n"
            f"# ICP: HQ + person in US/CA/UK/Europe (44 codes), revenue > $1M, employees on LinkedIn >= "
            f"{cfg.get('employee_count_min')}" + (f" and <= {cfg['employee_count_max']}" if cfg.get("employee_count_max") else "")
            + ", Director+, nonprofit/government/education excluded.\n")
    if name == "v1b_boutique_exec_search":
        head += "# V1b keeps 2-9 employees, which contradicts 'more than 10': run it only if the user confirms.\n"
    return cfg["name"], head + yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True)


def main():
    p = argparse.ArgumentParser(); p.add_argument("--out", required=True); a = p.parse_args()
    out = Path(a.out).resolve(); stage = out / "algo-universe-bundle"
    if stage.exists(): shutil.rmtree(stage)
    (stage / "workspace" / "config").mkdir(parents=True); (stage / "workspace" / "seeds").mkdir()
    (stage / "workspace" / "logs").mkdir()
    shutil.copytree(SKILL, stage / "listbuild", ignore=shutil.ignore_patterns(
        "__pycache__", ".pytest_cache", "algo_bridge.py", "setup.py", "SKILL.md", "test_algo_bridge_dnc.py", ".env*"))
    for f in ("BRIEF.md", "PROMPT.md", "algo_universe.py"):
        shutil.copy(HERE / f, stage / f)
    for src in sorted((ROOT / "sourcing" / "listbuild" / "config").glob("*.yaml")):
        name, text = universe_config(src)
        (stage / "workspace" / "config" / f"{name}.yaml").write_text(text, encoding="utf-8")
    subprocess.run([sys.executable, str(SKILL / "scripts" / "algo_bridge.py"), "seeds",
                    "--out", str(stage / "workspace" / "seeds" / "contacted_all.csv")], check=True, cwd=ROOT)
    shutil.copy(ROOT / "sourcing" / "data" / "dnc_clients.csv", stage / "workspace" / "dnc_clients.csv")
    zpath = out / "algo-universe-bundle.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(stage.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(out))
        z.writestr("algo-universe-bundle/workspace/logs/.keep", "")
    print(f"wrote {zpath} ({zpath.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
