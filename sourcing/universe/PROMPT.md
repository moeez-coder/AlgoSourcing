You are building the complete prospect universe for Algo Acquisition. Everything you need is in the attached
bundle `algo-universe-bundle.zip`; you do not have access to any other repository.

1. Unzip the bundle and read `BRIEF.md` completely (including sections 6-6d: the lessons and common mistakes from
   the listbuild skill) and `listbuild/README.md` before running anything. It contains the ICP, the ten verticals,
   the tool, the rules, the exclusions and the output format.
2. Check that the env var BLITZ_API_KEY is set (presence only, never print it); stop and tell me if it is missing.
   `pip install -r listbuild/requirements.txt`, then run the tests: `cd listbuild && python -m pytest -q tests`.
3. From `workspace/`, run the free PREVIEW for every config in `workspace/config/` (skip u_v1b_boutique_exec_search
   unless I confirm it). Check Blitz records left. Then STOP and report one table (plus ~10 sample rows per vertical and its title-guard
   fail count, flagging noisy titles per BRIEF.md 6b): per vertical, companies (core +
   keyword-matched), main-list people, review-file people, already-contacted overlap, and the combined estimate vs
   the 1,500,000 target. If it is under 1.5M, measure the levers in BRIEF.md section 8 and tell me the gain of each.
   Wait for my approval.
4. After approval: full `run` for each vertical, one at a time, detached (BRIEF.md section 6, "Long runs"),
   always with `--seeds seeds/contacted_all.csv --discolike-cap-usd 0`. Rerun the same command if one stops.
5. `python ../algo_universe.py --out ../universe_output`. All checks must be 0.
6. Report: combined main-list total vs 1.5M, per-vertical counts, review-file total, country and seniority split, top
   20 companies by people (flag large enterprises), Blitz records used, the "PROVIDER LIMITS HIT" list from each run verbatim, anything skipped or failed. Give me the
   `universe_output/` files.

Hard rules: Blitz only; firmographic filters only; never filter, score or drop people by name, ethnicity or
nationality; dedup on LinkedIn URL only; exclude everyone in seeds/contacted_all.csv and every company in
dnc_clients.csv; nothing is pushed to HeyReach or any outreach tool; never print or save API keys.
