# Multi-Session Coordination

**Updated 2026-09-08 — supersedes the earlier "hub session does groundwork /
execution session does sourcing" split.** The user now wants most actual
sourcing work done in one primary session, with individual per-vertical
sessions used only occasionally, for fine-tuning or troubleshooting. These
rules exist so that primary session and any occasional individual sessions
don't collide, duplicate pushes, or lose each other's work.

**Check `pipeline.md`'s "Current phase" banner before pushing anything to
HeyReach** — as of 2026-09-08 all verticals are in a testing/priming phase
with pushes paused pending the user's final approval. This applies to every
session, master or individual, across every vertical.

## Master / individual session model

- **Master session** (this one — the one the user is primarily working in;
  currently `session_019W2MEyTk1GwcVjEfcm7j7v`): does most of the actual work,
  across **all** verticals directly — TAM sizing, sourcing companies/people
  via Blitz/Clay, saving CSVs, ledger checks/updates, Progress Log entries,
  and (once the testing/priming phase lifts) HeyReach pushes. Not restricted
  to one vertical's files — free to read/write across
  `sourcing/verticals/*`, `sourcing/data/*/**` for whichever vertical the
  user is asking about. Also still does the groundwork role from the old
  model: laying groundwork for a new vertical/segment (ICP file, HeyReach
  campaign map entry, data folders + ledger, creating HeyReach campaigns via
  the `heyreach-vertical-launch` skill if needed) before an individual
  session for it would ever be opened.
- **Individual session** (opened by the user directly in Claude Code, only
  when something needs fine-tuning or isn't going right in one specific
  vertical/segment — not the default way work gets done anymore): scoped to
  **one vertical**, same restricted rules as before — stay inside that
  vertical's `sourcing/verticals/<slug>.md` and
  `sourcing/data/<slug>/**`, treat everything else as shared/read-mostly, and
  `git pull` before touching anything, since the master session is likely to
  have pushed new data since the individual session was last opened. It
  should not make ICP-identity-level decisions or create new HeyReach
  campaigns on its own — surface those to the user instead of guessing.

Because the master session does most of the work now, most commits will come
from here — that's expected. An individual session is the exception, spun up
for a specific fix, not a standing per-vertical worker.

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

If the master session and an individual session end up sourcing the same
vertical concurrently (uncommon now that individual sessions are the
exception, but possible if the user opens one to fine-tune something while
also asking the master session to keep working that vertical), `git pull`
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
- Commit and push these changes to the branch so the other session type can
  see them.

## Git conflict handling

Because multiple sessions write to this repo concurrently, expect occasional
merge conflicts, mostly in Progress Log sections. Resolve by keeping both
sessions' entries (Progress Logs are append-only lists — a conflict here is
almost always "both entries are valid, keep both, just reorder"), never by
discarding either side. Do not force-push.
