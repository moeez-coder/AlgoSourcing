# HeyReach Campaign Map — Algo Acquisition (workspace 126779)

Pulled via `mcp__Algo__get_all_campaigns` on 2026-09-08. Algo Acquisition's own
HeyReach org has 153 total campaigns; this file only tracks the ones relevant
to the 3 active BD verticals.

## How the 4-campaign structure actually works (read this before pushing anything)

Every vertical has 4 campaigns, in dependency order:

| # | Type | What it does | Where its leads come from |
|---|---|---|---|
| 1 | **Con Req** | Sends the LinkedIn connection request | **We push net-new sourced leads here** |
| 2 | **Con Acc** | 3-message follow-up sequence | Automated — Clay pushes leads here via webhook once they accept the connection request sent by Con Req. Never push sourced leads here directly. |
| 3 | **Open Check** | Checks if a profile is "open" (messageable without connecting) and views it | **We also push net-new sourced leads here** (parallel entry point, independent of Con Req/connection status) |
| 4 | **Open Profile** | Sends InMail to confirmed open profiles | Automated — fed by Open Check via Clay webhook, same pattern as Con Acc |

**Standing instruction from the user (updated 2026-09-08): push sourced leads
to both Con Req AND Open Check campaigns** for each vertical — these are two
independent entry points that both accept net-new leads in parallel (Con Req
attempts a connection; Open Check separately checks/views the profile and, if
open, feeds Open Profile automatically). Con Acc and Open Profile are never a
push target either way — they always fill automatically from Con Req / Open
Check respectively via Clay webhook.

So in practice: for each vertical, push the same sourced batch of people to
**both** its current live Con Req campaign ID and its current live Open Check
campaign ID below. Skip Con Acc and Open Profile.

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

**Push targets:**
- **Con Req 567452** — currently PAUSED, so before pushing, either confirm
  with the user it should be resumed, or check whether one of the older
  still-IN_PROGRESS Con Req versions below is the intended live target
  instead.
- **Open Check 567476** — currently FINISHED (fully drained, 24,100 users
  already processed). Confirm with the user whether to resume/reuse this one
  or whether a fresh Open Check campaign should be created for this vertical
  before pushing new leads.

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

**Push targets:**
- **Con Req 568586** (IN_PROGRESS — live, ready to receive leads)
- **Open Check 568621** (IN_PROGRESS — live, ready to receive leads)

No `icp_config` / `sourcing_config` exists yet for this vertical in the new
tracking-clients system — only the raw HeyReach campaigns above.

## Vertical 3 — M&A ("USA" Sept-2 draft set + "M&A - SEPT" relaunch set)

Two generations of campaigns exist. **Confirmed by the user (2026-09-09):
use the "M&A - SEPT - ..." labeled campaigns** (created by Joe) — the
earlier "USA | ... | Vertical 3" Sept-2 set is not in use.

**Confirmed (Sept 6, "M&A"-labeled) generation — use this one:**

| Stage | Campaign name | Campaign ID | Status (as of 2026-09-08) |
|---|---|---|---|
| Con Req | M&A - SEPT - CONN REC | 587149 | IN_PROGRESS |
| Con Acc | M&A - SEPT - CONN ACC | 587222 | IN_PROGRESS |
| Open Profile Check | M&A - SEPT - OPEN PROF CHECK | 587154 | FINISHED (0 users) |
| Open Check | M&A - SEPT - OP CHECK | 587156 | FINISHED |
| Open Profile Msg | M&A - SEPT - OPEN PROF MSG | 587225 | IN_PROGRESS |

**Push targets:**
- **Con Req 587149** (IN_PROGRESS — live, ready to receive leads)
- **Open Check 587156** — currently FINISHED (fully drained, 8,290 users
  already processed). Confirm with the user whether to resume/reuse this one
  or create a fresh Open Check campaign for this vertical before pushing new
  leads. Note there's also an older superseded Open Check (580514, DRAFT,
  Sept-2 generation) — don't use that one either without checking first.

Superseded Sept 2 generation (DRAFT/PAUSED, likely not the live target — do
not push here unless the user says otherwise): Con Req 580487 (PAUSED),
Con Acc 580482 (PAUSED), Open Check 580514 (DRAFT), Open Profile 580496 (DRAFT).

## How to push sourced leads in

**Push each sourced batch to both the Con Req and Open Check campaigns** for
that vertical (see "Push targets" in each section above). Never push directly
to Con Acc or Open Profile — they fill automatically from Clay via webhook
once a lead accepts the connection request (Con Req) or is confirmed
open-profile (Open Check).

Use `mcp__Algo__add_leads_to_campaign` / `add_leads_to_campaign_v2` against
each of the two target campaign IDs, or `add_leads_to_list` if staging into
each campaign's own linked list first (Con Req and Open Check each have their
own dedicated list — never share one list across both). Always re-confirm
both campaigns' current status and `progressStats` right before pushing,
since these numbers move daily — several verticals' Open Check campaigns are
currently FINISHED (fully drained) and need the user's input on whether to
resume/reuse or relaunch before they can receive new leads.
