# Tooling Access — What's Actually Available

Audited 2026-09-08; last updated 2026-09-29 (listbuild adoption, Clay/DiscoLike/Cold IQ keys). Re-verify this list periodically (tool access can change
between sessions/environments) rather than trusting it blindly forever, but
treat it as the reference so every session starts from the same understanding
instead of rediscovering this from scratch.

## Where API keys live (read this first)

**Never put real API key values in this repo, in any committed file, or in
chat.** This repo is pushed to GitHub — a secret committed here is exposed to
everyone with repo access, permanently, in git history, even after you
"remove" it later. It's also the wrong layer architecturally: secrets belong
in environment configuration, not version control.

**Correct place:** environment variables configured at the Claude Code
**environment** level (the environment these sourcing sessions run in — see
the "Environment configuration" docs at
https://code.claude.com/docs/en/claude-code-on-the-web). Set once there, and
every session spawned in that environment inherits it automatically as a
real env var — no repo involvement, no chat exposure, no per-session
re-entry. This is the actual mechanism for "available to every session"
without the security downside.

This repo only tracks:
- `.env.example` (repo root) — lists the env var **names** we expect
  (`BLITZ_API_KEY`, etc.), no values. Safe to commit, meant as documentation.
- `.gitignore` — excludes `.env`/`.env.*` so a real local secrets file can
  never be committed by accident.

If a session needs a key that isn't present in its environment, it should
stop and tell the user, not ask them to paste it into chat or a file.

## Tool-by-tool status

| Tool / MCP server | Status | Notes |
|---|---|---|
| **Clay** (`mcp__Clay__*`) | ✅ Live, functional | Real access to the connected Clay workspace: `find-and-enrich-company`, `find-and-enrich-contacts-at-company`, `find-and-enrich-list-of-contacts`, `query-objects`, `list_subroutines` / `run_subroutine`, etc. This is our primary working sourcing tool right now. |
| **Blitz** (`https://api.blitz-api.ai`) | ✅ Live. **Silently ignores unsupported filters** (see the 2026-09-29 note below; the 2026-09-17 "bug" was this) | `BLITZ_API_KEY` is now set at the environment level. **Verified working** via `GET /v2/account/key-info` from a fresh session that inherited the variable: valid, 14,922,558 records remaining (resets 2026-10-07), 50 req/sec rate limit, plan "Agency - Premium", full endpoint access (waterfall ICP search, people search, employee finder, company search, email/phone/domain↔LinkedIn/company-distribution enrichment, jobs search, account/key-info). There is still no MCP wrapper tool for it — call it directly via HTTP (curl or similar) with the `x-api-key` header, reading `BLITZ_API_KEY` from the environment. Note: a session only sees this env var if its container started *after* the variable was added — check with `env | grep -q '^BLITZ_API_KEY='` before assuming it's present (this hub session, for instance, was already running when the key was added and does not have it as of 2026-09-08). `search_blitz_api_the_api_engine_for` / `query_docs_filesystem_...` remain docs-only tools (endpoint reference), separate from actually calling the API. |
| **Cold IQ** (`https://api.coldiq.com`) | ✅ Key set, auth confirmed | **Not a data source itself — a GTM data marketplace/proxy.** One API key, unified credits, resells ~39 provider groups under `/v1/<provider>/*` (Apollo, Prospeo, FullEnrich, Findymail, Wiza, Icypeas, PDL, Sumble, BlitzAPI, BuiltWith, signal feeds, SEO/web, ad scrapers, and more). Env var `COLDIQ_API_KEY`. **Auth confirmed: `Authorization: Bearer <key>` on the `/v1/*` endpoints.** The `/dashboard/*` endpoints (credits etc.) need a browser session JWT, not the API key. Bundles its own `ai-ark` group, but the user's AI Ark access is a separate standalone account (row below). Repo: https://github.com/Cold-IQ/coldiq-marketplace-skills. Its 17 Claude Code skills are an optional plugin; ask the user before installing a third-party plugin. Not wired into listbuild yet: use it for enrichment and gap-fill after a listbuild run. |
| **AI Ark** (`https://api.ai-ark.com/api/developer-portal`) | ✅ Live, functional (confirmed 2026-09-10) | **Standalone product, not via Cold IQ** (the user has a direct AI Ark account — confirm this distinction before assuming Cold IQ's bundled `ai-ark` group covers it). 400M+ people / 70M+ company profiles, real-time verified emails/mobile numbers, lookalike/signal-based company discovery, personality analysis. Docs: https://docs.ai-ark.com/. Env var: `AIARK_API_KEY` — confirmed present and working via `GET /v1/payments/credits` (full path `https://api.ai-ark.com/api/developer-portal/v1/payments/credits`, free, no credit cost): returned `{"total": 15100.0}`. **Auth header: `X-TOKEN: <key>`** (not `Authorization` or `x-api-key` — different convention from Blitz). No MCP wrapper — call directly via HTTP. Company search: `POST .../v1/companies`. |
| **listbuild skill** (`.claude/skills/listbuild/`) | ✅ Adopted 2026-09-29; **mandatory for sourcing** | Python pipeline over Blitz -> Clay -> DiscoLike with filter canary, lossless sharding under the 50k cap, SQLite ledger dedup (LinkedIn URL only), title guard, ICP-fit split. Configs in `sourcing/listbuild/config/`. See its `SKILL.md` and the root `CLAUDE.md`. |
| **Clay public API** (`https://api.clay.com/public/v0`, header `clay-api-key`) | ⚠️ Key set; **quota exhausted until 2027-01-01** | Env var `CLAY_API_KEY`, workspace 770250. Used by listbuild for bulk people/company search. On 2026-09-29: 999,953 of 1,000,000 results used, 47 left, resets 2027-01-01. listbuild skips it and reports it under "PROVIDER LIMITS HIT". Separate from the Clay MCP (row above), which still works for small targeted pulls. Person `location_country` spells Czech Republic / North Macedonia, while company `country_name` wants Czechia / Macedonia. |
| **DiscoLike** (`https://api.discolike.com`) | ⚠️ Key valid; **account overdrawn (~ -$4)** | Env var `DISCOLIKE_API_KEY`. $0.0035 per contact; the most expensive layer in listbuild. Cannot apply exclusion lists, so ~40% of paid rows overlap free layers. V1 estimate 2026-09-29: ~263,786 contacts, ~$923 gross. Always run listbuild with `--discolike-cap-usd 0` until the user tops up and approves an estimate. Spend truth is `GET /usage -> billing_events`. |
| **HeyReach** (`mcp__Algo__*`) | ✅ Live, functional | Campaign/lead/list management for Algo Acquisition's own HeyReach workspace (126779). Used for all push/list/campaign operations — see `heyreach-campaign-map.md`. |
| **tracking_clients** (`mcp__tracking_clients__*`) | ✅ Live, functional | Algo's internal client/ICP/sourcing-config/campaign tracking system. Used for `list_icp_configs`, `create_sourcing_config`, etc. |
| **GitHub** (`mcp__github__*`) | ✅ Live, scoped | Scoped to `moeez-coder/algosourcing` for this session. Used for repo operations (this file is part of that). |
| Gmail / Google Calendar / Google Drive / Slack | ✅ Connected, not core to sourcing | Available if a sourcing session needs to check the client Slack channel, send something, or read a doc, but not part of the Blitz/Clay → HeyReach pipeline itself. |
| Prospeo | ❓ Unconfirmed direct; reachable via Cold IQ | No standalone Prospeo MCP tool or env var is present. Cold IQ resells it at `/v1/prospeo/*` once its key/header are confirmed — may make a separate direct Prospeo key unnecessary; compare cost/simplicity once Cold IQ is working before setting up a direct key too. |

### Blitz ignores unsupported filters (2026-09-29 finding, supersedes the 2026-09-17 "data-integrity bug")

Re-tested 2026-09-29 while adopting listbuild. **Blitz does not reject a filter
it does not support; it drops it silently and answers as if it were not
there.** An empty or fully ignored filter set returns the whole database
(454,021,881 people / 68,363,495 companies).

That explains the 2026-09-17 incident:
- `company.linkedin_url` is **not a Company Search filter**. Querying three
  different URLs all returned "Forbes" because the filter was dropped and
  Forbes is the first row of the unfiltered result (today it returns Google).
  Looking up a company by LinkedIn URL is done with `/v2/enrichment/company`,
  which returns the right company.
- The ~9x jump in "total_results" and the 84% of never-seen companies are
  consistent with a people-search filter being ignored in that exhaustive
  fetch, not with bad data in Blitz.
- **Correction:** the 2026-09-17 note called No Brothers, House of Facility
  and Lupa Hire non-staffing firms. No Brothers and Lupa Hire **are**
  staffing/recruitment firms.

What prevents a repeat (all automatic in listbuild):
- A **filter canary** before every preview and run: one single-filter query
  per filter; if any count equals the unfiltered total, the run aborts with
  `FilterIgnored`.
- The domain-join stage rejects any enrichment response whose LinkedIn URL
  does not match the one requested, and reports it.
- A shard-partition gap above 10% is reported as a notice.

**Vertical 1's held-back complete-TAM batch (60,772 people from 2026-09-17)
stays unpushed**; it was built without these checks. The replacement is a
listbuild run with `sourcing/listbuild/config/v1_staffing_recruitment.yaml`
(preview 2026-09-29: ~122,984 core contacts + ~50,020 in keyword-gated
industries, canary passed), imported with `algo_bridge.py import`.

## What this means practically (master session or individual session)

- **Sourcing runs through listbuild** (Blitz -> Clay -> DiscoLike); AI Ark
  and Cold IQ add enrichment and gap-fill afterwards. Clay public-API quota
  and DiscoLike balance are the current limits (rows above). Use every tool, per `pipeline.md`'s "Data philosophy" section: the user
  wants maximum data coverage, sequencing tools cheap → expensive but never
  skipping a more expensive tool just to save cost. Prospeo direct is
  unconfirmed; Cold IQ resells it.
- Before calling Blitz, confirm the key is actually in *your* session's
  environment first (`env | grep -q '^BLITZ_API_KEY='`) — don't assume it's
  present just because this file says Blitz is live overall; a session
  started before the key was added won't have it.
- **Don't silently skip Cold IQ/Prospeo and call it done** — if a task
  depends on them, say so explicitly (in the Progress Log and to the user)
  rather than quietly sourcing Clay/Blitz-only and presenting it as the full
  intended pipeline.
- Before starting real sourcing work, a session should re-check this file
  and, if it looks stale (a key now present that wasn't before, a tool
  missing that used to work), update it and note the change — same
  shared/read-mostly treatment as the other top-level `sourcing/*.md` files
  per `COORDINATION.md`.
