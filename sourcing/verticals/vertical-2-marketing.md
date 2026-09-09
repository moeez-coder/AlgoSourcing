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

## Target personas / titles

**Apply the shared seniority filter in `../icp-overview.md`** ("Seniority
filter" section) — this directly resolves finding #1 from the 2026-09-08
test run below (loose title matching pulled in junior BDR/associate-level
people). Director-and-above: Owner/Founder/Partner, C-suite, President/
Managing Director, Director, VP-and-above in Sales/BD/Growth/Revenue/
Marketing/New Business/Partnerships.

Vertical-specific job titles to search within that seniority band (draft):
CEO, Founder, Managing Partner, President, VP Sales, VP Business Development,
Head of Growth, Head of New Business. Use exact/bracket matching (`[CEO]`,
`[Founder]`, `[President]`, etc.) for short titles per the shared rule's
"Matching method" — this is what the test run below found necessary. Still
not yet validated specifically for the marketing-agency vertical beyond that
one test run; refine further as more results come back.

## To do (non-blocking — can proceed with drafts, refine as results come in)

- [x] ~~Persona/title list needs bracket-exact matching + seniority
      filter~~ — resolved 2026-09-08, see `../icp-overview.md` "Seniority
      filter" section, added in response to this vertical's own test-run
      finding.
- [ ] Create a proper `icp_config` + `sourcing_config` in tracking-clients for
      this vertical (mirror the Vertical 1 structure) so it's tracked the same
      way
- [ ] Company-size ceiling still missing (test-run finding #2, separate from
      the seniority fix) — large holding companies (Publicis, Omnicom, IPG,
      WPP) still pass the raw company filters
- [ ] Re-run the TAM/sample with the new seniority filter applied — the
      13,383/40,035 TAM and the 40,035 people figure both predate this rule
      and are now stale

## Dedup ledger

`sourcing/data/vertical-2-marketing/contacted_ledger.csv` exists (header row
only as of 2026-09-08, no runs yet). Check it before every push, update it
after every push — see `../pipeline.md`, "The contacted ledger."

## TAM (Total Addressable Market) — append-only, newest entry on top

Total companies matching this vertical's ICP filters, and total people
matching its persona/title filters across those companies — not the sample
actually sourced/pushed. See `../pipeline.md`, "TAM entry format."

### 2026-09-09 12:20 UTC — execution-session-vertical-2 (Director-and-above correction, per confirmed seniority rule)
- Companies matching ICP filters: 19,604 (unchanged — same 8-industry, headcount/revenue/HQ/type
  filters as the entry below; this run only changed the person-level seniority filter).
- People matching persona/title filters across those companies: 83,223 (method: Blitz
  `POST /v2/search/people`, `total_results`, `max_results=1`; company filters unchanged,
  person filters corrected to `job_level` = [C-Team, VP, Director] (dropped Manager, Staff)
  + `job_function` = [Advertising & Marketing, Sales & Business Development], per the
  user's 2026-09-09 confirmation ("Director and above ... not lower than that") now
  codified in `../icp-overview.md`'s "Seniority filter" section.
- Notes: **This is the vertical's current working TAM** — supersedes the 422,850 figure
  below, which used the broader Manager/Staff-inclusive job_level set at the user's
  earlier "~400,000" volume request. The `total_results` figure (83,223) reflects only
  the `job_level`+`job_function` filter, not the standing rule's mandatory second-pass
  exclude list (Representative, Associate, Coordinator, Specialist, Analyst, Assistant,
  Intern, Trainee, BDR, SDR, Account Executive, bare "Manager") — that exclude pass can
  only be applied to actually-returned records (title strings), not to a `total_results`
  count, so 83,223 is a slight overcount of the true addressable pool; the ~9.2%
  exclude rate measured on the 10,512-person sample below (965 of 11,477 pre-exclude
  records) is a reasonable estimate of the gap if a tighter TAM number is needed.

### 2026-09-08 14:48 UTC — execution-session-vertical-2 (wide-net re-run, per user request)
- Companies matching ICP filters: 19,604 (method: Blitz `POST /v2/search/companies`,
  `total_results`; same as prior entry below but industry list widened from 5 to 8:
  added Market Research, Design Services, Events Services. Headcount/revenue/HQ/type
  filters unchanged.)
- People matching persona/title filters across those companies: 422,850 (method:
  Blitz `POST /v2/search/people`, `total_results`, `max_results=1`; same 8-industry
  company filters, person filters switched from the narrow title-keyword list to
  `job_level` = [C-Team, VP, Director, Manager, Staff] AND `job_function` = [Advertising
  & Marketing, Sales & Business Development] — this is a materially different, broader
  targeting method than the previous entry's title-keyword approach, done at the
  user's explicit request to widen the net toward ~400,000 people. Landed at 422,850,
  ~6% over the ~400k target — close enough without further tuning.)
- Notes: **This number is legitimate but concentration-heavy** — confirmed by
  pulling real records, not just inferred: of the first 3,000 people records
  returned by blanket pagination against this exact filter set, 2,674 (89%) were
  a single company (Publicis Groupe, 41,945 LinkedIn employees) and the rest were
  Figma (a design SaaS company, mistagged into the "Design Services" industry —
  see Progress Log for detail). A handful of the largest global holding-company
  networks account for a very large share of the 422,850 total; the number is
  real but not evenly distributed across the 19,604 companies. See Progress Log
  entry same timestamp for how the actual sample was built to avoid this
  concentration.
- This *replaces* the prior entry's method as the vertical's working definition of
  "decision-maker" for TAM purposes going forward (bracket-exact C-suite titles
  were abandoned in favor of job_level+job_function for volume) — flagging in case
  a future run wants to reconcile the two TAM methodologies rather than just take
  the newest number at face value.

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

### 2026-09-09 12:20 UTC — execution-session-vertical-2 — TEST RUN, NO PUSH (Director-and-above correction, ~10k volume)
- Sourced: 1,998 companies (same widened pool as the prior wide-net run, minus the 2
  confirmed mistags) / 10,512 people
- Files: sourcing/data/vertical-2-marketing/companies/2026-09-09_1220_director-plus-10k-batch3.csv,
         sourcing/data/vertical-2-marketing/people/2026-09-09_1220_director-plus-10k-batch3.csv
- Pushed to HeyReach: **none yet** — the user asked to "push around 10k leads to
  connection req and open check campaign" and is creating a new HeyReach campaign for
  this session to push into. Per the testing/priming phase's explicit "check with the
  user directly, don't just assume" rule, and given a push of this size is not easily
  reversible, this session prepared the leads but held the actual push pending (a) the
  new campaign ID(s) from the user and (b) one more explicit go/no-go on this specific
  push. Not calling `add_leads_to_campaign`/`add_leads_to_list` until both are in hand.
- Push targets: existing Con Req 568586 / Open Check 568621 not re-verified this run
  (last checked 2026-09-08) — open question for the user whether the new campaign
  replaces or supplements these.
- Context: the user corrected the seniority bar to "Director and above ... not lower
  than that," which lines up exactly with the standing rule the master session had
  just added to `../icp-overview.md` ("Seniority filter" section, confirmed 2026-09-09).
  This run re-sourced from the same 8-industry/headcount/revenue/HQ-filtered company
  universe as the prior wide-net batch, but with `job_level` restricted to
  [C-Team, VP, Director] (dropping Manager, Staff) and then, critically, applied the
  standing rule's **mandatory second-pass exclude list** on the actual returned titles
  (Representative, Associate, Coordinator, Specialist, Analyst, Assistant, Intern,
  Trainee, BDR, SDR, Account Executive, bare "Manager") — this is not redundant with
  the job_level filter: it caught 965 people (9.2% of the initial 10,507-record pull)
  who were tagged job_level=Director by Blitz but had junior-leaning titles, mostly
  "Associate [X] Director" (877 of the 965) plus a smaller number of bare "Manager",
  "Intern", "Account Executive", "Specialist", and "Assistant" titles. Recommend
  treating this as confirmation that job_level alone is not sufficient and the
  exclude-list pass should be standard for every future pull, not just this one.
- **Repeated the same per-company-capped sourcing method from the prior wide-net run**
  (one query per company, capped `max_results`, this time 10-15 depending on pass) to
  avoid the Publicis/Figma-style domination problem discovered then — confirmed working
  again: 1,563 distinct companies represented across 10,512 people, largest single
  company only 19 (0.18%).
- Process note: needed two passes to hit the ~10.5k target after the exclude-list
  removed 965 — pass 1 queried all 1,998 qualified companies at `max_results=10` each
  (10,507 before exclusions, 9,542 after); pass 2 topped up from the 581 companies that
  had zero surviving results after pass 1's exclude filter, querying them at
  `max_results=15` and applying the same exclude filter inline, adding 970 more from
  266 of those companies to land at the final 10,512. No internal duplicates in the
  final file (verified: 10,512 rows, 10,512 distinct `linkedin_url`s).
- Dedup logic re-verified against the ledger (still empty) — 0 of 10,512 matched, as
  expected. Separately checked cross-batch overlap across all three saved run files for
  this vertical (batch1 test run, batch2 wide-net, batch3 this one) since they draw from
  overlapping company pools with different seniority bars: 346 people appear in more
  than one saved file. This does not affect a real push, since the ledger (not the
  per-run CSVs) is the actual dedup source of truth and only this batch (batch3) would
  be the one pushed — flagging only so a future session doesn't assume the three files
  are mutually exclusive if it ever needs to reconcile them.
- Notes: Blitz record spend this run: ~13,500 records (2,000 for the company pool,
  ~10,507 + ~4,000-ish across the two people-search passes including companies that
  returned 0 after filtering) — still negligible against the ~14.8M remaining balance.

### 2026-09-08 14:48 UTC — execution-session-vertical-2 — TEST RUN, NO PUSH (wide-net re-run)
- Sourced: 198 qualified companies (200 evaluated) / 986 people
- Files: sourcing/data/vertical-2-marketing/companies/2026-09-08_1448_wide-net-batch2.csv,
         sourcing/data/vertical-2-marketing/people/2026-09-08_1448_wide-net-batch2.csv
- Pushed to HeyReach: none (testing/priming phase — awaiting final approval)
- Push targets: still Con Req 568586 / Open Check 568621, per the entry above — not
  re-checked again this run (checked ~3 hours earlier same day, no reason to expect
  drift within the same session).
- Context: the user asked to "make the net much wider" after the first test run,
  then explicitly chose (multi-select): bigger volume at the same quality bar,
  bring the holding-company networks back in, broaden industry/title definitions,
  and use Clay in addition to Blitz — then gave a concrete target of "~400,000"
  prospects. This run widened company industries (5→8: added Market Research,
  Design Services, Events Services) and switched person targeting from a curated
  C-suite title list to `job_level` (C-Team/VP/Director/Manager/Staff) + `job_function`
  (Advertising & Marketing, Sales & Business Development) to hit that volume via
  Blitz. **Clay was not used this run** — ran out of scope for this pass; flagging
  per `TOOLS.md`'s standing instruction not to silently skip a requested tool. Should
  be layered on in a follow-up run per the "maximize coverage" data philosophy in
  `pipeline.md`.
- Feedback given to user: new TAM = 19,604 companies / 422,850 people (~6% over the
  400k target). Critical finding en route to this number: **blanket pagination
  against a broadened filter that includes large holding-company networks does not
  produce a diversified sample** — tested directly by pulling 3,000 consecutive
  people records against the widened filter and finding only 2 distinct companies
  represented (2,674 from Publicis Groupe alone, 326 from Figma), because Blitz's
  cursor pagination appears to enumerate a matching company's full employee base
  before moving to the next company, and Publicis alone (41,945 LinkedIn employees)
  is large enough to fill many thousands of consecutive results. Fixed by switching
  to **one capped query per company** (`max_results=5`, scoped via `company.linkedin_url`
  to each of the 198 qualified companies individually) instead of one blanket
  cross-company query — this guarantees every company is represented in the actual
  sample regardless of its size, at the cost of not literally enumerating the
  ~400k-person TAM into a file (which was never the intent — TAM is a total-match
  count, not a to-be-enriched list, per `pipeline.md` step 0). This is a real,
  previously-undocumented Blitz pagination behavior worth keeping in mind for any
  future high-volume pull across multiple companies, not just this vertical.
- Notes / judgment calls and data-quality issues this run:
  1. **Two companies excluded as confirmed mistags, not just flagged this time:**
     Figma (a design SaaS/software company, matched via the "Design Services"
     industry tag but is not a marketing/creative agency) and "Google Adsense"
     (a Google ad product, not an independent company — clearly a data artifact
     in Blitz's company index). Both are marked `qualified=no` in the companies
     CSV. The rest of the "Design Services" tag looked legitimate on inspection
     (IDEO, Pentagram, Wolff Olins, AKQA, Designit, COLLINS, WongDoody, etc. — real
     branding/design agencies), so the whole industry category was kept rather than
     dropped wholesale.
  2. **Seniority bar is intentionally much looser than the previous run.** Widening
     `job_level` down to Manager/Staff (previously bracket-exact C-suite titles only)
     pulled in real volume but also junior-leaning titles (Associate, Coordinator,
     Specialist, Assistant) — 132 of 986 rows flagged `seniority=junior` in the
     people CSV's notes/seniority columns. This is a direct, expected consequence of
     the volume target, not a mistake — flagging so the user can decide whether the
     job_level floor should sit higher (e.g. drop Staff) once real numbers are
     visible, since 400k was requested with "use all possible filters," which this
     run took literally.
  3. **Large holding-company networks are back in-scope** per the user's explicit
     choice ("bring the holding networks back in") — Publicis, Omnicom, IPG, WPP-
     owned shops, etc. are no longer excluded from either the TAM or the qualified-
     company list, reversing the previous run's manual curation. Their outbound-BD
     fit concern raised in the prior entry still stands and wasn't re-litigated here
     since the user already made the call.
  4. Dedup logic re-verified against the ledger (still empty) — 0 of 986 sampled
     people matched, as expected.
- Notes: Total Blitz record spend this run: ~1,190 records (several cheap `max_results=1`
  probes while tuning the ~400k target, 200 for the company pool, 986 for the
  per-company people pull) — negligible against the ~14.9M remaining balance.

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
