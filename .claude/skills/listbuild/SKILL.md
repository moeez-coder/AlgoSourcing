---
name: listbuild
description: Use for ANY people/company sourcing, TAM sizing or list build in the AlgoSourcing repo (pipeline.md steps 0-4) for Vertical 1 Staffing & Recruitment, Vertical 2 Marketing, Vertical 3 M&A or a new segment, whenever someone says "source", "build a list", "TAM", "more leads", "top up" or asks to run listbuild. Cheapest-first exhaustive build over Blitz -> Clay -> DiscoLike with ledger dedup, title guard and ICP-fit classification. Code ships in this folder.
---

# listbuild (AlgoSourcing edition): cheapest-first exhaustive list build

## Overview
This is the **mandatory method for pipeline.md steps 0-4** (TAM, companies, people, dedup, save) in every session,
master or individual. It layers providers cheapest to most expensive (Blitz -> Clay -> DiscoLike), dedups on the
normalised LinkedIn URL **only** (Algo rule 2026-09-29: never on name + company), excludes everyone in any vertical's `contacted_ledger.csv`, drops
sub-director titles, and splits companies into fit / candidate (keyword-gated catch-all industry) / unknown.
**Preview first; the user approves the sample before any full run.** HeyReach pushes (steps 5-6) stay manual and
follow `sourcing/pipeline.md`'s "Current phase" banner.

Paths used below (run everything **from the repo root** unless a step says otherwise):
- `SKILL` = `.claude/skills/listbuild`
- workspace = `sourcing/listbuild` (`config/` committed; `out/` and `seeds/` gitignored, regenerated on demand)
- vertical configs: `sourcing/listbuild/config/v1_staffing_recruitment.yaml`, `v2_marketing.yaml`,
  `v3_ma_advisory.yaml` (V3 is **DRAFT**: confirm the industry list with the user before a full run)

## Workflow
1. **Keys + deps (every new container, ~1 min).** Keys come from the Claude Code environment, never a file:
   `for k in BLITZ_API_KEY CLAY_API_KEY DISCOLIKE_API_KEY COLDIQ_API_KEY AIARK_API_KEY; do env | grep -q "^$k=" && echo "$k set" || echo "$k MISSING"; done`
   (presence only, never print values). Then `pip install -q -r SKILL/requirements.txt` and
   `python -m pytest -q SKILL/tests`. **Do not run `setup.py` with keys**: it writes a `.env`, which this repo
   forbids. A missing key: stop and tell the user (TOOLS.md, "Where API keys live").
2. **Seeds (every run).** `python SKILL/scripts/algo_bridge.py seeds` rebuilds
   `sourcing/listbuild/seeds/contacted_all.csv` from every vertical's contacted ledger (all verticals, so nobody is
   contacted twice across verticals either). Always pass it as `--seeds`.
3. **Config.** Use the vertical's existing config. For a new segment:
   `cd sourcing/listbuild && python ../../SKILL/scripts/listbuild.py new-icp --name <slug> --industries "<label>" ... --countries ALGO --revenue-min 1000000 --seniority director_plus`
   (`ALGO` = the 43 US/UK/Europe HQ codes from icp-overview.md). Add `--employees-max 500` for the new-vertical cap
   (`--employees-min` defaults to 10; both count employees on LinkedIn). Then copy the `company_type_exclude` block and the
   keyword gates from an existing vertical config. Read the printed notes: catch-all labels become a candidates layer;
   unmapped labels mean a misspelling; "related labels" are suggestions to confirm with the user, never add silently.
4. **Preview (free, ~1 min).** `cd sourcing/listbuild && python ../../SKILL/scripts/listbuild.py --icp config/<slug>.yaml preview --seeds seeds/contacted_all.csv`
   It runs the **Blitz filter canary** first (see rules). Show the user the sizing block (this is the TAM report,
   pipeline.md step 0), ~10 sample rows, the title-check fail count and the prior-list overlap. **Stop until approved.**
5. **Run (20 min to hours; resumable).** Launch with the Bash tool's `run_in_background`, from `sourcing/listbuild`:
   `python ../../SKILL/scripts/listbuild.py --icp config/<slug>.yaml run --seeds seeds/contacted_all.csv --discolike-cap-usd 0`
   If the container kills it, rerun the identical command; finished stages are skipped. **Always cap 0** unless the
   user approved the printed DiscoLike estimate and the balance covers it.
6. **Import into the repo (required, pipeline.md step 4).** From the repo root:
   `python SKILL/scripts/algo_bridge.py import --vertical <vertical-slug> --icp sourcing/listbuild/config/<slug>.yaml --label <short-label>`
   Writes `sourcing/data/<vertical>/people/<stamp>_listbuild-<label>.csv` (fit = the push file),
   `..._candidates.csv` (catch-all industries, review first), `..._unverified.csv` (industry unknown),
   `companies/<stamp>_listbuild-<label>.csv` and `reports/<stamp>_listbuild-<label>_{cost_report,preview}.md`, re-checking
   every row against every ledger. Then append the TAM + Progress Log entries to the vertical file, commit, push.
7. **Push (only when pipeline.md's phase banner allows it).** Push only the main (fit) file to the vertical's Con Req
   and/or Open Check campaign, never Con Acc or Open Profile, then update `contacted_ledger.csv` immediately.

## Quick reference
| Need | Command (from `sourcing/listbuild`, prefix `python ../../SKILL/scripts/listbuild.py`) |
|---|---|
| TAM + sample + overlap, no spend | `--icp config/x.yaml preview --seeds seeds/contacted_all.csv` |
| Whole build, no paid pull | `--icp config/x.yaml run --seeds seeds/contacted_all.csv --discolike-cap-usd 0` |
| Only some stages / redo a stage | `run --stages blitz merge export` / `run --force --stages fit export` |
| Add an industry label the generator does not know | extend `LEGACY_LABELS` / `DISCOLIKE_BUCKETS` in `SKILL/listbuild/icp_gen.py` (+ a test) |

## Provider status (re-check in preview; update TOOLS.md when it changes)
- **Blitz**: live, ~14.9M records/period. Cheapest; always first.
- **Clay public API** (`CLAY_API_KEY`): quota **exhausted until 2027-01-01** (47 of 1,000,000 results left on
  2026-09-29). The run skips Clay and lists it under "PROVIDER LIMITS HIT"; rerun `run --force --stages clay merge domains fit consolidate-final export`
  after the reset. The Clay MCP (`mcp__Clay__*`) is a separate channel and still works for small targeted pulls.
- **DiscoLike**: key valid, account **overdrawn (~ -$4)** and even the free estimate call now answers HTTP 403 "monthly
  usage limit", $0.0035/contact. Cap 0 until the user tops up and approves. A 402/403/429 from Clay or DiscoLike becomes
  a notice and the run continues (`orchestrate.provider_limit_notice`); any other error still stops the run.
- **AI Ark / Cold IQ**: not wired into listbuild yet. Use them afterwards for enrichment or gap-fill (TOOLS.md), and
  feed any extra people through the same seeds + ledger check before saving.

## Rules that came from real failures
- **Blitz silently ignores filters it does not support** and returns the whole database (454,021,881 people /
  68,363,495 companies). That, not a data bug, was the 2026-09-17 "every LinkedIn URL returns Forbes" incident
  (`company.linkedin_url` is not a Company Search filter). Preview and every run's pre-flight fire one single-filter
  canary per filter and abort with `FilterIgnored` if any count equals the unfiltered total. Never bypass it; when you
  add a filter, it goes through the canary automatically. Company lookups by LinkedIn URL use
  `/v2/enrichment/company`, and the join stage now rejects any response whose URL does not match the one requested.
- **Filter-inferred industry is not evidence.** Blitz/Clay rows only carry the industry we filtered on, so fit is
  decided on the company's own enriched industry; without one the row is `unknown`, never `fit`.
- **Clay's person `location_country` spells two countries differently** from its company `country_name`:
  Czech Republic / North Macedonia (person) vs Czechia / Macedonia (company). Configs carry
  `clay_person_country_names`; keep it when you regenerate.
- **Catch-all LinkedIn labels are never core.** "Business Consulting and Services", "Human Resources Services",
  "Financial Services", "Market Research", "Design Services" etc. are keyword-gated (~30% precise) and land in the
  `_candidates` file. Say so to the user at the config step.
- **Seniority = Director and above, enforced in `seniority.py`** (icp-overview.md "Seniority filter"): Associate,
  Coordinator, Specialist, Analyst, Representative, BDR, SDR, Account Executive, Talent Partner fail unless the
  person's own title is top-tier (Founder, Owner, CEO, Managing Director, Chief ... Officer, President, Geschäftsführer,
  Inhaber, Fondateur, Fundador, Eigenaar ...). Assistant/Intern/Trainee/AVP/advisory-board always fail, in any language
  the regex covers. VP passes but is not top-tier. Tighten only test-first (`SKILL/tests/test_seniority.py`).
- **Dedup is LinkedIn-URL-only.** The upstream name+domain matching (exclusion, merge, similar-slug collapse) is
  switched off in `ledger.py` / `seeds.py` / `pipeline.py`; tests in `test_ledger.py` pin it. Do not re-enable it.
- **Percent-encoded LinkedIn slugs** (`%C3%A9`, even double-encoded) are decoded before dedup; never compare raw URLs.
- **Never spend before the estimate.** DiscoLike ignores exclusion lists, so ~40% of paid rows overlap the free
  layers. Spend truth is the billing log (`GET /usage -> billing_events`), not the balance field.
- **Every run attempts every provider.** Never disable a provider or edit the config to dodge a limit; relay the
  closing "PROVIDER LIMITS HIT" list to the user verbatim. Never lower Clay `quota_reserve` below 150k.
- **Recruitment and agency titles are noisy.** "Partner", "Head of <desk>" (recruitment) and "Art Director"
  (agencies) are often fee-earner or mid-level roles; show them in the sample and let the user decide.
- **No Brothers and Lupa Hire are staffing firms** (the 2026-09-17 note called them non-staffing; that was wrong).

## Common mistakes
| Symptom | Cause | Fix |
|---|---|---|
| `FilterIgnored` in preview | a filter Blitz does not support | remove or rename it in the config; never bypass the canary |
| Consultancies in the main list | catch-all label under `fit.core_industries` | move it to `keyword_gated_industries` |
| Prior prospects reappear | seeds not rebuilt, or not passed | rerun `algo_bridge.py seeds` and pass `--seeds` |
| Blitz shard `oversized` | >50k rows in one filter combination | add a dimension to `SHARD_DIMS` or accept partial |
| `HTTP 402` from Clay | quota exhausted | run continues without Clay; rerun the clay stage after 2027-01-01 |
| A sub-director title exported | title-guard gap | add the case to `test_seniority.py`, fix `seniority.py`, rerun `run --force --stages consolidate-final export` |
| `.env` appears in `sourcing/listbuild` | someone ran `setup.py --blitz ...` | delete it; keys live in the environment only |

Provider facts, stage table and ledger schema: `SKILL/README.md`.
