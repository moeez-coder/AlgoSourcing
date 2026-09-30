# Vertical 3 — M&A (Mergers & Acquisitions)

## Status

Live vertical. **Confirmed by the user (2026-09-09): use the "M&A - SEPT -
..." labeled campaigns** (created by Joe, 2026-09-06) — see
`../heyreach-campaign-map.md`, Vertical 3 section. The earlier "USA | ... |
Vertical 3" Sept-2 set is not in use. No tracking-clients ICP config /
sourcing config exists yet for this vertical in the new system — only raw
HeyReach campaigns.

## Target companies (draft — confirm/refine before large sourcing runs)

- M&A advisory firms, business brokerages, investment banks / boutique
  advisory shops doing sell-side/buy-side M&A work, and similar deal-advisory
  firms that rely on outbound BD to win mandates.
- Apply shared filters from `../icp-overview.md`: revenue ≥ $1M, headcount ≥
  10, HQ in USA/UK/Europe with founders locally present.
- No `fixed_signals` defined yet — candidate signals to consider: firm
  announcing a new fund/practice area, senior hire (new MD/Partner), recent
  closed deal announcement (proof of active dealflow), office expansion.

## Target personas / titles (draft, mirrored from Vertical 1's buyer profile)

**Apply the shared seniority filter in `../icp-overview.md`** ("Seniority
filter" section) — Director-and-above: Owner/Founder/Partner, C-suite,
President/Managing Director, Director, VP-and-above in Sales/BD/Growth/
Revenue/Marketing/New Business/Partnerships. Worth noting for this vertical
specifically: "Managing Director" is often the *most senior* operating title
at a boutique M&A advisory shop (not mid-level like a corporate "Director"),
so it's squarely in scope here. Still apply the exclude list (Associate,
Analyst, etc.) as normal — those are genuinely junior, non-decision-making
titles at advisory firms too.

- **Job titles (draft):** Managing Partner, Managing Director, Director,
  Founder, CEO, President, Head of Business Development, VP Origination/Deal
  Sourcing
- Drafted from Algo's stated buyer profile; not yet validated specifically for
  the M&A-advisory vertical. Refine once real results come back. Use
  exact/bracket matching per the shared rule's "Matching method," not loose
  keyword search.

## To do before next sourcing run

- [ ] Create a proper `icp_config` + `sourcing_config` in tracking-clients for
      this vertical (mirror the Vertical 1 structure)
- [ ] Confirm/replace the draft persona list above
- [x] ~~Confirm whether to keep feeding the Sept-6 generation campaigns or
      the user wants a fresh relaunch~~ — resolved 2026-09-09: use the
      "M&A"-labeled Sept-6 campaigns (Joe's).
- [x] ~~Resume vs. fresh Open Check campaign~~ — user confirmed 2026-09-09:
      reuse Open Check 587156, don't create a fresh one. A direct
      `resume_campaign` call failed twice with a 500 (see
      `../heyreach-campaign-map.md` push targets) — **resolved 2026-09-10:
      don't call resume_campaign at all, just push leads directly.**
      Vertical 1 confirmed this on the identical FINISHED-campaign situation
      (567476): pushing leads alone flips FINISHED → IN_PROGRESS
      automatically, no resume call needed.

## Dedup ledger

`sourcing/data/vertical-3-ma/contacted_ledger.csv` exists (header row only as
of 2026-09-08, no runs yet). Check it before every push, update it after
every push — see `../pipeline.md`, "The contacted ledger."

## TAM (Total Addressable Market) — append-only, newest entry on top

Total companies matching this vertical's ICP filters, and total people
matching its persona/title filters across those companies — not the sample
actually sourced/pushed. See `../pipeline.md`, "TAM entry format."

### 2026-09-30 12:43 UTC — individual session (listbuild full-universe rerun, cap500 config)
- Companies matching ICP filters: core industry Investment Banking, headcount 10-500, at **73,716 companies**
  exported (companies file); of these, people-bearing fit-industry companies number in the low thousands after the
  cap (see top companies below). Method: `listbuild run`, `config/v3_ma_advisory.yaml` with `employee_count_max: 500`
  added (user decision 2026-09-29); same 43 US/UK/Europe HQ countries, revenue >= $1M, headcount 10-500; canary
  passed; Clay skipped (quota exhausted until 2027-01-01, 37 results left of 1,000,000).
- People matching persona/title filters: **351,269** director-plus-title people swept from Blitz (174 shards, 359,589
  fetched = 96%), after title guard 329,352 pass; ICP fit split: **11,192 main list** (core industry, Investment
  Banking, headcount <= 500), 26,777 keyword-gated candidates (Business Consulting/Management Consulting/Financial
  Services + M&A keywords), 6,341 unverified (industry unknown), 304,308 unfit (mostly consulting firms without M&A
  keywords, or outside headcount cap).
- Notes: **much cleaner than the DRAFT run.** Main list top companies are genuine boutique/mid-size advisory shops —
  Leerink Partners (143), Capstone Partners (127), SunTrust Robinson Humphrey (118), ROTH Capital Partners (114),
  Daiwa Capital Markets Europe (103), Deutsche Numis (103), Solomon Partners (102), Peel Hunt (81), MarshBerry (77) —
  no single mega-bank dominates (vs. Deutsche Bank = 30% of the prior draft's main list). Country split: US 6,986
  (62%), GB 1,375 (12%), FR 692, IT 370, ES 306, DE 247.

### 2026-09-29 10:32 UTC — master session (listbuild full-universe run, DRAFT config)
- Companies matching ICP filters: core industry Investment Banking at **1,335 companies** in the main list, plus
  **~3,379** Financial Services / Business Consulting / Management Consulting companies that pass the M&A keyword
  gate (M&A advisory, sell-side, buy-side, business broker, corporate finance / transaction advisory, exit
  planning). Blitz company sweep saw ~82,448 companies across all four labels. Method: `listbuild run`,
  `config/v3_ma_advisory.yaml` (DRAFT); 43 US/UK/Europe HQ countries, revenue >= $1M, headcount >= 10;
  canary passed.
- People matching persona/title filters: **~857,290** director-plus people across the four labels (395 shards,
  821,918 returned = 96%), 801,016 unique after LinkedIn-URL dedup; 716,606 pass the title guard. Split: **24,272
  main list** (Investment Banking), 106,006 keyword-gated candidates, 4,622 unverified; 580,653 held back
  (Financial Services / consulting firms without M&A keywords).
- Notes: **low precision on this draft.** Main list: Deutsche Bank alone is 7,417 people (30%), plus asset managers
  (Empower, AllianceBernstein); only 10,377 main-list people are at companies of <= 200 staff. Candidates are
  dominated by enterprises whose descriptions mention M&A (Fidelity 10,718, Accenture 7,941, KPMG, EY-Parthenon,
  New York Life, Wells Fargo). An upper headcount cap and/or the "acquirers" framing (verticals-portfolio.md) is
  needed before any push.


## Progress Log (append-only — newest entry on top; do not edit or delete other sessions' entries)

### 2026-09-30 12:43 UTC — individual session — FULL-UNIVERSE LISTBUILD RERUN (CAP500 CONFIG), NO PUSH
- User decision (2026-09-29): keep headcount cap at <= 500 and re-run; advisors-vs-acquirers framing not yet decided
  (left as-is for now — config still targets M&A advisory firms, not acquirers).
- Config change: added `employee_count_max: 500` to `sourcing/listbuild/config/v3_ma_advisory.yaml`, committed and
  pushed to main (commit db85a0e) before running.
- Sourced: 73,716 companies / 44,310 people exported (11,192 main + 26,777 candidates + 6,341 unverified).
- Files: sourcing/data/vertical-3-ma/people/2026-09-30_1243_listbuild-listbuild-full-universe-cap500.csv (main),
  `..._candidates.csv`, `..._unverified.csv`; companies/2026-09-30_1243_listbuild-listbuild-full-universe-cap500.csv;
  reports/2026-09-30_1243_listbuild-listbuild-full-universe-cap500_cost_report.md.
- Pushed to HeyReach: none — this is a preview/review run per the master-session model (listbuild preview -> user
  approval -> run -> import -> review -> push only when approved). Showing the user the main file next for a push
  decision.
- Checks: seeds rebuilt from all verticals' ledgers (67,123 contacted people) before the run; Blitz filter canary
  passed; title guard dropped 21,909 sub-director rows; 0 people purged as already-contacted (excluded=304 were
  merges within this run's own shards, not ledger hits — seed exclusion ran at 67,123 keys with 0 subsequent purges
  in consolidate). Clay layer skipped cleanly (quota exhausted, reported per the "every provider" rule). DiscoLike
  has no bucket for these industries, skipped as before.
- See TAM entry above for the company/precision detail (top companies now genuine boutique/mid-size shops, not one
  mega-bank).

### 2026-09-29 10:32 UTC — master session — FULL-UNIVERSE LISTBUILD RUN (DRAFT CONFIG), NO PUSH
- Sourced: 75,339 companies / 134,900 people exported (24,272 main + 106,006 candidates + 4,622 unverified).
- Files: sourcing/data/vertical-3-ma/people/2026-09-29_1032_listbuild-full-universe-draft.csv (main),
  `..._candidates_part01..02.csv`, `..._unverified.csv`; companies/2026-09-29_1032_listbuild-full-universe-draft.csv;
  reports/2026-09-29_1032_listbuild-full-universe-draft_cost_report.md.
- Pushed to HeyReach: none. Not push-ready: the config is a DRAFT and precision is low (see TAM entry).
- Checks: 0 duplicate LinkedIn URLs, 0 people already in any contacted ledger (only 231 V3 prospects were ever
  seeded), 0 title-guard fails, 0 client staff; 1,075 people dropped at placeholder employers ("Family Office",
  "Undisclosed", "Self-Employed Contractor", "Private Company"). Main list: US 52%, DE 31% (Deutsche Bank), GB 5%.
- Notes for the user: decide (1) M&A advisors vs acquirers, and (2) an upper headcount cap (<= 1,000 leaves 13,230
  main-list people; <= 500 leaves 11,804; <= 200 leaves 10,377). Re-cut the config, then re-run: the Blitz pull is
  free on the flat plan and takes ~35 min.

