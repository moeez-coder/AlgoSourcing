# Vertical 7 — Nearshore / Offshore Development Teams (TEST)

## Status

**Groundwork done 2026-09-29 by the master session; no sourcing run, no HeyReach campaigns yet.** Approved by the
user as a new vertical on 2026-09-29 (portfolio card V7 in `../verticals-portfolio.md`). This vertical's own
session does its sourcing and pushes (`../COORDINATION.md`); the master session checks the work. Work on `main`.

- listbuild config: `sourcing/listbuild/config/v7_nearshore_dev.yaml`
- Data folder: `sourcing/data/vertical-7-nearshore-dev/` (companies, people, reports, `contacted_ledger.csv`)
- HeyReach: **no campaigns yet**. Creating them (4-campaign set + 2 Clay webhooks, `heyreach-vertical-launch` skill)
  needs the user's go-ahead, sender accounts, copy and the Clay webhook URLs. See `../heyreach-campaign-map.md`.

## Target companies

- Providers of dedicated developer teams, staff augmentation and nearshore R&D centres, HQ'd in the US, UK or Europe with founders locally present.
- Why: Clients Zipdev and Alcor. $100k+ a year per team; crowded space, and some firms fail the HQ/founder rule.
- Filters: HQ in the 43 US/UK/Europe codes; revenue >= $1M; 10-500 employees on LinkedIn. **All labels keyword-gated**: IT Services and IT Consulting, Information Technology and Services, Outsourcing and Offshoring Consulting, Outsourcing/Offshoring, Software Development, Computer Software, on nearshore, nearshoring, offshore development, staff augmentation, dedicated development team, dedicated team, outstaffing, LatAm / Latin America / Eastern Europe developers, remote developers, software outsourcing, IT outsourcing.
- Company types excluded: Nonprofit, Government Agency, Educational, Educational Institution.

## Target personas / titles

Director and above, enforced by the listbuild title guard (`../icp-overview.md`, "Seniority filter"). Focus:
Founder, CEO, CRO, VP Sales, Head of Business Development.

## Messaging angle

Meetings with CTOs and VPs of Engineering facing hiring freezes.

## Notes

Keywords like 'IT outsourcing' and 'dedicated team' are broad: expect heavy overlap with V5 and a noisy candidates file. The full run pulls ~475k people to keep ~11k companies' worth; tighten keywords before running if Blitz records are short.

## Dedup ledger

`sourcing/data/vertical-7-nearshore-dev/contacted_ledger.csv` (header only as of 2026-09-29). Check before every push, update
right after every push. The listbuild seeds (`algo_bridge.py seeds`) include every vertical's ledger, so nobody
contacted in another vertical is sourced here, and `data/dnc_clients.csv` clients are dropped at import.

## TAM (Total Addressable Market) — append-only, newest entry on top

### 2026-09-29 11:20 UTC — master session (listbuild preview, free)
- Companies matching ICP filters: 0 (all keyword-gated) in core industries; ~11,146 keyword-matched companies (of 136,482). Method: Blitz company counts with the config's
  filters (43 US/UK/Europe HQ codes, revenue >= $1M, headcount as above, company types excluded); canary passed.
- People matching persona/title filters: ~474,913 people across the gated labels before the keyword gate (Blitz people counts, director-plus job levels).
- Notes: 17 of 215 sampled rows fail the title guard; 2 already prospected. Blitz only: Clay quota exhausted until 2027-01-01; DiscoLike 403 "monthly usage limit".

## Progress Log (append-only — newest entry on top; do not edit or delete other sessions' entries)

### 2026-09-29 11:20 UTC — master session — GROUNDWORK + PREVIEW, NO RUN, NO PUSH
- Created this file, the listbuild config, the data folder and an empty contacted ledger; ran the free preview (TAM above).
- Next (this vertical's session): review the preview sample with the user, then `listbuild run` once approved,
  `algo_bridge.py import`, review, and push only when the user approves and HeyReach campaigns exist.
