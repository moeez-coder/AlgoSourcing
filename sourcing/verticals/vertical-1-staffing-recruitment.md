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

`sourcing/data/vertical-1-staffing-recruitment/contacted_ledger.csv` —
14,991 rows as of 2026-09-13 (12,329 from the first sourced batch +
2,662 from the round-2 batch, all pushed to Open Check 567476; 0 rows
pushed to Con Req). Check it before every push, update it after every
push — see `../pipeline.md`, "The contacted ledger."

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

### 2026-09-13 12:49 UTC — execution-session-vertical-1 — ROUND 2: new sourcing + LIVE PUSH (Open Check only)
- User asked to "add more leads." The first batch's 4,433 sourced companies
  were a subset of the full 6,825-company ICP universe (Find People's
  pagination cap left ~2,392 companies unscanned in round 1). Rather than
  re-running the same broad query and risking overlap, targeted exactly
  those 2,392 previously-unsourced companies directly via `company.
  linkedin_url` (Blitz caps this filter at 50 URLs/call — 48 batches, each
  paginated to exhaustion), same Director+ `job_level` filter + exclude-
  list second pass + per-company cap of 5 (keyed on domain).
- Sourced: 1,329 companies / 2,662 people. 0 overlap with the 12,329
  people already in the ledger (cross-checked before building the batch).
- **Fix applied proactively:** the 2026-09-11 push traced its ~0.3-0.45%
  "unaccounted" gap to leads with a null `lastName` being silently dropped
  by `add_leads_to_campaign_v2`. This run backfilled a last name from
  `full_name` for every person missing one before building the push
  payload. Result: unaccounted rate dropped to 0.15% (4 of 2,662) this
  round, vs 0.45% last time — the fix helped but didn't fully eliminate a
  smaller residual gap, so it isn't the sole cause.
- Files: `sourcing/data/vertical-1-staffing-recruitment/companies/2026-09-13_1235_director-plus-round2-batch1.csv`,
         `sourcing/data/vertical-1-staffing-recruitment/people/2026-09-13_1235_director-plus-round2-batch1.csv`
- Pushed the full 2,662-person batch to Open Check 567476 via
  `add_leads_to_campaign_v2`, 27 batches of up to 100 leads, 3 parallel
  agents (continuing the "Open Check only, Con Req stays paused/untouched"
  choice from 2026-09-11 — not re-asked this round since nothing changed
  about Con Req's status).
  - Added (genuinely new): 2,261
  - Updated (already existed): 397
  - Failed (API-reported, per-lead): 0
  - Unaccounted: 4 of 2,662 (0.15%)
  - Checked against campaign 567476's own `progressStats`: `totalUsers`
    35,669 -> 37,845 (delta 2,176) — close to but not exactly the 2,261
    added tally, same small-gap pattern as 2026-09-11's push; not forcing
    a false reconciliation.
- Ledger: all 2,662 attempted people appended with `open_check_pushed_at`
  = this run's timestamp and `open_check_campaign_id` = 567476. Ledger
  total is now 14,991 rows (12,329 + 2,662).
- Coverage note: 4,433 + 1,329 = 5,762 of the 6,825 total ICP-qualifying
  companies have now been sourced from (84%). ~1,063 companies remain
  fully unscanned for a future round-3 batch, using the same
  company.linkedin_url-targeting approach.
- Same judgment-call flags as before apply here too (a nonprofit-adjacent
  org and at least one data-quality-artifact title string turned up in
  spot-checks) — not filtered out unilaterally, consistent with prior
  rounds' treatment.

### 2026-09-11 20:46 UTC — execution-session-vertical-1 — LIVE PUSH (remainder of the 2026-09-09 batch, Open Check only)
- User asked to "send more to con req and open check." Live-checked both
  campaigns first: Open Check 567476 had drained further to FINISHED again
  (26,897 total, up from 25,531 two days ago — confirms the earlier
  session's finding that pushing leads directly flips FINISHED ->
  IN_PROGRESS, no `resume_campaign` call needed). Con Req 567452 was
  PAUSED with 23,041 people already mid-flight from prior activity
  unrelated to this batch (7,433 in progress + 15,608 pending) — resuming
  it would restart sending to all of them, not just new leads, so I
  surfaced that distinction to the user before acting. **User chose to
  push only to the live one (Open Check) and leave Con Req paused/
  untouched** — 0 leads pushed to Con Req this round, same as before.
- Pushed the entire remaining 10,329-person held-back batch (from
  2026-09-09_1404_director-plus-batch1.csv) to Open Check 567476 via
  `add_leads_to_campaign_v2`, 104 batches of up to 100 leads, 10
  independent agents in parallel.
  - Added (genuinely new): 7,886
  - Updated (already existed): 2,397
  - Failed (API-reported, per-lead): 0
  - Unaccounted: 46 of 10,329 (0.45%) — same small gap pattern as the
    2026-09-09 push, but this time one push agent (chunks 055-065) traced
    it precisely: **every unaccounted lead in its batch had a null
    `lastName`** (3 for 3 — Manioris/crismanioris, Olivia/olivia-mae,
    Roth/cam-roth), and no chunk without a null-lastName lead was short.
    Other agents saw the same correlation on spot-check (chunk_054,
    chunks 013/015). Working theory, not fully confirmed across every
    unaccounted lead: `add_leads_to_campaign_v2` silently drops leads
    missing a last name rather than reporting them as failed. Worth a
    fix in the sourcing pipeline (backfill a placeholder last name from
    the full name when Blitz doesn't return one) before the next large
    push, across all verticals, not just this one.
  - Checked against campaign 567476's own `progressStats`: `totalUsers`
    26,897 -> 35,669 (delta 8,772) — **does not exactly match the 7,886
    added tally**, unlike the 2026-09-09 push's exact match. The ~15-minute
    wall-clock window across 10 parallel push agents means other queue
    activity on this campaign (leads moving between pending/in-progress/
    finished, `totalUsersFailed` also ticked 1784->1785) could account for
    the gap; flagging the discrepancy rather than claiming a clean
    reconciliation, since Con Req's own live figures are being watched
    for evidence of similar drift going forward.
- Ledger: all 10,329 attempted people appended with `open_check_pushed_at`
  = this run's timestamp and `open_check_campaign_id` = 567476. Combined
  with the 2026-09-09 push, **the entire 12,329-person sourced batch is
  now in the ledger as pushed to Open Check** — 0 rows have a
  `con_req_pushed_at` value; Con Req remains fully unpushed for this
  vertical pending a separate go-ahead to resume it.
- Notes for the next session: if the user later asks to push to Con Req
  567452, that decision (resume now vs. queue-and-leave-paused) needs to
  be raised again explicitly — it wasn't answered "no" permanently, just
  deferred this round in favor of the live campaign. No new sourcing was
  done this run; this is a pure push-the-existing-batch entry.

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
