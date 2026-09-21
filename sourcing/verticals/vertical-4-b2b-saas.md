# Vertical 4 — B2B SaaS Companies

## Status

**Full remaining TAM push COMPLETE as of 2026-09-21 (this session)** — the
~13,793 people sourced-but-unpushed from
`people/2026-09-21_1600_blitz_fulltam.csv` were pushed to both Con Req
(612584) and Open Check (612587) in 138 batches, split across multiple
parallel background agents. Both campaigns now confirmed at
**totalUsers = 14,576** each (verified via `mcp__Algo__get_campaign`).
`contacted_ledger.csv` was rebuilt from scratch from HeyReach's actual Con
Req list membership (`get_leads_from_list` on list 954767, paginated in 15
batches of up to 1000) as ground truth — 14,576 rows, 14,537 matched back to
the source CSVs by normalized `linkedin_url`, 39 unmatched (HeyReach-only
name/company/title recorded, `first_sourced_run_file` = "unmatched"). Note:
Open Check's actual list ID is **954769** (confirmed via `get_campaign` on
612587 this session), not 954768 as earlier notes assumed — Con Req's list
(954767) remains the ground-truth source for the ledger per the standing
instruction, and it's in sync with Open Check by count.

**Live as of 2026-09-21** — per the user's explicit go-ahead, the testing/
priming pause (`pipeline.md`) was lifted for Vertical 4 only (not the other
verticals). Both Con Req (612584) and Open Check (612587) are IN_PROGRESS.
Two batches pushed to each so far: 10 leads (Clay, CEO/Founder-level,
founder-presence-verified) then 200 more (Blitz bulk people-search,
industry-only TAM, geo-filtered to contact location US/GB/CA as a founder-
presence proxy) — 210 total per campaign. Both webhooks are active and
verified. No tracking-clients `icp_config` / `sourcing_config` exists yet for
this vertical.

**Full TAM sourced but only partially pushed (2026-09-21 second run):** a
Blitz bulk company+people search (industry-only, no SaaS keyword — see
target-companies section) returned 20,000 raw person-records across the
full run of pagination; after dedup, geo-filtering (contact location
US/GB/CA), and a title/domain sanity filter, **14,590 clean, qualified
people across ~11,000 companies** were saved to
`sourcing/data/vertical-4-b2b-saas/people/2026-09-21_1600_blitz_fulltam.csv`
and `.../companies/2026-09-21_1600_blitz_fulltam.csv`.

**807 of those 14,590 were pushed live this session** (confirmed by pulling
the actual HeyReach list membership as ground truth, not by counting API
calls — several individual pushes during this run hit different per-call
lead counts than expected, likely due to within-batch name/company overlaps,
so the ledger was rebuilt directly from `get_leads_from_list` rather than
trusting the running tally). Both Con Req (612584) and Open Check (612587)
lists are confirmed synced at exactly 807 leads each as of this session.
**~13,783 people remain sourced-but-unpushed** in the CSV above (roughly
rows 808 onward by `linkedin_url`, though the exact split isn't row-aligned
— always check the ledger's `linkedin_url` column against the person before
pushing, not the CSV row number). **The next session should resume pushing
from there**, in ≤100-lead batches to each campaign, and after every batch
**pull `get_leads_from_list` (or `get_campaign`'s `totalUsers`) to confirm
the real count** rather than trusting the running tally of `addedLeadsCount`
values — that's what caused the Con Req/Open Check drift this session (one
campaign got several batches the other didn't, caught only by comparing
`totalUsers` between the two `get_campaign` calls).

**Root cause of Open Check's earlier 500 error, resolved:** the user
confirmed Open Check requires senders with an active LinkedIn Sales
Navigator license to start. The original 100-account pool (cloned from
Vertical 1) only had 80/100 Nav-licensed; swapping in 20 Nav-licensed
accounts (from the wider workspace pool, `isValidNavigator: true` +
`isActive` + `authIsValid`) via `mcp__Algo__update_campaign_accounts` fixed
it immediately. **Open Check's sender list is therefore slightly different
from Con Req/Con Acc/Open Profile's** — see the exact 100 IDs in the git
history of this run if needed, or re-pull via `get_campaign`.

### HeyReach campaigns (workspace 126779)

Cloned from Vertical 1's templates, "US & Europe | ... | Vertical 4 |Moe 1.0"
naming, senders = Vertical 1's account pool (4 disconnected/invalid accounts
swapped out for other valid Vertical 1 accounts to keep the pool at 100).

| Stage | Campaign name | Campaign ID | List ID | Status (2026-09-21) |
|---|---|---|---|---|
| Con Req | US & Europe \| Con Req \| Vertical 4 \|Moe 1.0 | 612584 | 954767 | **IN_PROGRESS — live**, 10 leads loaded and sending (first batch, 2026-09-21) |
| Con Acc | US & Europe \| Con Acc \| Vertical 4 \|Moe 1.0 | 612586 | 954768 | DRAFT (terminal, no webhook needed) |
| Open Check | US & Europe \| Open Check \| Vertical 4 \|Moe 1.0 | 612587 | 954769 | **IN_PROGRESS — live**, 10 leads loaded and sending (first batch, 2026-09-21). Sender list swapped to all-Sales-Nav-licensed accounts (see Status above). |
| Open Profile | US & Europe \| Open Profile \| Vertical 4 \|Moe 1.0 | 612588 | 954770 | DRAFT (terminal, no webhook needed) |

All 4 cloned sequences were confirmed structurally correct against the
`heyreach-vertical-launch` skill's spec (Con Req: single CONNECTION_REQUEST;
Con Acc: 3-message MESSAGE chain with `{message1}`/`{message2}`/`{message3}`;
Open Check: CHECK_IS_OPEN_PROFILE → VIEW_PROFILE; Open Profile: single INMAIL
with `{subject}`/`{inmail}`).

**Push targets once ready:** Con Req 612584 and Open Check 612587 (per the
standing instruction in `../heyreach-campaign-map.md` — push sourced leads to
both, never to Con Acc/Open Profile, which fill automatically via Clay
webhook).

### Clay webhooks

| Webhook | Event | Scoped campaign | Webhook ID | Status |
|---|---|---|---|---|
| Vertical 4 \| Moe \| Acc | CONNECTION_REQUEST_ACCEPTED | Con Req 612584 | 82967 | Active, verified |
| Vertical 4 \| Moe \| Open | VIEWED_PROFILE | Open Check 612587 | 82968 | Active, verified |

## Target companies (draft — confirm/refine before large sourcing runs)

- B2B SaaS companies (software sold to other businesses, subscription/ARR
  model) doing active outbound BD/growth motion — i.e. companies that would
  be a buyer of Algo's own outbound sourcing/BD service, mirroring the
  self-referential logic used for the other 3 verticals (each vertical
  targets companies structurally similar to Algo's own ICP for that segment).
- Apply shared filters from `../icp-overview.md`: revenue ≥ $1M, headcount ≥
  10, HQ in USA/UK/Europe with founders locally present.
- No `fixed_signals` defined yet — candidate signals to consider: recent
  funding round (fresh budget for GTM hires), new VP/Head of Sales or
  Marketing hire, notable product launch or new pricing tier, job postings
  for AE/SDR/BDR roles (signals active outbound investment), G2/Capterra
  review velocity uptick.
- **Working Blitz filter (first real batch, 2026-09-21):** industry in
  {Computer Software, Software Development, Business Intelligence Platforms,
  Data Infrastructure and Analytics, Desktop Computing Software Products,
  Mobile Computing Software Products}, keyword include "SaaS", keyword
  exclude {staffing, recruiting, consulting} (needed — plain
  "IT Services and IT Consulting" pulled in IT staffing/consulting shops, not
  product SaaS), employee_count 10-500, revenue min $1M, HQ US/GB/CA,
  type = Privately Held. This combination produced clean B2B SaaS product
  companies (see companies CSV below) — reuse it as the starting filter next
  run.
- **Data-quality note:** Clay's per-company contact pull can return people no
  longer at the company (e.g. Scratchpad's pull returned contacts whose
  `latest_experience_company` was a different company as of 2026-08) —
  always check `latest_experience_company` matches before trusting a
  contact, not just the company search hit.
- **Full-TAM run (2026-09-21, "industry-only"):** used Blitz's bulk
  `/v2/search/people` endpoint (company + person filters combined in one
  call — far more efficient than per-company Clay pulls at this scale) with
  the same industry/employee/revenue/HQ filters above but **no SaaS keyword
  narrowing** (per explicit user instruction to source the "full 5,721,
  industry-only" TAM). `people.job_title.include` =
  [CEO, Founder, Co-Founder, VP Sales, VP Marketing, Head of Growth,
  Head of Demand Generation, Chief Revenue Officer, CRO],
  `people.job_level` = [C-Team, VP, Director]. Paginated 400 pages (20,000
  raw records, cursor still had more — stopped there as a practical cap).
  **Required a title/domain sanity filter afterward** — the API's keyword
  (FTS) title matching let through noise like a bare "Growth" title and
  garbage-looking domains (e.g. "0.email"); re-filtering to require the
  title regex actually contain one of the target keywords, plus a real-
  looking domain, dropped ~1,560 of 16,152 net-new rows (14,590 remained).
  Also filtered contact `country_code` to {US, GB, CA} as a practical proxy
  for "founder locally present" at scale (can't manually verify 14K+
  individuals) — this is weaker than the per-company founder check used in
  the first Clay batch and should be treated as approximate.

## Target personas / titles (draft, mirrored from Vertical 1's buyer profile)

- **Seniority include:** CXO, VP, Head of, Director, Founder
- **Job titles (draft):** CEO, Founder, Co-Founder, VP Sales, VP Marketing,
  Head of Growth, Head of Demand Generation, Director of Revenue Operations,
  CRO
- Drafted from Algo's stated buyer profile; validated in the first real batch
  — all 10 pushed contacts were CEO/Founder-level, easy to find via Clay's
  `find-and-enrich-contacts-at-company` with `job_title_keywords` on this
  list. VP Sales/CRO-level contacts were also found at several companies
  (e.g. Conversica's CRO, Ushur's VP Sales) but not pushed this round — a
  next batch could add a second contact per company at that level.

## To do before next sourcing run

- [x] **Push the remaining ~13,783 people** from
      `people/2026-09-21_1600_blitz_fulltam.csv` to Con Req 612584 and Open
      Check 612587 — **done this session** (138 batches, parallel background
      agents). Both campaigns confirmed at `totalUsers = 14,576`; ledger
      rebuilt from `get_leads_from_list` ground truth.
- [ ] Create a proper `icp_config` + `sourcing_config` in tracking-clients for
      this vertical (mirror the Vertical 1 structure)
- [ ] Confirm/replace the draft target-company and persona lists above with
      the user (now backed by one real batch's results, see above)
- [ ] Write outbound copy (message1/2/3 for Con Acc, subject/inmail for Open
      Profile) before the first accepted connection/open-profile actually
      needs to be messaged — Con Acc/Open Profile still carry Vertical 1's
      unfilled template placeholders, and leads are now flowing toward them
- [ ] Firmographic-only-qualified companies in the companies CSV (marked
      "founder-presence not contact-verified this run") still need a Clay
      contact pull + founder-presence check before their people are pushed
- [ ] Scratchpad (scratchpad.com) needs a manual re-check — Clay's pull
      suggests its founders/leadership may have moved to a company called
      "Clearskies" as of 2026-08; confirm before qualifying or dropping it
- [ ] Connecteam (connecteam.com) is currently disqualified (Tel Aviv-based
      leadership vs. nominal NYC HQ) — confirm with the user this exclusion
      rule should apply the same way it would for Vertical 1-3, since it's a
      judgment call on a borderline case
- [ ] Note for future batches: Open Check's sender list now differs from the
      other 3 campaigns' (swapped to Nav-licensed-only) — keep that in mind
      if reconciling sender pools later

## Dedup ledger

`sourcing/data/vertical-4-b2b-saas/contacted_ledger.csv` — **14,576 rows as
of 2026-09-21** (rebuilt from scratch), one row per lead confirmed in
HeyReach's actual Con Req list membership (`get_leads_from_list` on list
954767, paginated 15x at limit 1000). 14,537 rows matched back to
`people/2026-09-21_1600_blitz_fulltam.csv` or
`people/2026-09-21_1355_clay_batch1.csv` by normalized `linkedin_url`
(lowercased, URL-decoded, trailing slash stripped); 39 rows are unmatched
(HeyReach silently resolved the submitted URL to a different canonical one,
or the lead has no traceable source row) and carry
`first_sourced_run_file = "unmatched"` with name/company/title as returned
by HeyReach itself. All 14,576 confirmed pushed to both Con Req 612584 and
Open Check 612587 (both campaigns verified at `totalUsers = 14,576`). See
`../pipeline.md`, "The contacted ledger."

## Progress Log (append-only — newest entry on top; do not edit or delete other sessions' entries)

- **2026-09-21 19:00 UTC** (ledger-reconciliation session) — **Full remaining
  TAM push completed + ledger rebuilt from ground truth**:
  - Confirmed the full remaining TAM push (the ~13,793 people left unpushed
    as of the prior session's entry) completed via 138 batches split across
    multiple parallel background agents. Both Con Req 612584 and Open Check
    612587 now show `totalUsers = 14,576` (verified via `mcp__Algo__get_campaign`
    on both).
  - Verified Open Check's actual `linkedInUserListId` is **954769** (per
    `get_campaign` on 612587), not 954768 — noted for future reference; Con
    Req's list (954767) is used as the ledger's ground-truth ledger source
    per the standing instruction, and its count matches Open Check's.
  - Paginated `mcp__Algo__get_leads_from_list` on list 954767 in 15 calls
    (limit 1000, offset 0→14000) to pull all 14,576 leads' `profileUrl` +
    HeyReach-side name/company/title.
  - Rebuilt `sourcing/data/vertical-4-b2b-saas/contacted_ledger.csv` from
    scratch: normalized every HeyReach `profileUrl` and every source CSV's
    `linkedin_url` (lowercase, URL-decoded, trailing slash stripped) and
    matched. **14,537 of 14,576 matched** to
    `people/2026-09-21_1600_blitz_fulltam.csv` or
    `people/2026-09-21_1355_clay_batch1.csv`; **39 unmatched** (HeyReach URL
    resolution quirk noted in the prior session's entry recurs at scale) —
    recorded with HeyReach's own name/company/title and
    `first_sourced_run_file = "unmatched"`.
  - Both `con_req_pushed_at`/`open_check_pushed_at` set to 2026-09-21 for all
    rows (today's date, per this session's dual confirmed push).
  - Updated `../heyreach-campaign-map.md` Vertical 4 lead counts from 807 to
    14,576 for both campaigns.
  - To-do: the "push remaining TAM" item is now marked done above.

- **2026-09-21 17:30 UTC** (hub session) — **Continued live push + ledger
  reconciliation**:
  - Pushed further batches of the sourced full-TAM CSV to both Con Req
    612584 and Open Check 612587. Mid-session, `addedLeadsCount` tallies
    from `add_leads_to_campaign_v2` drifted from reality — one campaign
    received several batches the other didn't — caught by comparing
    `totalUsers` via `mcp__Algo__get_campaign` on both campaigns.
  - Both campaigns confirmed synced at **807 leads each** as of this entry.
  - Rebuilt `contacted_ledger.csv` from scratch using
    `mcp__Algo__get_leads_from_list` on list 954767 (Con Req's list) as
    ground truth — pulled all 807 actual member `profileUrl`s, matched them
    back to the sourced Clay/Blitz CSVs (normalizing trailing slashes and
    URL-encoding differences), and wrote one ledger row per confirmed-pushed
    person. One entry (Eric Boduch, 24 and Up) required a manual row — the
    URL we submitted (`eric-boduch-a1b61`) resolved to a different canonical
    profile URL (`ericboduch`) inside HeyReach; note this resolution
    behavior for future runs (submitted `profileUrl` may not equal the
    stored one).
  - Notes: **~13,783 of the 14,590 sourced people remain unpushed** — see
    "To do" above for the exact process to resume, including the
    verify-before-trust lesson from this session's drift.

- **2026-09-21 16:10 UTC** (hub session) — **LIVE RUN, full-TAM sourcing
  (partial push)**:
  - Sourced: full industry-only TAM via Blitz bulk `/v2/search/people`
    (company + person filters combined) — 20,000 raw records across 400
    paginated calls (cursor still had more; stopped as a practical cap for
    one session). After dedup against the ledger, a title/domain sanity
    filter (dropped ~1,560 noisy rows — bare-keyword FTS matches like
    "Growth" and garbage domains), and a contact-location filter
    (US/GB/CA, as a founder-presence proxy at this scale): **14,590 clean
    people across ~11,000 companies**.
  - Files: `sourcing/data/vertical-4-b2b-saas/people/2026-09-21_1600_blitz_fulltam.csv`
    (14,590 rows, full sourced set), `sourcing/data/vertical-4-b2b-saas/companies/2026-09-21_1600_blitz_fulltam.csv`
    (~11,000 unique companies)
  - Pushed to HeyReach Con Req campaign 612584: **200 of the 14,590** (first
    2 chunks of the sourced file) — not the full set; see "To do" above
  - Pushed to HeyReach Open Check campaign 612587: same 200
  - Dedup: checked against the then-10-row ledger from the earlier Clay
    batch, no overlaps found; all 200 newly pushed people written to the
    ledger with both campaigns' push timestamps
  - Notes: **This was a partial push, not a completed full-TAM push** — the
    remaining ~14,390 sourced-but-unpushed people are saved in the CSV
    above and need a follow-up session to push in ~100-lead batches
    (updating the ledger after each batch). Pushing all of them via
    individual tool calls in one turn was not practical (~290 more calls).
    Also note: per explicit user instruction, this Blitz run used
    industry-only filters (no "SaaS" keyword narrowing, unlike the first
    batch's filter) — this is a broader, noisier population than the first
    batch's filter and leans more heavily on the title/domain sanity pass
    for quality; worth revisiting whether the SaaS-keyword-narrowed filter
    would have been a cleaner source for the bulk of this TAM.

- **2026-09-21 14:00 UTC** (hub session) — **LIVE RUN** (testing/priming
  pause lifted for Vertical 4 only, by explicit user instruction):
  - Sourced: 29 companies (Blitz, see filter above) / 10 people (Clay
    `find-and-enrich-contacts-at-company`, CEO/Founder-level contacts at 10
    of those companies)
  - Files: `sourcing/data/vertical-4-b2b-saas/companies/2026-09-21_1355_blitz_batch1.csv`,
    `sourcing/data/vertical-4-b2b-saas/people/2026-09-21_1355_clay_batch1.csv`
  - Pushed to HeyReach Con Req campaign: US & Europe | Con Req | Vertical 4
    |Moe 1.0 (612584), 10 leads — campaign resumed, now IN_PROGRESS
  - Pushed to HeyReach Open Check campaign: US & Europe | Open Check |
    Vertical 4 |Moe 1.0 (612587), 10 leads — campaign resumed, now
    IN_PROGRESS (root cause of its earlier start failure fixed first: needed
    Sales-Nav-licensed senders, see Status section)
  - Dedup: ledger was empty pre-run (new vertical), so no exclusions; all 10
    people written to the ledger with both push timestamps/campaign IDs
  - Exclusions applied: Connecteam disqualified (leadership not
    HQ-region-present per `icp-overview.md`); Scratchpad excluded pending
    manual re-check (Clay pull suggests founders left); 18 of the 29 sourced
    companies are firmographic-qualified only (no Clay contact/founder-check
    pass yet this run) — see companies CSV notes column
  - Notes: Acc webhook (82967) and Open webhook (82968) both created and
    verified correct in this same session, ahead of the push. No
    `icp_config`/`sourcing_config` created in tracking-clients yet.
