# Multi-Session Coordination

The user runs a **separate Claude session/agent per vertical** (and possibly
per segment within a vertical), all working out of this same repo at the same
time. These rules exist so sessions don't collide, duplicate pushes, or lose
each other's work.

## Ownership boundaries

- Each session works **one vertical** (`vertical-1-staffing-recruitment`,
  `vertical-2-marketing`, or `vertical-3-ma`) at a time. Stay inside:
  - `sourcing/verticals/<your-vertical>.md` (read + append to Progress Log)
  - `sourcing/data/<your-vertical>/**` (read + write new files)
- Treat these as **shared, read-mostly**: `sourcing/README.md`,
  `sourcing/icp-overview.md`, `sourcing/heyreach-campaign-map.md`,
  `sourcing/pipeline.md`, `sourcing/COORDINATION.md`. If one of these needs a
  substantive change (e.g. a new confirmed campaign ID, a corrected ICP
  filter), make the edit, but keep it additive/small and mention it prominently
  in your Progress Log entry so other sessions notice it on their next pull.
- Never edit another vertical's file, and never edit another session's
  existing Progress Log entries — only append new ones.

## Before doing any sourcing or push in a session

1. `git pull` (or fetch + check) to get any updates other sessions have
   pushed since you last read this repo.
2. Re-read your vertical's file, in particular its Progress Log, so you know
   what's already been sourced and what's already been pushed to HeyReach.
3. Re-check `heyreach-campaign-map.md` for the current live campaign ID for
   your vertical+stage — statuses drift, and another session may have noted a
   change there.

## De-duplication

- Before pushing a batch of people to a HeyReach campaign, check the
  vertical's already-saved people CSVs (`sourcing/data/<vertical>/people/`)
  for LinkedIn URL / email overlap with your new batch, and check the
  campaign's own current lead list if unsure (`get_leads_from_campaign`).
  HeyReach itself may reject/ignore true duplicates, but avoid relying on that
  — check first.
- If two sessions are sourcing the same vertical concurrently (shouldn't
  normally happen under the one-session-per-vertical model, but can if the
  user starts a second one), the second session to push should skip any
  person already logged as `pushed_to_campaign_id` in the first session's CSV.

## After every sourcing/push run (mandatory)

- Save the company list and/or people list as new timestamped CSV files under
  `sourcing/data/<your-vertical>/...` — see `pipeline.md` for the naming
  convention and column format. Do this for every run, not just "final"
  batches — partial/exploratory pulls count too, so nothing is lost if the
  session ends unexpectedly.
- Append one Progress Log entry to your vertical's file (format in
  `pipeline.md`).
- Commit and push these changes to the branch so other sessions can see them.

## Git conflict handling

Because multiple sessions write to this repo concurrently, expect occasional
merge conflicts, mostly in Progress Log sections. Resolve by keeping both
sessions' entries (Progress Logs are append-only lists — a conflict here is
almost always "both entries are valid, keep both, just reorder"), never by
discarding either side. Do not force-push.
