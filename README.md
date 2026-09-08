# AlgoSourcing

Algo Acquisition's own BD sourcing pipeline: find companies and decision-makers
via Clay (and Blitz, once connected), then push them into HeyReach outbound
campaigns. This isn't a client project — it's Algo Acquisition prospecting for
itself.

## Structure

Everything lives under [`sourcing/`](sourcing/):

| File | What it's for |
|---|---|
| [`sourcing/README.md`](sourcing/README.md) | Full index and key IDs — start here for details |
| [`sourcing/COORDINATION.md`](sourcing/COORDINATION.md) | How multiple Claude sessions (one per vertical) work this repo without colliding |
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

One Claude Code session runs per vertical (sometimes per segment within a
vertical). Each sources companies and people, saves the raw output as CSVs
under `sourcing/data/<vertical>/`, checks/updates that vertical's
`contacted_ledger.csv` so nobody gets contacted twice, then pushes leads into
that vertical's **Con Req** and **Open Check** HeyReach campaigns (never Con
Acc or Open Profile — those fill automatically). New verticals/segments get
their groundwork laid in a planning session first, then handed to a dedicated
execution session — see `sourcing/COORDINATION.md`.

## Status / open items

- Clay is fully connected. Blitz is documentation-access only right now (no
  API key configured) — see `sourcing/TOOLS.md`.
- Cold IQ is referenced by the user but not yet identified/connected.
- Tracked in pull request [#1](https://github.com/moeez-coder/AlgoSourcing/pull/1).
