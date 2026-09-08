# HeyReach Campaign Map — Algo Acquisition (workspace 126779)

Pulled via `mcp__Algo__get_all_campaigns` on 2026-09-08. Algo Acquisition's own
HeyReach org has 153 total campaigns; this file only tracks the ones relevant
to the 3 active BD verticals. Campaign naming convention observed:
`<geo> | <stage> | Vertical <n> | <version tag>`, where stage is one of:
Con Req (connection request), Con Acc (connection accepted follow-up),
Open Check / Open Profile / Open Profile Check (open-profile InMail-style
outreach), sometimes "Connection Message".

**Statuses drift constantly** (leads exhaust, campaigns get paused/relaunched
with a new version suffix). Treat the IDs below as a map of what existed as of
2026-09-08, not a live status — re-check `mcp__Algo__get_campaign` /
`get_all_campaigns` before pushing a new batch of leads.

## Vertical 1 — Staffing & Recruitment ("US & Europe" campaigns)

Matches the existing tracking-clients ICP config "Recruitment US" (market:
Recruitment, Staffing and Recruiting), sourcing config "Recruitment US -
Custom NEW TEST LOOM" (campaign_count: 4).

Most recent iteration per stage as of 2026-09-08 (there are older superseded
versions of each — see raw pull if needed):

| Stage | Campaign name | Campaign ID | Status (as of 2026-09-08) |
|---|---|---|---|
| Con Req | US & Europe \| Con Req \| Vertical 1 \|Moe 1.4 | 567452 | PAUSED |
| Con Acc | US & Europe \| Con Acc \| Vertical 1 \|Moe 2.0 | 554375 | IN_PROGRESS |
| Open Check | US & Europe \| Open Check \| Vertical 1 \|Moe 1.3 | 567476 | FINISHED |
| Open Profile | US & Europe \| Open Profile \| Vertical 1 \|Moe | 557771 | IN_PROGRESS |

Older still-IN_PROGRESS Con Req versions for this vertical (leads may still be
draining through these — don't double-push the same people): 550752 (Moe),
553390 (Moe 1.2), 560664 (Moe 1.3).

## Vertical 2 — Marketing companies (assumed; confirm with user) ("US" campaigns, no ICP config yet in new system)

| Stage | Campaign name | Campaign ID | Status (as of 2026-09-08) |
|---|---|---|---|
| Con Req | US \| Con Req \| Vertical 2 \| Moe 1.0 | 568586 | IN_PROGRESS |
| Con Acc | US \| Con Acc \| Vertical 2 \| Moe 1.0 | 578018 | IN_PROGRESS |
| Open Check | US \| Open Check \| Vertical 2 \| Moe 1.0 | 568621 | IN_PROGRESS |
| Open Profile | US \| Open Profile \| Vertical 2 \| Moe 1.0 | 580498 | IN_PROGRESS |

No `icp_config` / `sourcing_config` exists yet for this vertical in the new
tracking-clients system — only the raw HeyReach campaigns above.

## Vertical 3 — M&A ("USA" Sept-2 draft set + "M&A - SEPT" relaunch set)

Two generations of campaigns exist. The Sept 2 "USA | ... | Vertical 3" set
looks superseded by the Sept 6 "M&A - SEPT - ..." set (created 4 days later,
actively running/finished vs. the Vertical-3-named ones sitting in
DRAFT/PAUSED).

**Current (Sept 6) generation — use this one:**

| Stage | Campaign name | Campaign ID | Status (as of 2026-09-08) |
|---|---|---|---|
| Con Req | M&A - SEPT - CONN REC | 587149 | IN_PROGRESS |
| Con Acc | M&A - SEPT - CONN ACC | 587222 | IN_PROGRESS |
| Open Profile Check | M&A - SEPT - OPEN PROF CHECK | 587154 | FINISHED (0 users) |
| Open Check | M&A - SEPT - OP CHECK | 587156 | FINISHED |
| Open Profile Msg | M&A - SEPT - OPEN PROF MSG | 587225 | IN_PROGRESS |

Superseded Sept 2 generation (DRAFT/PAUSED, likely not the live target — do
not push here unless the user says otherwise): Con Req 580487 (PAUSED),
Con Acc 580482 (PAUSED), Open Check 580514 (DRAFT), Open Profile 580496 (DRAFT).

## How to push sourced leads in

Use `mcp__Algo__add_leads_to_campaign` / `add_leads_to_campaign_v2` with the
target campaign ID above, or `add_leads_to_list` if staging into a
`linkedInUserListId` first (each campaign above has one attached — see
`linkedInUserListId` in the raw pull). Always re-confirm the campaign's
current status and `progressStats` right before pushing, since these numbers
move daily.
