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

`sourcing/data/vertical-1-staffing-recruitment/contacted_ledger.csv` — 2,000
rows as of 2026-09-09 (the Open Check 567476 push below). Check it before
every push, update it after every push — see `../pipeline.md`, "The
contacted ledger."

## TAM (Total Addressable Market) — append-only, newest entry on top

Total companies matching this vertical's ICP filters, and total people
matching its persona/title filters across those companies — not the sample
actually sourced/pushed. See `../pipeline.md`, "TAM entry format."

### 2026-09-09 15:22 UTC — execution-session-vertical-1
- Companies matching ICP filters: 6,825 (US 5,661 + Europe/UK 1,164). Method:
  Blitz Company Search, fully paginated to exhaustion, filtered by
  `company.industry.include` = ["Staffing and Recruiting","Executive Search
  Services","Human Resources Services","Temporary Help Services"],
  `employee_count.min`=10, `revenue.min`=1,000,000, `hq.country_code`=["US"]
  run separately from `hq.continent`=["Europe"] (covers UK).
- People matching persona/title filters across those companies: 50,332 (US
  42,426 + Europe/UK 7,906). Method: Blitz Find People, same company filters,
  `people.job_level`=["C-Team","VP","Director"] (structured seniority field
  per the shared rule's "prefer structured field" guidance), read directly
  from the `total_results` metadata field (single call, no pagination
  needed for the count itself).
- Notes: exact counts, not estimates (Company Search fully exhausted its
  cursor for both geos; Find People's `total_results` is an exact count per
  Blitz's docs). `job_level` alone doesn't capture 100% of Owner/Founder
  titles that Blitz might bucket oddly, so this is a slightly conservative
  floor on the people TAM, not an overcount.

## Progress Log (append-only — newest entry on top; do not edit or delete other sessions' entries)

### 2026-09-09 15:22 UTC — execution-session-vertical-1 — LIVE PUSH (single-campaign exception, same pattern as Vertical 2's 2026-09-09 push — see `../pipeline.md`'s "One-off exception, 2026-09-09" note, now covering both verticals)
- Sourced: 4,433 companies / 12,329 people (Director+, exact/bracket-safe
  server-side `job_level` filter + client-side exclude-list second pass +
  per-company cap of 5, keyed on **company domain** not just LinkedIn URL —
  caught one company, Peoplease, with two separate LinkedIn company pages
  (`peopleasellc` and `peoplease-corporation`) that would have doubled its
  representation under a naive LinkedIn-URL-only cap).
- Files: `sourcing/data/vertical-1-staffing-recruitment/companies/2026-09-09_1404_director-plus-batch1.csv`,
         `sourcing/data/vertical-1-staffing-recruitment/people/2026-09-09_1404_director-plus-batch1.csv`
  (full sourced batch, 12,329 people — only 2,000 of these were actually
  pushed this run, see below; the remaining 10,329 are sourced and deduped
  but NOT YET pushed, held for a follow-up push).
- Campaign-target question resolved with the user: Open Check 567476 (which
  was FINISHED/fully-drained, 24,100 users) — user confirmed **resume/reuse
  567476** rather than creating a fresh Open Check campaign.
- User reviewed a sample and chose to push a 2,000-person subset first
  (round-robin sampled across companies for max diversity — 2,000 people
  from 2,000 distinct companies) rather than the full 12,329, holding the
  remaining 10,329 back.
- **Pushed to HeyReach Open Check campaign 567476** ("US & Europe | Open
  Check | Vertical 1 |Moe 1.3"), 2,000 leads submitted via
  `add_leads_to_campaign_v2`, batches of 100 (20 batches, 4 independent
  agents in parallel, matching Vertical 2's push mechanics).
  - Added (genuinely new): 1,431
  - Updated (already existed in the campaign before this push): 563
  - Failed (API-reported, per-lead): 0
  - Unaccounted (present in neither added/updated/failed across all 20
    batches, despite 0 reported failures): 6 of 2,000 (0.3%) — same small
    gap pattern Vertical 2 flagged (attributed there to HeyReach silently
    collapsing duplicate/near-duplicate LinkedIn profile URLs within a
    batch); not confirmed further here either.
  - Verified against the campaign's own `progressStats`: `totalUsers` went
    24,100 → 25,531 (delta 1,431, exactly matching the "added" count) and
    status flipped FINISHED → IN_PROGRESS with `totalUsersPending` 98 → 1,529
    (delta 1,431, same match). Numbers are real, not just self-reported by
    the push agents.
- **Not pushed to Con Req** — out of scope for this session (Con Req is
  explicitly held for the user to push separately, later, per this
  session's task scope).
- Ledger: all 2,000 attempted people (added + updated + the 6 unaccounted)
  written to `contacted_ledger.csv` with `open_check_pushed_at` = this run's
  timestamp and `open_check_campaign_id` = 567476 — attempted, not just
  "added," is the correct dedup signal regardless of HeyReach's internal
  added/updated bucketing.
- Judgment calls / open questions for the user: (1) a handful of sourced
  companies are HR-tech/payroll/PEO firms (Paychex, Deel, Alight Solutions)
  rather than traditional staffing/recruiting agencies — they matched the
  "Human Resources Services" industry filter and weren't excluded, but may
  not be the intended buyer profile; (2) at least one sourced company
  (CareerSource Heartland) looks like a publicly-funded workforce board, not
  a company that would buy BD/outbound services — same industry-taxonomy
  false-positive risk; (3) hiring-burst signal enrichment (per this
  vertical's "Signal to prioritize" note) was not done this run — the
  `signal(s)` column in the companies CSV is blank for all 4,433 companies.
  Flagging rather than deciding unilaterally whether to tighten the industry
  filter or add a `company.type` exclude for Nonprofit/Government Agency.
- Notes for the next session: 10,329 sourced-but-unpushed people remain in
  the same batch file, already deduped against the ledger as of this run —
  re-check the ledger before reusing them (this run's 2,000 are now in it,
  so a straight re-read of the file already excludes them). Con Req push for
  this vertical's batch is still pending user go-ahead, per the "Open Check
  only" scope of this session.
