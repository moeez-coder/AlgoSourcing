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
4. **Push to HeyReach:** once a people file is finalized, push those leads
   into the correct existing HeyReach campaign for that vertical (see
   `heyreach-campaign-map.md`) using `mcp__Algo__add_leads_to_campaign` /
   `add_leads_to_campaign_v2` (or `add_leads_to_list` if staging into the
   campaign's linked list first). Re-check the campaign's live status
   immediately before pushing.
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
pushed_to_campaign_id, pushed_at`

Fill `pushed_to_campaign_id` / `pushed_at` after the HeyReach push step, and
re-save the file (or save a second "pushed" version) so it's clear from the
file alone what has already gone out — this is the main de-dup signal other
sessions should check before sourcing the same vertical again.

## Progress Log entry format (append to the relevant vertical file)

```
### 2026-09-08 14:32 UTC — <session/agent name or id>
- Sourced: N companies / M people
- Files: sourcing/data/<vertical>/companies/2026-09-08_1432_<label>.csv,
         sourcing/data/<vertical>/people/2026-09-08_1432_<label>.csv
- Pushed to HeyReach campaign: <name> (<id>), <count> leads
- Notes: <dedup notes, exclusions applied, anything the next session needs>
```

See `COORDINATION.md` for the rules on running multiple sessions/agents
against this repo at once.
