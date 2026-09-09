# Vertical 1 — Staffing & Recruitment

## Status

Live vertical, most mature. Existing tracking-clients ICP config: "Recruitment
US" (`6ff6d647-764f-401b-8f3c-d470fb731ddd`), sourcing config "Recruitment US -
Custom NEW TEST LOOM" (`24dd6abd-06d2-43eb-853f-50fa41dd2288`). HeyReach
campaigns: see `../heyreach-campaign-map.md` (Vertical 1 section).

## Target companies

- Staffing, recruitment, and executive-search firms (any specialty vertical —
  construction, maritime/offshore, defense/aerospace, etc. — Algo's own
  testimonials span multiple recruiting niches).
- Apply shared filters from `../icp-overview.md`: revenue ≥ $1M, headcount ≥
  10, HQ in USA/UK/Europe with founders locally present.
- Signal to prioritize: **hiring burst** at the target company (per the
  existing ICP config's `fixed_signals`) — a staffing/recruiting firm that is
  itself scaling headcount is a strong buying signal for BD/outbound services.

## Target personas / titles

**Apply the shared seniority filter in `../icp-overview.md`** ("Seniority
filter" section) — Director-and-above: Owner/Founder/Partner, C-suite,
President/Managing Director, Director, VP-and-above in Sales/BD/Growth/
Revenue/Marketing/New Business/Partnerships.

Vertical-specific job titles to search within that seniority band: Head of
Staffing, CEO, Founder, Managing Partner, President, VP Sales, VP Business
Development, Head of Business Development (from Algo's own `callerBriefing`:
"Founders, owners, MDs and sales directors at B2B companies that depend on
outbound"). Use exact/bracket matching per the shared rule's "Matching
method," not loose keyword search.

## Note

The stored tracking-clients ICP config (persona
`eb374338-87bd-4296-a5ae-805a27da3942`) includes Director already (matches
current rule) but still uses a loose/free-text title list rather than
exact/bracket matching, and its `geos`/`company_sizes` predate the
2026-09-08 criteria (US/UK/Europe, revenue floor, no upper headcount cap).
Update the ICP config in tracking-clients (`update_icp_config`) before using
it to drive new sourcing, or treat it as reference only and apply
`../icp-overview.md` filters directly in Clay/Blitz.

## Dedup ledger

`sourcing/data/vertical-1-staffing-recruitment/contacted_ledger.csv` exists
(header row only as of 2026-09-08, no runs yet). Check it before every push,
update it after every push — see `../pipeline.md`, "The contacted ledger."

## TAM (Total Addressable Market) — append-only, newest entry on top

Total companies matching this vertical's ICP filters, and total people
matching its persona/title filters across those companies — not the sample
actually sourced/pushed. See `../pipeline.md`, "TAM entry format."

_No estimate logged yet as of 2026-09-08._

## Progress Log (append-only — newest entry on top; do not edit or delete other sessions' entries)

_No sourcing runs logged yet as of 2026-09-08._
