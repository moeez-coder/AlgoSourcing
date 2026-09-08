# AlgoSourcing

Algo Acquisition's own BD sourcing pipeline: find companies and decision-makers
via Clay and Blitz, then push them into HeyReach outbound campaigns. This
isn't a client project — it's Algo Acquisition prospecting for itself.

## Structure

Everything lives under [`sourcing/`](sourcing/):

| File | What it's for |
|---|---|
| [`sourcing/README.md`](sourcing/README.md) | Full index and key IDs — start here for details |
| [`sourcing/COORDINATION.md`](sourcing/COORDINATION.md) | Master/individual session model — how the primary working session and occasional per-vertical sessions share this repo without colliding |
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

One **master session** does most of the actual work across all three
verticals directly: sourcing companies and people, saving raw output as CSVs
under `sourcing/data/<vertical>/`, checking/updating each vertical's
`contacted_ledger.csv` so nobody gets contacted twice, tracking TAM, and (once
approved) pushing leads into each vertical's **Con Req** and **Open Check**
HeyReach campaigns (never Con Acc or Open Profile — those fill
automatically). The user opens a separate, **individual session for one
vertical** only occasionally — to fine-tune something or fix an issue in that
vertical specifically — not as the default way work gets done. See
`sourcing/COORDINATION.md` for the full model.

## Status / open items

- Clay and Blitz are both fully connected and live as of 2026-09-08 — see
  `sourcing/TOOLS.md` for confirmed API access details (Blitz has no MCP
  wrapper; it's called directly via HTTP using an environment-level
  `BLITZ_API_KEY`).
- Cold IQ is referenced by the user but not yet identified/connected.
- Tracked in pull requests [#1](https://github.com/moeez-coder/AlgoSourcing/pull/1) and [#2](https://github.com/moeez-coder/AlgoSourcing/pull/2), both merged. Further pushes to this branch will open a new PR automatically.
