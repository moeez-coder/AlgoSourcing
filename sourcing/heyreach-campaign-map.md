# HeyReach Campaign Map — Algo Acquisition (workspace 126779)

Pulled via `mcp__Algo__get_all_campaigns` on 2026-09-08. Algo Acquisition's own
HeyReach org has 153 total campaigns; this file only tracks the ones relevant
to the 3 active BD verticals.

## How the 4-campaign structure actually works (read this before pushing anything)

Every vertical has 4 campaigns, in dependency order:

| # | Type | What it does | Where its leads come from |
|---|---|---|---|
| 1 | **Con Req** | Sends the LinkedIn connection request | **This is where we push net-new sourced leads** |
| 2 | **Con Acc** | 3-message follow-up sequence | Automated — Clay pushes leads here via webhook once they accept the connection request sent by Con Req. Never push sourced leads here directly. |
| 3 | **Open Check** | Checks if a profile is "open" (messageable without connecting) and views it | A *separate* entry funnel, not used by us right now |
| 4 | **Open Profile** | Sends InMail to confirmed open profiles | Automated — fed by Open Check via Clay webhook, same pattern as Con Acc |

**Standing instruction from the user (2026-09-08): only push sourced leads to
Con Req campaigns.** We are not using the Open Check / Open Profile funnel for
this BD sourcing work. Con Acc and Open Profile are never a push target
either way — they fill automatically from Con Req / Open Check respectively.

So in practice: for each vertical, find its current live **Con Req** campaign
ID below and push there. Ignore the Con Acc / Open Check / Open Profile rows
except as background — they're listed for completeness and because the
"current generation vs. superseded" reasoning below depends on seeing the
whole quadset together.

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

**Push target = Con Req 567452** — but it's currently PAUSED, so before
pushing, either confirm with the user it should be resumed, or check whether
one of the older still-IN_PROGRESS Con Req versions below is the intended live
target instead.

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

**Push target = Con Req 568586** (IN_PROGRESS — live, ready to receive leads).

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

**Push target = Con Req 587149** (IN_PROGRESS — live, ready to receive leads).

Superseded Sept 2 generation (DRAFT/PAUSED, likely not the live target — do
not push here unless the user says otherwise): Con Req 580487 (PAUSED),
Con Acc 580482 (PAUSED), Open Check 580514 (DRAFT), Open Profile 580496 (DRAFT).

## How to push sourced leads in

**Only push to each vertical's Con Req campaign** (see "Push target" line in
each section above). Never push directly to Con Acc, Open Check, or Open
Profile — Con Acc and Open Profile fill automatically from Clay via webhook,
and Open Check is a different funnel we aren't using for this project.

Use `mcp__Algo__add_leads_to_campaign` / `add_leads_to_campaign_v2` with the
Con Req campaign ID above, or `add_leads_to_list` if staging into its
`linkedInUserListId` first (each campaign above has one attached — see
`linkedInUserListId` in the raw pull). Always re-confirm the campaign's
current status and `progressStats` right before pushing, since these numbers
move daily.
