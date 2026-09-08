# Sourcing Pipeline — Blitz + Clay → HeyReach

**Before starting, read `TOOLS.md`** for what's actually callable right now
(Clay and Blitz are both live as of 2026-09-08; Cold IQ/Prospeo are not) and,
critically, where API keys actually live (environment-level config — never
in this repo or in chat). Blitz has no MCP wrapper — call its REST API
directly via HTTP using the `BLITZ_API_KEY` env var, after confirming your
session's environment actually has it.

## Workflow

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
