# Sourcing Pipeline — Blitz + Clay → HeyReach

## 🛑 Current phase (as of 2026-09-08): TESTING / PRIMING — DO NOT PUSH TO HEYREACH

The user has explicitly paused all HeyReach pushes across **every vertical**
while sourcing gets tested and primed. This overrides step 5 below until the
user gives explicit final approval to resume live pushes — check with the
user (not just this file) before assuming that approval has happened, and
update this section the moment it does.

While this phase is active, any session — master or individual — should:
- Do the full sourcing workflow (companies → people → dedup-check against the
  ledger → save CSVs) exactly as normal.
- **Skip step 5 (push to HeyReach) and step 6 (update ledger with push
  data) entirely** — do not call `add_leads_to_campaign` /
  `add_leads_to_campaign_v2` / `add_leads_to_list` at all right now.
- **Report back for feedback before going further.** Don't just log a
  Progress Log entry and stop silently — surface to the user: what you
  sourced, sample rows (a handful of companies/people so they can eyeball
  quality), how many passed the ICP filters vs. got excluded and why, any
  judgment calls you made, and any gaps/questions (ambiguous signals, a
  persona list that doesn't feel right, data quality issues). This is
  exactly the point of the testing phase — the user is relying on this
  feedback to decide whether the ICP/persona/signal criteria need
  adjusting before real pushes start.
- Mark the Progress Log entry clearly as a **test run, no push** (see format
  below).

**Before starting, read `TOOLS.md`** for what's actually callable right now
(Clay and Blitz are both live as of 2026-09-08; Cold IQ/Prospeo are not) and,
critically, where API keys actually live (environment-level config — never
in this repo or in chat). Blitz has no MCP wrapper — call its REST API
directly via HTTP using the `BLITZ_API_KEY` env var, after confirming your
session's environment actually has it.

## Data philosophy: maximize coverage, cheap → expensive waterfall

Standing instruction from the user (2026-09-08): **always prefer more data
over less.** Use every tool available for sourcing and enrichment — don't
stop at the first tool/endpoint that returns a partial result if another
available tool could add more (more qualifying companies, more people per
company, more enrichment fields per person — email, phone, verified
LinkedIn, etc.). This applies to the actual sourced sample/batch; it does
**not** loosen the TAM-sizing step above, where using cheap total-match
counts instead of enriching every record is still the right call precisely
because it maximizes what you can report (total market size) for the
least cost.

Sequence tools/endpoints **cheap → expensive**, but only as an ordering rule,
never as a reason to skip a more expensive source:
1. Try the cheapest available source/endpoint first (e.g. Blitz's own
   waterfall cascade already sequences this internally per its docs; a free
   or low-cost Clay lookup before a paid enrichment call).
2. Escalate to progressively more expensive sources/endpoints for whatever
   the cheap tier didn't fully resolve — missing email, missing phone,
   ambiguous company match, etc.
3. Combine and merge results across tools rather than treating the first hit
   as final. If Blitz returns a person's title/company but no email, and
   Clay (or another connected tool) can find the email, use both and keep
   the richer combined record.
4. As new tools get connected (Cold IQ, Prospeo, etc. — see `TOOLS.md`), add
   them into this waterfall rather than treating Clay+Blitz as the ceiling.

## Workflow

0. **TAM sizing (required every run, before/alongside sourcing):** get the
   *total* count of companies matching that vertical's ICP filters, and the
   total count of people matching its persona/title filters across those
   companies — not just the small batch you're actually going to sample.
   Most search tools (Blitz waterfall ICP / people search, Clay searches)
   return a total-match count in their response metadata even when you only
   paginate through a subset — use that rather than trying to enumerate and
   enrich every single match, which would burn far more record budget than
   sizing the market requires. Record the result in the vertical's file under
   its "TAM" section (template there) — this is a running log, not a
   single number, since it'll shift as filters get refined. Report the
   current TAM to the user alongside any sourced sample.
1. **Companies:** find target companies per vertical using Blitz API and/or
   Clay (Clay company search / find-and-enrich-company), filtered by
   `icp-overview.md` + the vertical's own file (revenue, headcount, HQ
   US/UK/Europe with founders locally present, vertical-specific signals).
2. **People:** for qualified companies, find decision-makers via Clay
   (find-and-enrich-contacts-at-company / find-and-enrich-list-of-contacts)
   and/or Blitz, filtered by the vertical's target personas/titles.
3. **Dedup against the ledger BEFORE pushing (required):** load
   `sourcing/data/<vertical>/contacted_ledger.csv` and drop anyone whose
   `linkedin_url` already has a non-empty `con_req_pushed_at` (for the Con Req
   push) or `open_check_pushed_at` (for the Open Check push) — see "The
   contacted ledger" section below. A person can still be eligible for
   whichever of the two campaigns they haven't been pushed to yet.
4. **Save the run to the repo (required — every run, no exceptions):** write
   both the company list and the people list to CSV files under
   `sourcing/data/<vertical>/companies/` and `sourcing/data/<vertical>/people/`
   respectively, then commit them. This is the durable record other
   sessions/agents rely on — don't leave sourcing output only in chat or in an
   external tool's UI.
5. **Push to HeyReach — Con Req AND Open Check:** once a people file is
   finalized and deduped, push those leads into **both** that vertical's Con
   Req campaign and its Open Check campaign (see `heyreach-campaign-map.md` —
   "Push targets" per vertical) using `mcp__Algo__add_leads_to_campaign` /
   `add_leads_to_campaign_v2` (or `add_leads_to_list` if staging into each
   campaign's own linked list first — they each need their own list, don't
   share one). Standing instruction from the user (updated 2026-09-08): **push
   to Con Req and Open Check, never to Con Acc or Open Profile** — those two
   fill automatically via Clay webhook once a lead accepts the connection
   request or is confirmed open-profile. Re-check both campaigns' live status
   immediately before pushing — some verticals' Open Check campaigns are
   currently FINISHED/drained and need confirmation before reuse.
6. **Update the ledger immediately after pushing:** append/update a row per
   person in `sourcing/data/<vertical>/contacted_ledger.csv` with the
   campaign ID(s) and timestamp(s) they were just pushed to. Do this before
   ending the session/turn — an un-logged push is invisible to every other
   session and will cause a duplicate contact next time this vertical is
   sourced.
7. **Log the run** by appending an entry to that vertical's Progress Log
   (bottom of its file in `verticals/`) — see format below.

## The contacted ledger (the actual de-dup mechanism)

Each vertical has one running file: `sourcing/data/<vertical>/contacted_ledger.csv`
— columns: `linkedin_url, full_name, company_name, title, con_req_pushed_at,
con_req_campaign_id, open_check_pushed_at, open_check_campaign_id,
first_sourced_run_file`.

This is the single source of truth for "have we already reached out to this
person," and it's the file every session must check before pushing and update
after pushing — the per-run timestamped CSVs (below) are the audit trail of
what was sourced when, but they are NOT what you check for dedup; always use
the ledger. `linkedin_url` is the dedup key (normalize: strip query params and
trailing slash before comparing).

Two additional safety nets, on top of the ledger:
- HeyReach's own campaign-level exclusion flags
  (`excludeContactedFromSenderInOtherCampaign`, `excludeInOtherCampaigns`)
  are enabled on several of these campaigns already (check via
  `mcp__Algo__get_campaign`) — this stops the platform from re-messaging
  someone already in conversation from the same sender account, independent
  of our ledger.
- If ever in doubt about a specific campaign's current membership, confirm
  directly with `mcp__Algo__get_leads_from_campaign` before a large push.

Neither of those replaces the ledger — the ledger is what lets a session
avoid even *attempting* to push someone twice, and it's what a brand-new
session with no other context can trust on day one.

## TAM entry format (append to the relevant vertical file's TAM section)

```
### 2026-09-08 14:32 UTC — <session/agent name or id>
- Companies matching ICP filters: N (method: <tool/endpoint + filters used>)
- People matching persona/title filters across those companies: M (method: <tool/endpoint + filters used>)
- Notes: <exact/estimate, any filter caveats, overlap with other verticals if relevant>
```

Treat this like the Progress Log — append-only, newest on top, don't edit or
delete another session's prior estimate (the history of how TAM moved as
filters got refined is useful on its own).

## Data file naming convention

`sourcing/data/<vertical-slug>/companies/YYYY-MM-DD_HHMM_<short-label>.csv`
`sourcing/data/<vertical-slug>/people/YYYY-MM-DD_HHMM_<short-label>.csv`

Vertical slugs: `vertical-1-staffing-recruitment`, `vertical-2-marketing`,
`vertical-3-ma`. Use UTC or note the timezone if not UTC. Never overwrite a
previous run's file — each run gets its own timestamped file so the history
of what was sourced/pushed stays intact across sessions.

### Companies CSV — minimum columns

`company_name, domain, linkedin_url, hq_city, hq_country, employee_count,
estimated_revenue, industry, signal(s), qualified (yes/no), notes`

### People CSV — minimum columns

`first_name, last_name, full_name, title, company_name, company_domain,
linkedin_url, email (if found), seniority, source (blitz/clay/both)`

This per-run file is the audit trail of what was sourced in that batch — it
is not the dedup source (that's the ledger, above). After pushing, the
ledger gets the `pushed_to_*` / timestamp data, not this file.

## Progress Log entry format (append to the relevant vertical file)

While the testing/priming phase (above) is active, use this form — no push
happened, so say so explicitly rather than omitting the push lines:

```
### 2026-09-08 14:32 UTC — <session/agent name or id> — TEST RUN, NO PUSH
- Sourced: N companies / M people
- Files: sourcing/data/<vertical>/companies/2026-09-08_1432_<label>.csv,
         sourcing/data/<vertical>/people/2026-09-08_1432_<label>.csv
- Pushed to HeyReach: none (testing/priming phase — awaiting final approval)
- Feedback given to user: <summary of what you reported for review — sample
  quality, exclusion reasons, open questions>
- Notes: <dedup notes, exclusions applied, anything the next session needs>
```

Once the user lifts the pause and live pushes resume, switch to:

```
### 2026-09-08 14:32 UTC — <session/agent name or id>
- Sourced: N companies / M people
- Files: sourcing/data/<vertical>/companies/2026-09-08_1432_<label>.csv,
         sourcing/data/<vertical>/people/2026-09-08_1432_<label>.csv
- Pushed to HeyReach Con Req campaign: <name> (<id>), <count> leads
- Pushed to HeyReach Open Check campaign: <name> (<id>), <count> leads
- Notes: <dedup notes, exclusions applied, anything the next session needs>
```

See `COORDINATION.md` for the rules on running multiple sessions/agents
against this repo at once.
