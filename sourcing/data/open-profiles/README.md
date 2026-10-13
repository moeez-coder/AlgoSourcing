# Open-profiles master list (2026-10-13): qualification for Algo outreach

Source: `open-profiles-master-2026-10-13.csv` shared by the user on Discord (104,386 LinkedIn profiles confirmed
"open" across 35 HeyReach open-profile lists: IT / Cyber 35.6k, Recruitment 29.3k, Finance / M&A 15.3k,
Verticals 1-4 14.8k, Other 4.3k). Checked by the master session against the shared ICP and every vertical's
listbuild config. **Nothing was pushed to HeyReach.**

Committed file: `2026-10-13_1430_open-profiles-master_qualified.csv` (QUALIFIED and QUALIFIED - review rows only,
36,631). The full 104k-row result including every "not qualified" row and its reason was kept out of the repo
(79 MB); re-create it with the method below if needed.

## Method
1. **Person, from the file:** Director-and-above title guard (`seniority.py`) on `position` (headline as fallback);
   person location in the 43 US/UK/Europe codes (unclear metro names resolved with Blitz's location).
2. **Company, via Blitz:** `/v2/enrichment/person` for the current company (91,395 lookups), then
   `/v2/enrichment/company` for each of 58,767 unique companies (industry, HQ, employees on LinkedIn, type, about /
   specialties). Responses for a different company than requested were discarded.
3. **Fit per vertical:** company industry in a vertical's core labels, or in its keyword-gated labels with a keyword
   in the company's about / specialties; company HQ in the 43 codes; employees on LinkedIn inside the vertical's band
   (>= 10; <= 500 where the config caps it; 2-9 for V1b); not Nonprofit / Government / Educational; not an Algo client
   (`dnc_clients.csv`).
4. **Revenue >= $1M** can only be confirmed when the company is already in one of our filtered listbuild sweeps
   (`revenue_check = verified`); otherwise `unverified`.
5. **Status:** `QUALIFIED` = core industry + revenue verified; `QUALIFIED - review` = passes everything else but
   revenue is unverified or the match is keyword-gated; `already contacted` = in a contacted ledger;
   `not qualified` = with a reason.

## Results

| Status | People |
|---|---|
| QUALIFIED | **21,772** |
| QUALIFIED - review | 14,859 (core industry, revenue unverified 10,110; keyword-gated 4,749) |
| already contacted (in our ledgers) | 5,576 |
| not qualified | 62,179 |

| Vertical | QUALIFIED | review | already contacted |
|---|---|---|---|
| V1 Staffing & Recruitment | 9,421 | 1,694 | 2,032 |
| V2 Marketing | 5,387 | 402 | 532 |
| V3 M&A | 704 | 538 | 5 |
| V4 B2B SaaS | 6,220 | 974 | 2,870 |
| V1b Boutique exec search | 3 | 3,083 | 30 |
| V5 IT services | 37 | 7,627 | 32 |
| V6 Life-sciences services | 0 | 39 | 1 |
| V7 Nearshore dev | 0 | 3 | 1 |
| V8 Fractional / consulting | 0 | 146 | 0 |
| V9 PEO / EOR / HR tech | 0 | 353 | 73 |

V5 and V1b sit mostly in "review" only because no listbuild sweep has run for them yet, so revenue is unverified.

**Why the 62,179 do not qualify:** industry outside every vertical 18,567 (top: Financial Services 3,776, Business
Consulting 3,180, VC / PE 1,555, HR Services 1,228, Investment Management 1,125, Insurance 788); company too small
(mostly 1-9 employees on LinkedIn) 16,402; title below Director 11,704; no current company 5,654; not found in Blitz
4,011; company HQ outside US/UK/Europe 2,823; nonprofit / government / education 1,470; person outside US/UK/Europe
1,446; works at an Algo client 58; company not found 44.

## Notes
- These people are already known to be open profiles, so Open Check (which is failing on lapsed Sales Navigator
  seats, see `heyreach-campaign-map.md`) is not needed for them. Routing them anywhere is the user's decision:
  the shared rules say Open Profile campaigns are filled by Clay only.
- Before any push: re-check against all contacted ledgers (other sessions may have pushed since) and
  `dnc_clients.csv`, and log the push in the vertical's ledger and Progress Log.
