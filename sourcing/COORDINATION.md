# Multi-Session Coordination

**Updated 2026-09-29 (user decision) — supersedes the 2026-09-08 "master does most of the work" model.**
Each vertical has its own **individual session that does that vertical's sourcing and pushes**. The **master
session is the guide and the checker**: it owns the shared rules, tools and code, and makes sure every
vertical's work is correct and consistent. All sessions work on **`main`** (see "One branch: main").

**Check `pipeline.md`'s "Current phase" banner before pushing anything to HeyReach.** It applies to every
session, and each vertical's push still needs the user's go-ahead.

**Every session sources with the `listbuild` skill** (`.claude/skills/listbuild/SKILL.md`), and the repo-root
`CLAUDE.md` loads automatically with the shared rules.

## Master / individual session model

- **Individual session** (one per vertical, e.g. "Vertical 2 Marketing", "Vertical 4 B2B SaaS initialization"):
  - Does its own vertical's work end to end: listbuild preview (TAM) -> user approval -> run -> `algo_bridge.py
    import` -> review with the user -> push (when approved) -> ledger update -> TAM and Progress Log entries.
  - Stays inside `sourcing/verticals/<its-vertical>.md`, `sourcing/data/<its-vertical>/**` and its own config in
    `sourcing/listbuild/config/`.
  - Does not change the shared ICP, shared code or other verticals on its own. Needs a change there (a bug fix,
    a rule gap)? Make it test-first if it is code, keep it small, and log it prominently in its Progress Log so
    the master session reviews it.
  - Asks the user before creating HeyReach campaigns or resuming a paused campaign.
- **Master session** (`session_019W2MEyTk1GwcVjEfcm7j7v`, "ALGO BD Main"):
  - Owns the shared rules and tools: `CLAUDE.md`, `icp-overview.md`, `pipeline.md`, `TOOLS.md`, this file,
    `verticals-portfolio.md`, `client-base-vertical-analysis.md`, `data/dnc_clients.csv`, the listbuild code and
    `algo_bridge.py`.
  - **Checks that everything works correctly**, across all verticals: every vertical's contacted ledger is on
    `main` and in the exclusion seeds; nobody is contacted twice or at a client; runs used listbuild with the
    current checks; ICP and seniority rules are applied; HeyReach campaigns are healthy (e.g. Con Acc / Open
    Profile actually receiving leads); shared-code changes from individual sessions are correct.
  - Reviews individual sessions' commits and reports problems to the user; fixes shared code and docs itself.
  - Lays the groundwork for a new vertical (portfolio card, config, data folder and ledger, campaign-map entry)
    before its individual session starts, and gives the user the session's starting prompt.
  - Does sourcing for a vertical only when the user asks it to (e.g. the 2026-09-29 full-universe runs).

## Ownership boundaries

- The **master session** may read/write across all of `sourcing/verticals/*`
  and `sourcing/data/*/**` — it isn't scoped to one vertical.
- An **individual session** stays scoped to **one vertical**
  (`vertical-1-staffing-recruitment`, `vertical-2-marketing`, or
  `vertical-3-ma`) for the duration of that session:
  - `sourcing/verticals/<its-vertical>.md` (read + append to Progress Log/TAM)
  - `sourcing/data/<its-vertical>/**` (read + write new files)
- Treat these as **shared, read-mostly** from an individual session (the
  master session can edit them freely as part of its normal work):
  `sourcing/README.md`, `sourcing/icp-overview.md`,
  `sourcing/heyreach-campaign-map.md`, `sourcing/pipeline.md`,
  `sourcing/TOOLS.md`, `sourcing/COORDINATION.md`. If an individual session
  needs a substantive change here (e.g. a new confirmed campaign ID), make
  the edit, but keep it additive/small and mention it prominently in its
  Progress Log entry so the master session notices it on its next pull.
- Never edit another vertical's file from an individual session, and never
  edit another session's existing Progress Log/TAM entries — only append new
  ones. This applies to the master session too when appending alongside
  work an individual session already logged.

## One branch: main (user decision 2026-09-29)

Every session, master or individual, works on **`main`** and pushes only there. Claude Code gives each new
session its own branch by default, so switch before touching anything:
`git fetch origin main && git checkout main && git pull origin main`.
- Pull right before you commit and again before you push (`git pull --no-rebase origin main`); other sessions push
  to `main` all the time. Never force-push, never rebase `main`.
- The old shared branch `claude/algo-acquisition-sourcing-jmos79` and per-session branches such as
  `claude/upbeat-knuth-kwy4n4` are history only: everything on them is on `main`. Do not push to them.
- Why: the V4 session worked on its own branch, so its 14,576-person contacted ledger was invisible to every other
  session's dedup for 8 days.

## Before doing any sourcing or push, in either session type

1. `git pull` (or fetch + check) to get any updates the other session type
   has pushed since you last read this repo. This matters more now, not
   less: the master session may be actively pushing across several verticals
   while an individual session is open for just one of them.
2. Re-read the relevant vertical's file, in particular its Progress Log and
   TAM section, so you know what's already been sourced and what's already
   been pushed to HeyReach.
3. Re-check `heyreach-campaign-map.md` for the current live campaign ID for
   that vertical+stage — statuses drift, and the other session may have
   noted a change there.

## De-duplication — the contacted ledger

Each vertical's dedup source of truth is
`sourcing/data/<vertical>/contacted_ledger.csv` — see `pipeline.md`, "The
contacted ledger" section, for the exact mechanism. In short: check it before
every push, update it immediately after every push, and treat it (not the
per-run people CSVs) as the answer to "have we already reached out to this
person." This is what actually prevents sending the same person a connection
request or open-profile InMail twice.

If two sessions end up sourcing the same vertical concurrently (e.g. the
master session was asked to run it while the vertical's own session is
open), `git pull`
immediately before checking the ledger so you see the other session's latest
pushes, and resolve any ledger merge conflict by keeping both sessions' rows
(never drop a row to resolve a conflict).

## After every sourcing/push run (mandatory), in either session type

- Save the company list and/or people list as new timestamped CSV files under
  `sourcing/data/<that-vertical>/...` — see `pipeline.md` for the naming
  convention and column format. Do this for every run, not just "final"
  batches — partial/exploratory pulls count too, so nothing is lost if the
  session ends unexpectedly.
- Append one Progress Log entry (and a TAM entry, if sizing was done) to that
  vertical's file (format in `pipeline.md`).
- Commit and push these changes to `main` so every other session sees them.

## Git conflict handling

Because multiple sessions write to this repo concurrently, expect occasional
merge conflicts, mostly in Progress Log sections. Resolve by keeping both
sessions' entries (Progress Logs are append-only lists — a conflict here is
almost always "both entries are valid, keep both, just reorder"), never by
discarding either side. Do not force-push.
