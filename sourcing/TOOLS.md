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
| **Blitz** (`mcp__Blitz-API__*`) | ⚠️ Docs-only, no execution | `search_blitz_api_the_api_engine_for` and `query_docs_filesystem_...` search/read Blitz's *documentation* — they do not call the live API. Blitz itself is a real REST API at `https://api.blitz-api.ai` (e.g. `/v2/search/waterfall-icp-keyword`, `/people-search/find-people`), authenticated via an `x-api-key` header (or `BLITZ_API_KEY` env var for its official SDKs). **No key present in this environment as of 2026-09-08.** Once a key is set at the environment level (see above), a session can call these endpoints directly via HTTP (curl or similar) — there is no MCP wrapper tool for execution, so this is a raw API integration, not a tool call. |
| **Cold IQ** | ❌ Not found | No MCP server, tool, or env var under this name exists anywhere in this session as of 2026-09-08. Unknown what this actually is (a platform? an API? possibly a name mix-up with something else). **Needs the user to clarify what it is before it can be connected.** |
| **HeyReach** (`mcp__Algo__*`) | ✅ Live, functional | Campaign/lead/list management for Algo Acquisition's own HeyReach workspace (126779). Used for all push/list/campaign operations — see `heyreach-campaign-map.md`. |
| **tracking_clients** (`mcp__tracking_clients__*`) | ✅ Live, functional | Algo's internal client/ICP/sourcing-config/campaign tracking system. Used for `list_icp_configs`, `create_sourcing_config`, etc. |
| **GitHub** (`mcp__github__*`) | ✅ Live, scoped | Scoped to `moeez-coder/algosourcing` for this session. Used for repo operations (this file is part of that). |
| Gmail / Google Calendar / Google Drive / Slack | ✅ Connected, not core to sourcing | Available if a sourcing session needs to check the client Slack channel, send something, or read a doc, but not part of the Blitz/Clay → HeyReach pipeline itself. |
| Prospeo | ❓ Unconfirmed | Referenced in the existing Vertical 1 sourcing config's `sourcing_instructions` ("Use prospeo, use blitz api...") but no Prospeo MCP tool or env var is present in this session either. Same treatment as Blitz/Cold IQ — don't assume it works, confirm before relying on it. |

## What this means for an execution session, practically

- **Use Clay** as the primary sourcing tool right now — it's the only one of
  the three named tools (Blitz, Clay, Cold IQ / Prospeo) that's actually
  callable today.
- **Don't silently skip Blitz/Cold IQ/Prospeo and call it done** — if a task
  depends on them, say so explicitly (in the Progress Log and to the user)
  rather than quietly sourcing Clay-only and presenting it as the full
  intended pipeline.
- Before starting real sourcing work, a session should re-check this file
  and, if it looks stale (a key now present that wasn't before, a tool
  missing that used to work), update it and note the change — same
  shared/read-mostly treatment as the other top-level `sourcing/*.md` files
  per `COORDINATION.md`.
