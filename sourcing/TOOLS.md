# Tooling Access — What's Actually Available

Audited 2026-09-08. Re-verify this list periodically (tool access can change
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
| **Blitz** (`https://api.blitz-api.ai`) | ✅ Live, functional (confirmed 2026-09-08) | `BLITZ_API_KEY` is now set at the environment level. **Verified working** via `GET /v2/account/key-info` from a fresh session that inherited the variable: valid, 14,922,558 records remaining (resets 2026-10-07), 50 req/sec rate limit, plan "Agency - Premium", full endpoint access (waterfall ICP search, people search, employee finder, company search, email/phone/domain↔LinkedIn/company-distribution enrichment, jobs search, account/key-info). There is still no MCP wrapper tool for it — call it directly via HTTP (curl or similar) with the `x-api-key` header, reading `BLITZ_API_KEY` from the environment. Note: a session only sees this env var if its container started *after* the variable was added — check with `env | grep -q '^BLITZ_API_KEY='` before assuming it's present (this hub session, for instance, was already running when the key was added and does not have it as of 2026-09-08). `search_blitz_api_the_api_engine_for` / `query_docs_filesystem_...` remain docs-only tools (endpoint reference), separate from actually calling the API. |
| **Cold IQ** (`https://api.coldiq.com`) | ⚠️ Identified 2026-09-08, key not yet set | **Not a data source itself — a GTM data marketplace/proxy.** One API key, unified credits, resells ~39 provider groups under `/v1/<provider>/*`: `apollo`, `prospeo`, `fullenrich`, `findymail`, `wiza`, `icypeas`, `pdl`, `sumble`, `linkupapi`, `companyenrich`, **`blitzapi`** (yes — Blitz is itself resold here), `builtwith`, `openmart`, `influencers-club`, plus signals (`signalbase`, `predictleads`, `theirstack`, job-posting scrapers), SEO/web (`dataforseo`, `exa`, `serper`, `jina`), ad/scraper groups (Meta/Google/LinkedIn ads, Google Maps, Reddit, Twitter), and BYOK-free sending/CRM (`instantly`, `lemlist`, `attio`, `unipile`). Also bundles a native `ai-ark` dataset group under its own umbrella — **but the user's AI Ark access is a separate, standalone account, not through Cold IQ** (see AI Ark row below; don't conflate the two). Repo: https://github.com/Cold-IQ/coldiq-marketplace-skills (cloned read-only to `/home/user/cold-iq/coldiq-marketplace-skills` for reference). Env var: `COLDIQ_API_KEY`. **Auth header is UNVERIFIED against the live API** — two candidates, `X-KEY: <key>` (their own docs' best guess, since they resell Prospeo which uses `X-KEY`) or `Authorization: Bearer <key>`; test both against the free `GET /dashboard/credits` once a key exists and record which works here. Also ships **17 Claude Code skills** (`tam-scoring`, `icp-personas`, `signal-detection`, `contact-enrichment`, `list-dedup`, `apollo-search`, etc.) that closely mirror this repo's own `pipeline.md` workflow — installable as a real Claude Code plugin (`claude plugin marketplace add Cold-IQ/coldiq-marketplace-skills` then `claude plugin install coldiq@coldiq --config apiKey=...`), which is a separate decision from just setting the env var for raw API calls — ask the user before installing a third-party plugin. |
| **AI Ark** (`https://api.ai-ark.com/api/developer-portal`) | ✅ Live, functional (confirmed 2026-09-10) | **Standalone product, not via Cold IQ** (the user has a direct AI Ark account — confirm this distinction before assuming Cold IQ's bundled `ai-ark` group covers it). 400M+ people / 70M+ company profiles, real-time verified emails/mobile numbers, lookalike/signal-based company discovery, personality analysis. Docs: https://docs.ai-ark.com/. Env var: `AIARK_API_KEY` — confirmed present and working via `GET /v1/payments/credits` (full path `https://api.ai-ark.com/api/developer-portal/v1/payments/credits`, free, no credit cost): returned `{"total": 15100.0}`. **Auth header: `X-TOKEN: <key>`** (not `Authorization` or `x-api-key` — different convention from Blitz). No MCP wrapper — call directly via HTTP. Company search: `POST .../v1/companies`. |
| **HeyReach** (`mcp__Algo__*`) | ✅ Live, functional | Campaign/lead/list management for Algo Acquisition's own HeyReach workspace (126779). Used for all push/list/campaign operations — see `heyreach-campaign-map.md`. |
| **tracking_clients** (`mcp__tracking_clients__*`) | ✅ Live, functional | Algo's internal client/ICP/sourcing-config/campaign tracking system. Used for `list_icp_configs`, `create_sourcing_config`, etc. |
| **GitHub** (`mcp__github__*`) | ✅ Live, scoped | Scoped to `moeez-coder/algosourcing` for this session. Used for repo operations (this file is part of that). |
| Gmail / Google Calendar / Google Drive / Slack | ✅ Connected, not core to sourcing | Available if a sourcing session needs to check the client Slack channel, send something, or read a doc, but not part of the Blitz/Clay → HeyReach pipeline itself. |
| Prospeo | ❓ Unconfirmed direct; reachable via Cold IQ | No standalone Prospeo MCP tool or env var is present. Cold IQ resells it at `/v1/prospeo/*` once its key/header are confirmed — may make a separate direct Prospeo key unnecessary; compare cost/simplicity once Cold IQ is working before setting up a direct key too. |

## What this means practically (master session or individual session)

- **Clay, Blitz, and AI Ark are all live** as of 2026-09-10 — use all three,
  not just one, per `pipeline.md`'s "Data philosophy" section: the user
  wants maximum data coverage, sequencing tools cheap → expensive but never
  skipping a more expensive tool just to save cost. **Cold IQ is identified
  but not yet keyed/verified; Prospeo direct is unconfirmed** — don't assume
  either works, but fold them into the waterfall the moment they are (Cold
  IQ in particular adds a lot of coverage — Apollo, additional
  enrichment/verification providers, signal feeds — once its key and auth
  header are confirmed).
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
