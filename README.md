# AlgoSourcing

Algo Acquisition's own BD sourcing pipeline: find companies and decision-makers
via Clay and Blitz, then push them into HeyReach outbound campaigns. This
isn't a client project — it's Algo Acquisition prospecting for itself.

## Structure

Everything lives under [`sourcing/`](sourcing/):

| File | What it's for |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Rules every Claude session loads automatically (read order, sourcing method, dedup, push and key rules) |
| [`.claude/skills/listbuild/`](.claude/skills/listbuild/SKILL.md) | The sourcing engine every session uses: Blitz → Clay → DiscoLike, cheapest first, with dedup against every contacted ledger |
| [`sourcing/README.md`](sourcing/README.md) | Full index and key IDs — start here for details |
| [`sourcing/COORDINATION.md`](sourcing/COORDINATION.md) | Session model: one session per vertical does its own sourcing, the master session guides and checks; every session works on `main` |
| [`sourcing/TOOLS.md`](sourcing/TOOLS.md) | What's actually connected right now (Clay, Blitz, HeyReach, etc.) and where API keys belong |
| [`sourcing/icp-overview.md`](sourcing/icp-overview.md) | Shared targeting criteria across all verticals (revenue, headcount, geography) |
| [`sourcing/verticals/`](sourcing/verticals/) | One file per vertical: target companies, personas, status |
| [`sourcing/heyreach-campaign-map.md`](sourcing/heyreach-campaign-map.md) | Which HeyReach campaign ID to push leads into, per vertical |
| [`sourcing/pipeline.md`](sourcing/pipeline.md) | The actual sourcing → dedup → push workflow |
| [`sourcing/data/`](sourcing/data/) | Every sourcing run's output (companies/people CSVs) and each vertical's contacted-leads ledger |

## Current verticals

1. **Staffing & Recruitment** — live, most mature
2. **Marketing companies** — live
3. **M&A** — live

Shared filters across all three: revenue ≥ $1M, headcount ≥ 10, HQ in
USA/UK/Europe with founders locally present.

## How this works day to day

Each vertical has its **own Claude session that does its sourcing**: it sizes the market with the listbuild
skill, runs the full build once you approve, saves the files under `sourcing/data/<vertical>/`, and (once you
approve) pushes leads into that vertical's **Con Req** and **Open Check** HeyReach campaigns, updating its
`contacted_ledger.csv` so nobody is contacted twice. Con Acc and Open Profile fill automatically via Clay.

The **master session** ("ALGO BD Main") is the guide and checker: it owns the shared rules and tools and makes
sure every vertical's work is correct (dedup across verticals, client do-not-contact list, ICP and seniority
rules, healthy campaigns). **Every session works on the `main` branch.** See `sourcing/COORDINATION.md`.

## Status / open items

- **Sourcing runs through the listbuild skill** since 2026-09-29 (see
  `CLAUDE.md`). Preview first, approve, then run; outputs land in
  `sourcing/data/<vertical>/`.
- Blitz, AI Ark and Cold IQ keys are live. The Clay public API's quota is used
  up until 2027-01-01, and DiscoLike needs a top-up before any paid pull. See
  `sourcing/TOOLS.md` for details.
- The 2026-09-17 "Blitz data bug" turned out to be Blitz ignoring an
  unsupported filter; listbuild now checks every filter before running.
- Tracked in pull requests [#1](https://github.com/moeez-coder/AlgoSourcing/pull/1) and [#2](https://github.com/moeez-coder/AlgoSourcing/pull/2), both merged. Further pushes to this branch will open a new PR automatically.
