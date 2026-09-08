# Vertical 2 — Marketing Companies

## Status

**Confirmed with the user (2026-09-08): Vertical 2 = Marketing companies.**
Live HeyReach campaigns exist (see `../heyreach-campaign-map.md`, Vertical 2
section) but there is **no tracking-clients ICP config or sourcing config yet**
for this vertical in the new system — only raw HeyReach campaigns.

## Target companies (draft — confirm/refine before large sourcing runs)

- Marketing agencies / marketing services companies (e.g. demand gen, paid
  media, branding, PR agencies) that themselves rely on outbound/BD to win
  clients.
- Apply shared filters from `../icp-overview.md`: revenue ≥ $1M, headcount ≥
  10, HQ in USA/UK/Europe with founders locally present.
- No `fixed_signals` defined yet — candidate signals to consider: agency
  hiring burst, new office/market expansion, leadership change (new
  CEO/CRO/Head of Growth), recent funding or acquisition.

## Target personas / titles (draft, mirrored from Vertical 1's buyer profile)

- **Seniority include:** CXO, Director, Vice President, Owner / Partner,
  Founder
- **Job titles (draft):** CEO, Founder, Managing Partner, President, VP
  Sales/Business Development, Head of Growth, Head of New Business
- These are drafted from Algo's own stated buyer profile ("Founders, owners,
  MDs and sales directors at B2B companies that depend on outbound") — not yet
  validated specifically for the marketing-agency vertical. Refine once real
  results come back.

## To do (non-blocking — can proceed with drafts, refine as results come in)

- [ ] Create a proper `icp_config` + `sourcing_config` in tracking-clients for
      this vertical (mirror the Vertical 1 structure) so it's tracked the same
      way
- [ ] Confirm/replace the draft persona list above once real results come back

## Dedup ledger

`sourcing/data/vertical-2-marketing/contacted_ledger.csv` exists (header row
only as of 2026-09-08, no runs yet). Check it before every push, update it
after every push — see `../pipeline.md`, "The contacted ledger."

## TAM (Total Addressable Market) — append-only, newest entry on top

Total companies matching this vertical's ICP filters, and total people
matching its persona/title filters across those companies — not the sample
actually sourced/pushed. See `../pipeline.md`, "TAM entry format."

### 2026-09-08 11:39 UTC — execution-session-vertical-2 (test run)
- Companies matching ICP filters: 13,383 (method: Blitz `POST /v2/search/companies`,
  `total_results` field; filters: `industry.include` = [Marketing and Advertising,
  Advertising Services, Marketing Services, Public Relations and Communications
  Services, Graphic Design], `employee_count.min=10`, `revenue.min=1000000`,
  `hq.country_code` = US + UK + ~40-code Europe list (see run notes below),
  `type.exclude` = [Nonprofit, Government Agency, Educational, Educational
  Institution])
- People matching persona/title filters across those companies: 40,035 (method:
  Blitz `POST /v2/search/people`, `total_results` field, `max_results=1` to
  minimize record spend; same company filters as above, plus `people.job_title.include`
  = [CEO, Founder, Managing Partner, President, VP Sales, Vice President Sales,
  VP Business Development, Vice President Business Development, Head of Growth,
  Head of New Business, Owner, Partner] -- i.e. the *draft* persona list as
  originally written, before the title-matching issue below was discovered)
- Notes: Estimate, not exact -- Blitz's underlying LinkedIn-derived data has known
  gaps/miscategorization (see Progress Log entry same timestamp for detail). The
  13,383/40,035 figures **include very large global agency holding networks
  (Publicis, Omnicom, IPG, WPP-owned shops, etc.) and some mis-tagged ad-tech/martech
  platforms** that do not match the vertical's actual intent ("independent agencies
  that themselves rely on outbound BD") -- true addressable TAM for boutique/independent
  agencies is materially smaller than these headline numbers; see Progress Log for
  the sample-level breakdown that surfaced this. The people TAM was run with the
  *original* draft title list (loose keyword matching), which the same run found to
  overcount significantly (see Progress Log) -- treat 40,035 as an upper bound, not
  a refined estimate. "Founders locally present" (icp-overview.md) is not a
  structured Blitz filter and is not reflected in either count -- both are HQ-country
  filters only.
- Europe country_code list used: US, GB, IE, FR, DE, ES, IT, NL, BE, PT, CH, AT, SE,
  NO, DK, FI, PL, CZ, SK, HU, RO, BG, GR, HR, SI, EE, LV, LT, LU, MT, CY, IS, LI, MC,
  AD, SM, UA, RS, ME, MK, AL, BA, MD -- a judgment call, not confirmed with the user;
  flag if a different Europe boundary (e.g. EU-27 only, or including/excluding
  specific non-EU states) is intended.

## Progress Log (append-only — newest entry on top; do not edit or delete other sessions' entries)

### 2026-09-08 11:39 UTC — execution-session-vertical-2 — TEST RUN, NO PUSH
- Sourced: 12 qualified companies (50 evaluated) / 50 people
- Files: sourcing/data/vertical-2-marketing/companies/2026-09-08_1139_test-run-batch1.csv,
         sourcing/data/vertical-2-marketing/people/2026-09-08_1139_test-run-batch1.csv
- Pushed to HeyReach: none (testing/priming phase — awaiting final approval)
- Push targets re-confirmed live: Con Req 568586 ("US | Con Req | Vertical 2 | Moe
  1.0", IN_PROGRESS, 63,766 total users) and Open Check 568621 ("US | Open Check |
  Vertical 2 | Moe 1.0", IN_PROGRESS but nearly drained — 57,985/63,486 finished,
  only 74 pending + 9 in progress). Still the right IDs per heyreach-campaign-map.md;
  not pushed to.
- Feedback given to user: TAM = 13,383 companies / 40,035 people (see TAM section —
  flagged as an upper-bound estimate, not refined). Pulled a 50-company candidate
  pool via Blitz company-search (industry + headcount≥10 + revenue≥$1M + US/UK/Europe
  HQ); only 12 of 50 were genuinely qualified — the other 38 were global agency
  holding-company networks (Publicis, Omnicom, IPG, WPP-owned shops, etc., 2.5k-40k+
  employees) or mis-tagged ad-tech/martech/events companies (Klaviyo, Criteo, Teads,
  Cannes Lions) that pass the raw ICP filters but don't match the vertical's actual
  intent (independent agencies that themselves run outbound BD). Sourced 50 people
  across the 12 qualified companies using a *revised* title filter after the
  draft persona list's free-text keyword matching proved to overmatch badly (see
  below); flagged 13 of those 50 as likely too junior (BDR/associate-level) despite
  matching "Business Development" as a keyword.
- Notes / judgment calls for the user to weigh in on:
  1. **Persona/title list needs bracket-exact matching for core titles.** Running
     the *draft* list (`VP Sales`, `Vice President Sales`, `VP Business
     Development`, etc.) as free-text keywords returned "Vice President Design",
     "Vice President Analytics", "Vice President People & Experience", "Vice
     President Learning and Development" and similar — Blitz's non-bracketed
     title search appears to match on token overlap ("Vice President") rather
     than the full phrase, not AND-of-the-whole-phrase. It also skewed results
     toward whichever company happened to have the most people with any
     "Vice President ___" title (23 of a 40-result page went to one company),
     starving smaller companies of any results at all. Switched to bracket-exact
     syntax (`[CEO]`, `[Founder]`, `[President]`, `[Managing Partner]`, `[Owner]`)
     plus plain-keyword `Business Development` / `Head of Growth` / `Head of New
     Business` (kept unbracketed since these are more distinctive phrases) —
     this fixed the noise but still pulled in junior BDR/SDR titles under
     "Business Development" (13 of 50). Recommend the persona list either add
     a `job_level` filter (C-Team/VP/Director only) or an explicit
     exclude list (Representative, Associate, Specialist) alongside it, and use
     bracket-exact matching for the single-word C-suite titles by default.
  2. **Company-size ceiling is missing.** The vertical doc's ICP only sets a
     headcount *floor* (≥10) — there's no ceiling, so raw filters pull in
     40,000+-employee public holding companies that are a poor fit for
     "agencies that themselves rely on outbound." Recommend adding an explicit
     upper headcount bound (or a `type.exclude` for Public Company) once you
     confirm the intended agency size band.
  3. **Two qualified companies are ambiguous and included for your review, not
     silently excluded or silently kept:** Droga5 (founder-led heritage, but
     acquired by Accenture in 2019 — now a holdco subsidiary) and Bbh London
     (part of the WPP network). Both look independent on paper (privately
     held / partnership type) but may not fit "independently BD-driven" once
     you know the ownership. See companies CSV notes column.
  4. **"Founders locally present" (icp-overview.md) isn't a Blitz-queryable
     filter** — HQ country is filterable in bulk, but verifying a founder's
     actual physical presence requires manual per-company review (LinkedIn/
     site check), which doesn't scale to a 13,383-company TAM. Applied HQ-country
     only for both the TAM count and the sample; the presence check would need
     to happen at qualification time for real pushes, not at sourcing time.
  5. **Person-location vs. company-HQ mismatch, not resolved:** several sampled
     decision-makers sit far from their agency's HQ region (e.g. a Wieden+Kennedy
     "President" based in Mumbai, another in Toronto — plausible regional-office
     staff at a global agency, not necessarily wrong, but worth a decision on
     whether contact-level location should also be constrained to US/UK/Europe,
     separate from the company-level HQ filter).
  6. **Data-quality flags observed, not corrected:** (a) one Wieden+Kennedy result
     tagged "Founder"/"Owner" for two different people — W+K's actual founders
     are historical/deceased, so this looks like a stale or mismatched LinkedIn-
     derived record, not fact-checked further; (b) BBDO returned with its company
     `name` field in Chinese ("天联广告公司") despite a US domain; (c) Criteo's
     `domain` field returned as `bit.ly`; (d) Interpublic Group and Omnicom
     returned identical `domain` values (one is wrong). None of these blocked
     the run but would need cleanup before any of these specific rows were
     pushed for real.
  7. Dedup logic verified against the ledger (still header-only / empty as of
     this run) — 0 of the 50 sampled people matched, as expected. Normalization
     (lowercase, strip query params + trailing slash) confirmed working correctly
     on the code path, just nothing to catch yet.
- Notes: No `fixed_signals` exist yet for this vertical (per the "To do" section
  above) so signal(s) column in the companies CSV is mostly "not assessed this
  run" except where a founding-year signal was obvious (Icon, founded 2024).
  Total Blitz record spend this run: 141 records (TAM company count 50, TAM
  people count 1, two people-search attempts at 40 + 50) — negligible against
  the ~14.9M remaining balance.
