# Vertical 3 — M&A (Mergers & Acquisitions)

## Status

Live vertical, currently running its second generation of HeyReach campaigns
("M&A - SEPT - ..." set, created 2026-09-06 — see `../heyreach-campaign-map.md`,
Vertical 3 section, "current generation" table). No tracking-clients ICP
config / sourcing config exists yet for this vertical in the new system —
only raw HeyReach campaigns.

## Target companies (draft — confirm/refine before large sourcing runs)

- M&A advisory firms, business brokerages, investment banks / boutique
  advisory shops doing sell-side/buy-side M&A work, and similar deal-advisory
  firms that rely on outbound BD to win mandates.
- Apply shared filters from `../icp-overview.md`: revenue ≥ $1M, headcount ≥
  10, HQ in USA/UK/Europe with founders locally present.
- No `fixed_signals` defined yet — candidate signals to consider: firm
  announcing a new fund/practice area, senior hire (new MD/Partner), recent
  closed deal announcement (proof of active dealflow), office expansion.

## Target personas / titles (draft, mirrored from Vertical 1's buyer profile)

**Apply the shared seniority filter in `../icp-overview.md`** ("Seniority
filter" section, added 2026-09-08) — Owner/Founder/Partner, C-suite,
President/Managing Director, VP-and-above in Sales/BD/Growth/Revenue/
Marketing/New Business/Partnerships.

**Per-vertical override on Director:** the shared rule excludes plain
"Director" by default, but in investment banking/M&A advisory, "Director"
and especially "Managing Director" are genuinely senior, deal-authority
titles (Managing Director is often the most senior operating title at a
boutique advisory shop, not mid-level like a corporate "Director"). For this
vertical, **include Director and Managing Director** as senior — the default
exclusion doesn't apply here. Still apply the exclude list (Associate,
Analyst, etc.) as normal — "Associate" and "Analyst" are genuinely junior,
non-decision-making titles at advisory firms too.

- **Job titles (draft):** Managing Partner, Managing Director, Director,
  Founder, CEO, President, Head of Business Development, VP Origination/Deal
  Sourcing
- Drafted from Algo's stated buyer profile; not yet validated specifically for
  the M&A-advisory vertical. Refine once real results come back. Use
  exact/bracket matching per the shared rule's "Matching method," not loose
  keyword search.

## To do before next sourcing run

- [ ] Create a proper `icp_config` + `sourcing_config` in tracking-clients for
      this vertical (mirror the Vertical 1 structure)
- [ ] Confirm/replace the draft persona list above
- [ ] Confirm whether to keep feeding the Sept-6 generation campaigns or the
      user wants a fresh relaunch
- [ ] Confirm the Director/Managing Director override above with the user —
      it's a reasonable industry-convention judgment call but not yet
      explicitly signed off

## Dedup ledger

`sourcing/data/vertical-3-ma/contacted_ledger.csv` exists (header row only as
of 2026-09-08, no runs yet). Check it before every push, update it after
every push — see `../pipeline.md`, "The contacted ledger."

## TAM (Total Addressable Market) — append-only, newest entry on top

Total companies matching this vertical's ICP filters, and total people
matching its persona/title filters across those companies — not the sample
actually sourced/pushed. See `../pipeline.md`, "TAM entry format."

_No estimate logged yet as of 2026-09-08._

## Progress Log (append-only — newest entry on top; do not edit or delete other sessions' entries)

_No sourcing runs yet as of 2026-09-08._
