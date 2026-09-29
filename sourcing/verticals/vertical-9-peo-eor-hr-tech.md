# Vertical 9 — PEO / EOR / Payroll & HR-Tech Providers (TEST)

## Status

**Groundwork done 2026-09-29 by the master session; no sourcing run, no HeyReach campaigns yet.** Approved by the
user as a new vertical on 2026-09-29 (portfolio card V9 in `../verticals-portfolio.md`). This vertical's own
session does its sourcing and pushes (`../COORDINATION.md`); the master session checks the work. Work on `main`.

- listbuild config: `sourcing/listbuild/config/v9_peo_eor_hr_tech.yaml`
- Data folder: `sourcing/data/vertical-9-peo-eor-hr-tech/` (companies, people, reports, `contacted_ledger.csv`)
- HeyReach: **no campaigns yet**. Creating them (4-campaign set + 2 Clay webhooks, `heyreach-vertical-launch` skill)
  needs the user's go-ahead, sender accounts, copy and the Clay webhook URLs. See `../heyreach-campaign-map.md`.

## Target companies

- Professional employer organisations, employer-of-record and global payroll providers, HR outsourcing, HR / payroll software companies.
- Why: Clients Brain Payroll and SharpenHR. High value per client (per-employee fees). V1's 2026-09-29 run held back ~16.7k director-plus people at HR-services firms that are not staffing firms; much of that pool is this vertical.
- Filters: HQ in the 43 US/UK/Europe codes; revenue >= $1M; 10-500 employees on LinkedIn. **All labels keyword-gated**: Human Resources Services, Human Resources, Software Development, Computer Software, on PEO, professional employer organization, employer of record, EOR, global payroll, payroll services, payroll software, HR outsourcing, benefits administration, HRIS, HR software, global employment, workforce management software.
- Company types excluded: Nonprofit, Government Agency, Educational, Educational Institution.

## Target personas / titles

Director and above, enforced by the listbuild title guard (`../icp-overview.md`, "Seniority filter"). Focus:
Founder, CEO, CRO, VP / Head of Sales, Business Development, Partnerships.

## Messaging angle

Meetings with CFOs, COOs and HR leaders at scaling and expanding companies.

## Notes

Overlaps V4 (SaaS) for HR / payroll software firms; the cross-vertical ledger check handles double contact.

## Dedup ledger

`sourcing/data/vertical-9-peo-eor-hr-tech/contacted_ledger.csv` (header only as of 2026-09-29). Check before every push, update
right after every push. The listbuild seeds (`algo_bridge.py seeds`) include every vertical's ledger, so nobody
contacted in another vertical is sourced here, and `data/dnc_clients.csv` clients are dropped at import.

## TAM (Total Addressable Market) — append-only, newest entry on top

### 2026-09-29 11:20 UTC — master session (listbuild preview, free)
- Companies matching ICP filters: 0 (all keyword-gated) in core industries; ~2,709 keyword-matched companies (of 60,294). Method: Blitz company counts with the config's
  filters (43 US/UK/Europe HQ codes, revenue >= $1M, headcount as above, company types excluded); canary passed.
- People matching persona/title filters: ~246,374 people across the gated labels before the keyword gate (Blitz people counts, director-plus job levels).
- Notes: 11 of 215 sampled rows fail the title guard; 4 already prospected. Blitz only: Clay quota exhausted until 2027-01-01; DiscoLike 403 "monthly usage limit".

## Progress Log (append-only — newest entry on top; do not edit or delete other sessions' entries)

### 2026-09-29 11:20 UTC — master session — GROUNDWORK + PREVIEW, NO RUN, NO PUSH
- Created this file, the listbuild config, the data folder and an empty contacted ledger; ran the free preview (TAM above).
- Next (this vertical's session): review the preview sample with the user, then `listbuild run` once approved,
  `algo_bridge.py import`, review, and push only when the user approves and HeyReach campaigns exist.
