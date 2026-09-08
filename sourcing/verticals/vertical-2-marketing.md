# Vertical 2 — Marketing Companies

## Status

**Confirmed with the user (2026-09-08): Vertical 2 = Marketing companies.**
Live HeyReach campaigns exist (see `../heyreach-campaign-map.md`, Vertical 2
section) but there is **no tracking-clients ICP config or sourcing config yet**
for this vertical in the new system — only raw HeyReach campaigns.

## Target companies (draft — confirm/refine before large sourcing runs)

- Marketing agencies / marketing services companies (e.g. demand gen, paid
  media, branding, PR agencies) that themselves rely on outbound/BD to win
  clients.
- Apply shared filters from `../icp-overview.md`: revenue ≥ $1M, headcount ≥
  10, HQ in USA/UK/Europe with founders locally present.
- No `fixed_signals` defined yet — candidate signals to consider: agency
  hiring burst, new office/market expansion, leadership change (new
  CEO/CRO/Head of Growth), recent funding or acquisition.

## Target personas / titles (draft, mirrored from Vertical 1's buyer profile)

- **Seniority include:** CXO, Director, Vice President, Owner / Partner,
  Founder
- **Job titles (draft):** CEO, Founder, Managing Partner, President, VP
  Sales/Business Development, Head of Growth, Head of New Business
- These are drafted from Algo's own stated buyer profile ("Founders, owners,
  MDs and sales directors at B2B companies that depend on outbound") — not yet
  validated specifically for the marketing-agency vertical. Refine once real
  results come back.

## To do (non-blocking — can proceed with drafts, refine as results come in)

- [ ] Create a proper `icp_config` + `sourcing_config` in tracking-clients for
      this vertical (mirror the Vertical 1 structure) so it's tracked the same
      way
- [ ] Confirm/replace the draft persona list above once real results come back

## Dedup ledger

`sourcing/data/vertical-2-marketing/contacted_ledger.csv` exists (header row
only as of 2026-09-08, no runs yet). Check it before every push, update it
after every push — see `../pipeline.md`, "The contacted ledger."

## TAM (Total Addressable Market) — append-only, newest entry on top

Total companies matching this vertical's ICP filters, and total people
matching its persona/title filters across those companies — not the sample
actually sourced/pushed. See `../pipeline.md`, "TAM entry format."

_No estimate logged yet as of 2026-09-08._

## Progress Log (append-only — newest entry on top; do not edit or delete other sessions' entries)

_No sourcing runs yet as of 2026-09-08._
