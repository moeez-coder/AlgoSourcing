# Sourcing Pipeline — Blitz + Clay → HeyReach

## Workflow

1. **Companies:** find target companies per vertical using Blitz API and/or
   Clay (Clay company search / find-and-enrich-company), filtered by
   `icp-overview.md` + the vertical's own file (revenue, headcount, HQ
   US/UK/Europe with founders locally present, vertical-specific signals).
2. **People:** for qualified companies, find decision-makers via Clay
   (find-and-enrich-contacts-at-company / find-and-enrich-list-of-contacts)
   and/or Blitz, filtered by the vertical's target personas/titles.
3. **Save the run to the repo (required — every run, no exceptions):** write
   both the company list and the people list to CSV files under
   `sourcing/data/<vertical>/companies/` and `sourcing/data/<vertical>/people/`
   respectively, then commit them. This is the durable record other
   sessions/agents rely on — don't leave sourcing output only in chat or in an
   external tool's UI.
4. **Push to HeyReach — Con Req AND Open Check:** once a people file is
   finalized, push those leads into **both** that vertical's Con Req campaign
   and its Open Check campaign (see `heyreach-campaign-map.md` — "Push
   targets" per vertical) using `mcp__Algo__add_leads_to_campaign` /
   `add_leads_to_campaign_v2` (or `add_leads_to_list` if staging into each
   campaign's own linked list first — they each need their own list, don't
   share one). Standing instruction from the user (updated 2026-09-08): **push
   to Con Req and Open Check, never to Con Acc or Open Profile** — those two
   fill automatically via Clay webhook once a lead accepts the connection
   request or is confirmed open-profile. Re-check both campaigns' live status
   immediately before pushing — some verticals' Open Check campaigns are
   currently FINISHED/drained and need confirmation before reuse.
5. **Log the run** by appending an entry to that vertical's Progress Log
   (bottom of its file in `verticals/`) — see format below.

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
linkedin_url, email (if found), seniority, source (blitz/clay/both),
pushed_to_con_req_campaign_id, pushed_to_con_req_at,
pushed_to_open_check_campaign_id, pushed_to_open_check_at`

Fill the four `pushed_to_*` columns after each HeyReach push step (a lead may
land in Con Req and Open Check at different times if they weren't pushed
together), and re-save the file (or save a second "pushed" version) so it's
clear from the file alone what has already gone out to which campaign — this
is the main de-dup signal other sessions should check before sourcing the
same vertical again.

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
