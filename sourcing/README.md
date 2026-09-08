# Algo Acquisition — BD Sourcing Context

This directory is the persistent context for Algo Acquisition's own outbound BD
sourcing (not a client campaign). Purpose: source people via Blitz API + Clay,
then push them into existing HeyReach campaigns.

**The user runs a separate Claude session/agent per vertical (and possibly per
segment), all working out of this repo concurrently.** Read
`COORDINATION.md` before doing anything else in a new session — it defines
which files you own vs. share, and the pull/log/push discipline that keeps
sessions from colliding or duplicating leads.

## Index

- `COORDINATION.md` — **read first** — rules for running multiple sessions/agents against this repo at once
- `icp-overview.md` — shared firmographic/geographic filters across all verticals
- `verticals/vertical-1-staffing-recruitment.md`
- `verticals/vertical-2-marketing.md`
- `verticals/vertical-3-ma.md`
- `heyreach-campaign-map.md` — every relevant HeyReach campaign ID, by vertical/stage
- `pipeline.md` — the Blitz → Clay → HeyReach sourcing workflow, data-file conventions, and key system IDs
- `data/<vertical>/companies/`, `data/<vertical>/people/` — every sourcing run's output, saved as timestamped CSVs (required for every run — see `pipeline.md`)

## Key IDs (system of record)

- Tracking-clients client record for Algo Acquisition itself: `35bee65b-98e6-4186-a3a5-a097b53dd63a` (name `algoacquisition`, `isAlgo: true`)
- HeyReach workspace ID: `126779`
- Master inbox HeyReach integration ID: `1712`
- Existing ICP config in tracking-clients (new ICP→Sourcing→Campaign system): "Recruitment US", id `6ff6d647-764f-401b-8f3c-d470fb731ddd` — this maps to Vertical 1 below, but its stored filters (US only, headcount 11–500) are **out of date** vs. the criteria agreed 2026-09-08 (see icp-overview.md) and should be updated before relying on it for new sourcing.
- Existing sourcing config: "Recruitment US - Custom NEW TEST LOOM", id `24dd6abd-06d2-43eb-853f-50fa41dd2288`, module = Custom (company-granularity), pointed at Clay workbook `https://app.clay.com/workspaces/770250/workbooks/wb_0thrp4yvduWHnYDHKJQ`. Its `sourcing_instructions` field says: "Use prospeo, use blitz api, combine them together and rate them using Claygent to find the specific signals for each company." `campaign_count: 4` (already linked to 4 HeyReach campaigns, which freezes editing per tracking-clients rules).

## Open items / assumptions to confirm with the user

- Vertical → HeyReach naming mapping (Vertical 1 / 2 / 3) is inferred from campaign names + the one existing ICP config, not explicitly confirmed for Vertical 2. See `heyreach-campaign-map.md` for the reasoning. **Confirm Vertical 2 = Marketing companies before pushing leads there.**
- Multiple HeyReach campaigns exist per vertical per stage (versioned "Moe 1.0", "1.2", "1.3", "2.0" etc., some paused/finished/in-progress simultaneously). Before pushing a new batch of sourced leads, confirm with the user (or check `progressStats`/status fresh) exactly which campaign ID is the live target for that vertical+stage — don't assume the highest version number is still the active one.
