# ALGO full-universe build — complete brief (self-contained)

You have everything you need in this bundle. You do **not** have access to Algo's AlgoSourcing repo; do not
look for it. Read this whole file before running anything.

## 1. Who and why
**Algo Acquisition** (algoacquisition.ai) sells a done-for-you "booked-meeting engine" to B2B companies:
LinkedIn-first outbound (Sales Navigator + HeyReach), 5-minute reply handling, warm calling, booked meetings.
Core plan: $20k / quarter for 40 guaranteed showed meetings. This task builds **Algo's own prospect universe**: every
director-plus decision-maker at companies in Algo's target verticals, **target >= 1,500,000 never-contacted people**,
as one deduplicated master file. **Nothing is sent or pushed anywhere** (no HeyReach, no email): data only.

## 2. ICP for this run (user decisions, 2026-10-14)
- **Company HQ:** USA, Canada, UK and Europe. Country codes (44): US, CA, GB, IE, FR, DE, ES, IT, NL, BE, PT, CH, AT,
  SE, NO, DK, FI, PL, CZ, SK, HU, RO, BG, GR, HR, SI, EE, LV, LT, LU, MT, CY, IS, LI, MC, AD, SM, UA, RS, ME, MK,
  AL, BA, MD.
- **Person location:** the same 44 countries (decision-makers based where the company is).
- **Revenue:** > $1,000,000 (Blitz `company.revenue.min`).
- **Headcount:** more than 10 employees (Blitz `company.employee_count.min = 11`). Some verticals also cap at 500
  (see section 4).
- **Company types excluded:** Nonprofit, Government Agency, Educational, Educational Institution.
- **Seniority:** Director and above, enforced on the actual job title (section 6).
- **Firmographic filters only.** Never filter, score or drop people by their name, ethnicity, nationality or any
  proxy for them. Geography is handled only through company HQ and person location above.

## 3. Bundle layout
```
BRIEF.md                 this file
PROMPT.md                the task prompt you were given
algo_universe.py         combines all vertical runs into the master + checks + REPORT.md
listbuild/               the list-building tool (Python; tests in listbuild/tests)
workspace/               run everything from here (listbuild's workspace)
  config/u_*.yaml        one config per vertical, with this run's ICP already applied
  seeds/contacted_all.csv  everyone Algo has already contacted (exclude them)
  dnc_clients.csv        Algo's current and past clients (never contact anyone at these companies)
```

## 4. The verticals (all combined)
| Config | Vertical | Core industries (main list) | Keyword-gated industries (review file) | Headcount |
|---|---|---|---|---|
| u_v1_staffing_recruitment | Staffing & recruitment | Staffing and Recruiting, Executive Search Services, Temporary Help Services | Human Resources Services, Human Resources (staffing keywords) | 11+ |
| u_v2_marketing | Marketing / advertising / PR agencies | Marketing Services, Advertising Services, Public Relations and Communications Services, Graphic Design (+ legacy labels) | Market Research, Design Services, Design, Events Services | 11+ |
| u_v3_ma_advisory | M&A advisory (draft) | Investment Banking | Financial Services, Business Consulting and Services, Management Consulting (M&A keywords) | 11-500 |
| u_v4_b2b_saas | B2B SaaS & AI | Software Development, Data Infrastructure and Analytics, Desktop / Mobile Computing Software Products, Computer Software | Business Intelligence Platforms | 11-500 |
| u_v5_it_services | IT services & technology partners | IT Services and IT Consulting, Information Technology and Services, Computer and Network Security | Business Consulting and Services, Management Consulting (partner / MSP keywords) | 11-500 |
| u_v6_life_sciences_services | Life-sciences B2B services | (none) | Research Services, Biotechnology Research, Pharmaceutical Manufacturing, Medical Equipment Manufacturing (+ legacy) | 11-500 |
| u_v7_nearshore_dev | Nearshore / offshore dev teams | (none) | IT Services, Outsourcing and Offshoring Consulting, Software Development (+ legacy) | 11-500 |
| u_v8_fractional_consulting | Fractional execs & B2B consultancies | (none) | Business Consulting and Services, Management Consulting, Strategic Management Services | 11-500 |
| u_v9_peo_eor_hr_tech | PEO / EOR / payroll & HR tech | (none) | Human Resources Services, Software Development (+ legacy) | 11-500 |
| u_v1b_boutique_exec_search | Boutique executive search | Executive Search Services | Staffing and Recruiting (search keywords) | **2-9: contradicts "more than 10"; skip unless the user confirms** |

Exact labels and keywords are in each config. V6-V9 have no core industries, so all their people land in the
review file. The master main list comes from core-industry matches only.

## 5. How listbuild works (what it does for you)
Stages per config: `seed` (load exclusions) -> `blitz` (people sweep) -> `clay` -> `merge` -> `companies` /
`companies-kw` (company sweeps, keyword gate) -> `domains` -> `consolidate` -> `discolike-*` -> `fit` ->
`consolidate-final` -> `export`. Every stage is resumable: rerun the same command and finished stages are skipped.
Results live in `workspace/out/<config name>/ledger.sqlite` (table `contacts`, column `icp_fit` = fit / candidate /
unknown / unfit, `title_check` = pass / fail).

Commands (from `workspace/`):
```
python ../listbuild/scripts/listbuild.py --icp config/u_v1_staffing_recruitment.yaml preview --seeds seeds/contacted_all.csv
python ../listbuild/scripts/listbuild.py --icp config/u_v1_staffing_recruitment.yaml run --seeds seeds/contacted_all.csv --discolike-cap-usd 0
python ../listbuild/scripts/listbuild.py --icp config/<x>.yaml run --force --stages fit consolidate-final export   # re-classify only
```
Clay (quota exhausted until 2027-01-01) and DiscoLike (account limit) are not used in this run: the run logs them as
skipped; always pass `--discolike-cap-usd 0`. Blitz is the only provider.

## 6. Rules learned the hard way (do not relax)
- **Blitz silently ignores filters it does not support** and returns its whole database (~454M people / ~68M
  companies). listbuild fires a "filter canary" in every preview and run and aborts with `FilterIgnored`. Never
  bypass it. `company.linkedin_url` is NOT a Company Search filter.
- **50,000 results max per Blitz query:** listbuild shards losslessly (country, job level, industry, person country,
  employee range, founded year). Expect ~95% of the planned rows back; a gap > 10% is reported.
- **Headcount definition:** `company.employee_count` counts **employees on LinkedIn**, far stricter than the company's
  declared LinkedIn size band (`company.employee_range`: "11-50", "51-200", ...). Example, UK IT services: declared
  11-500 staff = 16,337 companies vs >= 10 on LinkedIn = 6,727. The configs use `employee_count`.
- **Industry labels:** Blitz keeps legacy LinkedIn labels as separate values (e.g. "Information Technology and
  Services", "Computer Software", "Research", "Biotechnology"); configs include them. An invalid label is rejected
  with HTTP 422 (e.g. "Computer & Network Security", "Medical Devices").
- **Dedup on the normalised LinkedIn URL only** (lowercase, no query string, no trailing slash, percent-decoded). Two
  people with the same name at the same company are different people if their URLs differ.
- **Title guard (Director and above):** passes Director, Head, VP/SVP/EVP, C-suite / Chief ... Officer, President,
  Owner, Founder, Partner, Managing Director, Board, plus German / French / Dutch / Spanish / Italian / Polish /
  Nordic / Czech / Hungarian equivalents. Fails Associate, Coordinator, Specialist, Analyst, Representative,
  BDR, SDR, Account Executive, Talent Partner, bare Manager / Recruiter / Consultant unless the person's own title is
  top-tier (Founder, Owner, CEO, MD...). Assistant, Intern, Trainee, AVP and advisory-board roles always fail.
- **Filter-inferred industry is not evidence:** a person counts as "fit" only when the company's own enriched
  industry matches; otherwise "unknown" (review file).
- **Catch-all labels are never core:** Business Consulting, Financial Services, HR Services, Market Research etc. are
  keyword-gated (about 30% precise) and go to the review file.
- **Placeholder employers** ("Private Company", "Self-employed", "Freelance", "Confidential", "Undisclosed",
  "Family Office", "Stealth"...) are dropped.
- **Large enterprises** pass the filters but fit Algo's offer poorly (e.g. Robert Half, VML, Publicis, Deutsche
  Bank). Report the top 20 companies by people count; do not drop them without the user's say-so.
- **Long runs:** cloud shells stop background commands after ~10 minutes. Start long runs detached:
  `setsid nohup python ../listbuild/scripts/listbuild.py ... > logs/<name>.log 2>&1 < /dev/null &`, then check the
  log. If a run dies, rerun the identical command (it resumes).
- **Blitz limits:** 50 requests/second per key (shared by everything using the key), records per cycle shown by
  `GET https://api.blitz-api.ai/v2/account/key-info` with header `x-api-key: $BLITZ_API_KEY` (~14.4M left, resets
  2026-11-07). Run verticals one at a time. A full pull of ~2-3M people fits.

## 7. Keys
Needs the env var `BLITZ_API_KEY`. Check presence only (`env | grep -q '^BLITZ_API_KEY=' && echo set`); never print,
log or write a key into a file. If it is missing, stop and tell the user.

## 8. If the combined main list is under 1,500,000
Do not loosen anything on your own. Measure each lever with a preview and report the gain:
1. Remove the 500 cap (`employee_count_max`) on V3-V9.
2. Use the declared size band instead of employees-on-LinkedIn: replace `employee_count_min: 11` with Blitz
   `employee_range` 11-50 and above (needs a small change in `listbuild/listbuild/providers/blitz.py`, test-first,
   and a canary pass).
3. Count the keyword-gated review layers.
4. Add adjacent industries (e.g. Financial Services, Insurance, Real Estate, Accounting, Legal Services) as a new
   config (`new-icp`, see `listbuild/README.md`).
Then ask the user which to apply.

## 9. Outputs
`python ../algo_universe.py --out ../universe_output` (from `workspace/`) writes:
- `algo-universe_partNN.csv.gz`: the master main list, <= 250k rows per part, columns `linkedin_url, first_name,
  last_name, full_name, job_title, seniority, company_name, company_domain, company_linkedin_url, industry,
  person_country, company_country, vertical, all_verticals, icp_fit, fit_reason`;
- `algo-universe_review.csv.gz`: keyword-gated candidates + unverified industry (never mixed into the main list);
- `REPORT.md`: per-vertical counts, combined total vs 1.5M, country and seniority split, top 20 companies, and the
  checks (duplicates, already contacted, Algo clients, title-guard fails, countries outside the list), which must all
  be 0 (the script exits with an error otherwise).
