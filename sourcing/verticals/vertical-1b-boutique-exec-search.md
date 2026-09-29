# Vertical 1b — Boutique Executive Search (2-9 staff)

## Status

**Groundwork done 2026-09-29 by the master session; no sourcing run, no HeyReach campaigns yet.** Approved by the
user as a new vertical on 2026-09-29 (portfolio card V1b in `../verticals-portfolio.md`). This vertical's own
session does its sourcing and pushes (`../COORDINATION.md`); the master session checks the work. Work on `main`.

- listbuild config: `sourcing/listbuild/config/v1b_boutique_exec_search.yaml`
- Data folder: `sourcing/data/vertical-1b-boutique-exec-search/` (companies, people, reports, `contacted_ledger.csv`)
- HeyReach: **no campaigns yet**. Creating them (4-campaign set + 2 Clay webhooks, `heyreach-vertical-launch` skill)
  needs the user's go-ahead, sender accounts, copy and the Clay webhook URLs. See `../heyreach-campaign-map.md`.

## Target companies

- Retained and contingent executive search boutiques with 2-9 employees on LinkedIn and revenue >= $1M: firms placing C-suite, VP and board leaders, often for PE-backed and growth companies.
- Why: 12 of the 35 recruitment clients have 10 or fewer LinkedIn staff (Harrison Stone, Brick, Sequel, SIG, Astro Talent, Harrison Davies, Rosenstein, Mastrovito). Retained fees of $50-100k+ make the economics the best of any vertical.
- Filters: HQ in the 43 US/UK/Europe codes; revenue >= $1M; **2-9 employees on LinkedIn (user-approved exception to the >= 10 rule, 2026-09-29; disjoint from V1, which starts at 10)**. Core: Executive Search Services. Keyword-gated: Staffing and Recruiting, on retained search / executive search / C-suite search / board search / leadership search / headhunting / search firm.
- Company types excluded: Nonprofit, Government Agency, Educational, Educational Institution.

## Target personas / titles

Director and above, enforced by the listbuild title guard (`../icp-overview.md`, "Seniority filter"). Focus:
Founder, Managing Partner, Partner, Managing Director, CEO, Owner.

## Messaging angle

Meetings with PE-backed CEOs, CHROs and hiring executives; retained-mandate economics.

## Notes

Small firms: expect 1-3 decision-makers per company. Overlaps V1 only at the ledger level (V1 is >= 10 staff).

## Dedup ledger

`sourcing/data/vertical-1b-boutique-exec-search/contacted_ledger.csv` (header only as of 2026-09-29). Check before every push, update
right after every push. The listbuild seeds (`algo_bridge.py seeds`) include every vertical's ledger, so nobody
contacted in another vertical is sourced here, and `data/dnc_clients.csv` clients are dropped at import.

## TAM (Total Addressable Market) — append-only, newest entry on top

### 2026-09-29 11:20 UTC — master session (listbuild preview, free)
- Companies matching ICP filters: ~678 in core industries; ~13,801 keyword-matched small staffing firms (of 40,375). Method: Blitz company counts with the config's
  filters (43 US/UK/Europe HQ codes, revenue >= $1M, headcount as above, company types excluded); canary passed.
- People matching persona/title filters: ~934 main-list people (Executive Search Services) + ~31,111 in Staffing and Recruiting before the keyword gate (Blitz people counts, director-plus job levels).
- Notes: 5 of 93 sampled rows fail the title guard; 0 of 93 already prospected. Sample is on target (KT Executive Search, DRC Search, Eames Partnership, Blue Danube Executive Search). Blitz only: Clay quota exhausted until 2027-01-01; DiscoLike 403 "monthly usage limit".

## Progress Log (append-only — newest entry on top; do not edit or delete other sessions' entries)

### 2026-09-29 11:20 UTC — master session — GROUNDWORK + PREVIEW, NO RUN, NO PUSH
- Created this file, the listbuild config, the data folder and an empty contacted ledger; ran the free preview (TAM above).
- Next (this vertical's session): review the preview sample with the user, then `listbuild run` once approved,
  `algo_bridge.py import`, review, and push only when the user approves and HeyReach campaigns exist.
