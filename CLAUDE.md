# AlgoSourcing: rules every session follows

Algo Acquisition's own BD sourcing: find director-plus decision-makers at Staffing & Recruitment (V1), Marketing
(V2) and M&A (V3) companies, then push them into HeyReach **Con Req** and **Open Check** campaigns only. This file
loads automatically in every Claude Code session opened on this repo, master or individual.

## Read before doing anything
1. `sourcing/COORDINATION.md`: master vs individual session, who owns which files, pull/log/push discipline.
2. `sourcing/pipeline.md`: the **"Current phase" banner** (which pushes are allowed right now) and the workflow.
3. `sourcing/TOOLS.md`: which tools and keys are live and their quotas.
4. `sourcing/icp-overview.md` + the vertical file in `sourcing/verticals/`: ICP, seniority, TAM and Progress Log.
5. `sourcing/heyreach-campaign-map.md`: campaign IDs per vertical.

## Sourcing method (mandatory)
- **All sourcing, TAM sizing and list builds (pipeline.md steps 0-4) go through the `listbuild` skill**
  (`.claude/skills/listbuild/SKILL.md`). Do not hand-roll Blitz/Clay pagination scripts for bulk pulls: listbuild
  has the filter canary, lossless sharding, dedup, title guard and fit checks that hand-rolled pulls lacked.
  Small one-off lookups (one company, a handful of people) can use the MCP tools or a direct API call.
- Preview first and show the user the TAM, sample rows and exclusions; run only after they approve.
- Cheapest to most expensive (Blitz -> Clay -> DiscoLike, then AI Ark / Cold IQ enrichment), but always every tool:
  the user wants more data, not less. A provider at its limit is reported, never silently skipped.
- Report TAM (companies and people) on every run and log it in the vertical file.

## Never contact anyone twice
- Before any run: `python .claude/skills/listbuild/scripts/algo_bridge.py seeds` (all verticals' ledgers ->
  `sourcing/listbuild/seeds/contacted_all.csv`) and pass it as `--seeds`.
- Dedup keys: normalised LinkedIn URL (lowercase, no query, no trailing slash, percent-decoded) and
  sha1(first|last|domain).
- After every push, update `sourcing/data/<vertical>/contacted_ledger.csv` **before the turn ends**.

## Push rules
- Obey the pipeline.md phase banner and its scoped exceptions; when unsure, ask the user.
- Push only to Con Req and Open Check; **never** to Con Acc or Open Profile (they fill via Clay webhooks).
- Push only the main (fit) people file. `_candidates` and `_unverified` files need the user's review first.
- Pushing leads to a FINISHED campaign resumes it; `resume_campaign` returns 500 on FINISHED campaigns. Resuming a
  PAUSED campaign also restarts everyone already in it: ask first.

## Data files
- Every run is saved under `sourcing/data/<vertical>/{companies,people,reports}/` with the `YYYY-MM-DD_HHMM_<label>`
  naming (`algo_bridge.py import` does this for listbuild runs) and committed. Never overwrite a previous run's file.
- `sourcing/listbuild/out/` and `sourcing/listbuild/seeds/` are scratch (gitignored); the committed record is in
  `sourcing/data/`.

## Keys and secrets
- API keys live only in the Claude Code environment's env vars. Never write a key into the repo, a `.env`, a commit
  or chat. Check presence only: `env | grep -q '^BLITZ_API_KEY=' && echo set`.
- A missing key: stop and tell the user (TOOLS.md, "Where API keys live").

## Git
- Work on `claude/algo-acquisition-sourcing-jmos79`; `git pull origin claude/algo-acquisition-sourcing-jmos79`
  before editing, since other sessions push to it. No PRs unless the user asks.
- Keep the md files current: a finding that changes how others should work goes into the relevant shared file,
  not only into chat.
