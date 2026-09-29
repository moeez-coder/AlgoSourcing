# Vertical 8 — Fractional Executives & B2B Consultancies (TEST)

## Status

**Groundwork done 2026-09-29 by the master session; no sourcing run, no HeyReach campaigns yet.** Approved by the
user as a new vertical on 2026-09-29 (portfolio card V8 in `../verticals-portfolio.md`). This vertical's own
session does its sourcing and pushes (`../COORDINATION.md`); the master session checks the work. Work on `main`.

- listbuild config: `sourcing/listbuild/config/v8_fractional_consulting.yaml`
- Data folder: `sourcing/data/vertical-8-fractional-consulting/` (companies, people, reports, `contacted_ledger.csv`)
- HeyReach: **no campaigns yet**. Creating them (4-campaign set + 2 Clay webhooks, `heyreach-vertical-launch` skill)
  needs the user's go-ahead, sender accounts, copy and the Clay webhook URLs. See `../heyreach-campaign-map.md`.

## Target companies

- Fractional CFO / CMO / CRO / COO firms, RevOps and go-to-market consultancies, pricing and sales-strategy firms with >= 10 staff.
- Why: 6 clients (Tiffany Otten / Coro, Jeanny Consulting, Sullivan Adventures, Follow The Sun, SharpenHR), almost all under 10 staff. High retainer economics.
- Filters: HQ in the 43 US/UK/Europe codes; revenue >= $1M; 10-500 employees on LinkedIn. **All labels keyword-gated**: Business Consulting and Services, Management Consulting, Strategic Management Services, on fractional CFO/CMO/CRO/COO, fractional executive, fractional leadership, revenue operations, RevOps, go-to-market / GTM consulting, pricing strategy, sales consulting, growth consulting, interim executive.
- Company types excluded: Nonprofit, Government Agency, Educational, Educational Institution.

## Target personas / titles

Director and above, enforced by the listbuild title guard (`../icp-overview.md`, "Seniority filter"). Focus:
Founder, Managing Partner, CEO, Partner.

## Messaging angle

Meetings with founders and CEOs of $5-50M companies.

## Notes

Catch-all consulting labels: the keyword gate is ~30% precise, so review is essential.

## Dedup ledger

`sourcing/data/vertical-8-fractional-consulting/contacted_ledger.csv` (header only as of 2026-09-29). Check before every push, update
right after every push. The listbuild seeds (`algo_bridge.py seeds`) include every vertical's ledger, so nobody
contacted in another vertical is sourced here, and `data/dnc_clients.csv` clients are dropped at import.

## TAM (Total Addressable Market) — append-only, newest entry on top

### 2026-09-29 11:20 UTC — master session (listbuild preview, free)
- Companies matching ICP filters: 0 (all keyword-gated) in core industries; ~3,226 keyword-matched companies (of 36,235). Method: Blitz company counts with the config's
  filters (43 US/UK/Europe HQ codes, revenue >= $1M, headcount as above, company types excluded); canary passed.
- People matching persona/title filters: ~127,587 people across the gated labels before the keyword gate (Blitz people counts, director-plus job levels).
- Notes: 7 of 207 sampled rows fail the title guard; 1 already prospected. Blitz only: Clay quota exhausted until 2027-01-01; DiscoLike 403 "monthly usage limit".

## Progress Log (append-only — newest entry on top; do not edit or delete other sessions' entries)

### 2026-09-29 11:20 UTC — master session — GROUNDWORK + PREVIEW, NO RUN, NO PUSH
- Created this file, the listbuild config, the data folder and an empty contacted ledger; ran the free preview (TAM above).
- Next (this vertical's session): review the preview sample with the user, then `listbuild run` once approved,
  `algo_bridge.py import`, review, and push only when the user approves and HeyReach campaigns exist.
