# Vertical 6 — Life-Sciences & Healthcare B2B Services

## Status

**Groundwork done 2026-09-29 by the master session; no sourcing run, no HeyReach campaigns yet.** Approved by the
user as a new vertical on 2026-09-29 (portfolio card V6 in `../verticals-portfolio.md`). This vertical's own
session does its sourcing and pushes (`../COORDINATION.md`); the master session checks the work. Work on `main`.

- listbuild config: `sourcing/listbuild/config/v6_life_sciences_services.yaml`
- Data folder: `sourcing/data/vertical-6-life-sciences-services/` (companies, people, reports, `contacted_ledger.csv`)
- HeyReach: **no campaigns yet**. Creating them (4-campaign set + 2 Clay webhooks, `heyreach-vertical-launch` skill)
  needs the user's go-ahead, sender accounts, copy and the Clay webhook URLs. See `../heyreach-campaign-map.md`.

## Target companies

- Contract research and manufacturing organisations (CROs, CDMOs), clinical-trial and clinical-data services, pharmacovigilance and regulatory consultancies, medical communications and writing, lab and bioanalytical services.
- Why: Healthcare / life sciences recurs in 7 clients (Epic x2, Rosman, Meet Life Sciences, SecondDesk AI, Sensor Bio, Matchstick); life-sciences case study on the site. $50k+ contracts.
- Filters: HQ in the 43 US/UK/Europe codes; revenue >= $1M; 10-500 employees on LinkedIn. **All labels keyword-gated** (changed from the portfolio draft, where Research Services was core: that label also holds market-research and academic firms): Research Services, Research, Biotechnology Research, Biotechnology, Pharmaceutical Manufacturing, Pharmaceuticals, Medical Equipment Manufacturing, on contract research organization, CRO, CDMO, clinical trial services, clinical research, pharmacovigilance, regulatory affairs, medical communications, medical writing, bioanalytical, laboratory services, preclinical services, biostatistics, drug development services.
- Company types excluded: Nonprofit, Government Agency, Educational, Educational Institution.

## Target personas / titles

Director and above, enforced by the listbuild title guard (`../icp-overview.md`, "Seniority filter"). Focus:
CEO, Chief Commercial Officer, VP / Head of Business Development, VP Sales, Head of Partnerships.

## Messaging angle

Meetings with clinical, R&D and procurement leaders at pharma and biotech companies. Proof: Meet Life Sciences.

## Notes

Everything exports to `_candidates` for review; nothing is push-ready without the user's review.

## Dedup ledger

`sourcing/data/vertical-6-life-sciences-services/contacted_ledger.csv` (header only as of 2026-09-29). Check before every push, update
right after every push. The listbuild seeds (`algo_bridge.py seeds`) include every vertical's ledger, so nobody
contacted in another vertical is sourced here, and `data/dnc_clients.csv` clients are dropped at import.

## TAM (Total Addressable Market) — append-only, newest entry on top

### 2026-09-29 11:20 UTC — master session (listbuild preview, free)
- Companies matching ICP filters: 0 (all keyword-gated) in core industries; ~4,738 keyword-matched companies (of 37,208). Method: Blitz company counts with the config's
  filters (43 US/UK/Europe HQ codes, revenue >= $1M, headcount as above, company types excluded); canary passed.
- People matching persona/title filters: ~169,214 people across the gated labels before the keyword gate (Blitz people counts, director-plus job levels).
- Notes: 10 of 213 sampled rows fail the title guard; 0 already prospected. The preview sample is drawn before the keyword gate, so it is not a sample of the final candidates. Blitz only: Clay quota exhausted until 2027-01-01; DiscoLike 403 "monthly usage limit".

## Progress Log (append-only — newest entry on top; do not edit or delete other sessions' entries)

### 2026-09-29 11:20 UTC — master session — GROUNDWORK + PREVIEW, NO RUN, NO PUSH
- Created this file, the listbuild config, the data folder and an empty contacted ledger; ran the free preview (TAM above).
- Next (this vertical's session): review the preview sample with the user, then `listbuild run` once approved,
  `algo_bridge.py import`, review, and push only when the user approves and HeyReach campaigns exist.
