# Vertical 5 — IT Services & Technology Partners

## Status

**Groundwork done 2026-09-29 by the master session; no sourcing run, no HeyReach campaigns yet.** Approved by the
user as a new vertical on 2026-09-29 (portfolio card V5 in `../verticals-portfolio.md`). This vertical's own
session does its sourcing and pushes (`../COORDINATION.md`); the master session checks the work. Work on `main`.

- listbuild config: `sourcing/listbuild/config/v5_it_services.yaml`
- Data folder: `sourcing/data/vertical-5-it-services/` (companies, people, reports, `contacted_ledger.csv`)
- HeyReach: **no campaigns yet**. Creating them (4-campaign set + 2 Clay webhooks, `heyreach-vertical-launch` skill)
  needs the user's go-ahead, sender accounts, copy and the Clay webhook URLs. See `../heyreach-campaign-map.md`.

## Target companies

- SAP, Salesforce, Microsoft, ServiceNow, Oracle, Workday and Siemens implementation partners; managed IT (MSPs) and cybersecurity services; data and AI consultancies; infrastructure resellers.
- Why: 7 clients (Triumphus, Forge Digital, ITS, Teleion, STORServer, POSRG, Drebcon) plus Local World; Triumphus testimonial. $50k+ projects or monthly contracts; clean LinkedIn label.
- Filters: HQ in the 43 US/UK/Europe codes; revenue >= $1M; 10-500 employees on LinkedIn. Core: IT Services and IT Consulting, Information Technology and Services (legacy), Computer and Network Security. Keyword-gated: Business Consulting and Services, Management Consulting, on SAP / Salesforce / ServiceNow / Microsoft / Oracle / Workday partner, managed services, MSP, systems integrator, digital transformation, cloud migration, cybersecurity services.
- Company types excluded: Nonprofit, Government Agency, Educational, Educational Institution.

## Target personas / titles

Director and above, enforced by the listbuild title guard (`../icp-overview.md`, "Seniority filter"). Focus:
Founder, CEO, Managing Director, Partner, CRO, VP / Head / Director of Sales, Business Development, Alliances.

## Messaging angle

Meetings with CIOs, CTOs and operations leaders at mid-market companies. Proof: Triumphus.

## Notes

Largest new vertical; overlaps V7 (nearshore dev) and V4 (SaaS) at the edges, so the cross-vertical ledger check matters.

## Dedup ledger

`sourcing/data/vertical-5-it-services/contacted_ledger.csv` (header only as of 2026-09-29). Check before every push, update
right after every push. The listbuild seeds (`algo_bridge.py seeds`) include every vertical's ledger, so nobody
contacted in another vertical is sourced here, and `data/dnc_clients.csv` clients are dropped at import.

## TAM (Total Addressable Market) — append-only, newest entry on top

### 2026-09-29 11:20 UTC — master session (listbuild preview, free)
- Companies matching ICP filters: ~87,815 in core industries; ~2,495 keyword-matched consultancies (of 35,121). Method: Blitz company counts with the config's
  filters (43 US/UK/Europe HQ codes, revenue >= $1M, headcount as above, company types excluded); canary passed.
- People matching persona/title filters: ~265,785 main-list people + ~124,736 in consulting labels before the keyword gate (Blitz people counts, director-plus job levels).
- Notes: 14 of 215 sampled rows fail the title guard; 0 already prospected. DiscoLike would add ~219,628 contacts (~$769) once topped up. Blitz only: Clay quota exhausted until 2027-01-01; DiscoLike 403 "monthly usage limit".

## Progress Log (append-only — newest entry on top; do not edit or delete other sessions' entries)

### 2026-09-29 11:20 UTC — master session — GROUNDWORK + PREVIEW, NO RUN, NO PUSH
- Created this file, the listbuild config, the data folder and an empty contacted ledger; ran the free preview (TAM above).
- Next (this vertical's session): review the preview sample with the user, then `listbuild run` once approved,
  `algo_bridge.py import`, review, and push only when the user approves and HeyReach campaigns exist.
