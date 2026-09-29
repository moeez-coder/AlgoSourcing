# Client-base analysis: which verticals to do outreach on

Analysed 2026-09-29 by the master session. Inputs:
- the client DNC export the user shared (40 unique clients after dedup, Algo itself removed), and
- 24 further clients in the tracking_clients system that are not in that export (mostly signed Aug-Sep 2026).

Each client was profiled from its Blitz company record (LinkedIn industry, headcount, HQ, description,
specialties); Jeanne M. Sullivan from her website. Campaign results were deliberately left out (user, 2026-09-29).
All 65 clients are now in `data/dnc_clients.csv` and are never contacted (see the end of this file).

## The client base at a glance

| Cluster | Clients | Share |
|---|---|---|
| Recruitment, staffing and executive search | 35 | 54% |
| B2B software and AI companies | 13 | 20% |
| IT services and technology consulting | 7 | 11% |
| Consulting and advisory boutiques | 6 | 9% |
| Investors / holding companies | 2 | 3% |
| Marketing agency | 1 | 2% |
| Industrial manufacturer | 1 | 2% |

Three patterns matter for targeting:
1. **Recruitment is the core buyer**, and inside it the clients bunch into clear niches (below).
2. **About a third of all clients have 10 or fewer employees on LinkedIn** (23 of 65, plus solo advisor Jeanne Sullivan; including 12 of the 35
   recruitment firms). Boutique retained-search firms are a proven buyer that the current "headcount >= 10"
   filter excludes.
3. **The same end markets recur across clusters:** healthcare and life sciences (7 clients), defence, aerospace and
   space (5), financial services and wealth (6), engineering and regulated manufacturing (5).

## Every client, by cluster

### Recruitment, staffing and executive search (35)
| Client | Niche | HQ | LinkedIn staff |
|---|---|---|---|
| Epic Physician Staffing | Physician staffing, locum tenens | US | 67 |
| Epic Special Education Staffing (Seabright) | School therapy / special-ed staffing | US | 356 |
| Rosman Search | Physician recruitment (neuro, urology, GI) | US | 74 |
| Meet Life Sciences | Pharma, biotech, CRO recruitment | GB | 508 |
| Mastrovito Associates | Defence (cleared) and engineering recruitment, RPO | US | 1 |
| Thomas Taylor Partners (TTSP) | Exec search: defence, aerospace, space (PE/VC-backed) | US | 13 |
| Astro Talent | Space-industry recruitment | GB | 3 |
| JBL Resources | Engineering, quality, regulatory in regulated manufacturing | US | 93 |
| Core Group Resources | Maritime, offshore, oil and gas | US | 179 |
| Excel Resourcing | Automotive and technical recruitment | GB | 47 |
| Trillium Staffing | Light-industrial temp and direct hire | US | 799 |
| Brilliant Staffing | Accounting, finance and IT staffing | US | 196 |
| Abacus Search & Staffing | Accounting, finance, HR, supply chain (Midwest) | US | 50 |
| Talent Edge | Finance and technology perm / interim / RPO | GB | 71 |
| Harrison Stone & Associates | Retained search, investment management | US | 3 |
| Leah Yosef International | Retained search, private wealth / RIAs | US | 25 |
| Search Intelligence Group | Retained VP / C-suite search for PE-backed firms | US | 5 |
| Sequel Search | Exec search for the consultancy sector | US | 1 |
| Solutions Driven | Exec search, STEM, RPO | GB | 54 |
| Harrison Davies Partners | Boutique recruitment | GB | 7 |
| Brick Executive Search | Boutique exec search | US | 3 |
| Logix Inc. | Exec search: biotech, IT, consulting | US | 59 |
| The Rosenstein Group | SaaS / eCommerce sales recruiting | US | 3 |
| Quanta | Tech and SaaS GTM recruitment | GB | 9 |
| Local World Inc. | SAP and Salesforce recruitment and delivery | US | 96 |
| PTY Tech | IT staffing | US | 8 |
| Blu (Blu Selection) | Multilingual recruitment across EU hubs | ES | 57 |
| Reesmarx | Global expansion and exec search | US | 33 |
| Cobalt Recruitment | Recruitment (Blitz could not resolve the company) | ? | ? |
| Moving Up Recruiting | Recruitment agency | US | 3 |
| Super Recruiter | Recruitment for in-house hiring teams | US | 8 |
| Zipdev | Nearshore developer staffing (LatAm) | US | 75 |
| Alcor | Nearshore R&D centres (LatAm, Eastern Europe) | US | 229 |
| Assist World | Virtual assistant / offshore staffing | US (Asia offices) | 51 |
| Nextwo | Tech talent (Jordan, Egypt) for Saudi Arabia | JO | 127 |

### B2B software and AI (13)
Deepen AI (autonomous-systems data, 225), S3 Partners (financial data, 68), Sensor Bio (medical wearables, 16),
VNTANA (3D product content, 28), Airoi (ESG/carbon AI, 24), DTR Labs (retail attribution, 37), Brain Payroll
(payroll SaaS, GB, 159), Rolai (enterprise AI for higher ed, 5), Weilliptic (AI / tokenisation, 8), SecondDesk AI
(AI agents for healthcare recruiting, 2), American Data Solutions (S1000D defence documentation software, 16),
Jurisphere / ReCo Legal (legal AI, IN, 33), Witzzy (AI speed-to-lead, n/a).

### IT services and technology consulting (7)
Triumphus (IT consulting, 11), Forge Digital (Siemens NX / Teamcenter / Mendix digital engineering, 8),
Insurance Technology Services (insurance systems consulting, 49), Teleion (data and AI professional services, 147),
STORServer (backup and DR, 13), POSRG (point-of-sale solutions, 60), Drebcon (compliance and audit, IN, 1).

### Consulting and advisory boutiques (6)
Tiffany Otten Consulting and its brand Coro (RevOps / martech, 5), Jeanny Consulting (pricing strategy, BE, 3),
Sullivan Adventures / Jeanne M. Sullivan (fundraising coaching, ex-StarVest VC, solo), Follow The Sun
(consulting, 3), SharpenHR (HCM technology consulting, 1).

### Others (4)
Long Holding Company (permanent-capital acquirer of information-services businesses, 3), Bluecat Investments
(land acquisition), The Matchstick Group (healthcare marketing agency, 6), Garrison Flood Control (flood-barrier
manufacturer, 23).

Outside the US/UK/Europe HQ rule: Nextwo (Jordan), Drebcon and Jurisphere (India). Assist World is US-HQ with
Asian delivery. These became clients anyway, but they are not a pattern to target.

## Recommended verticals, in priority order

### 1. Staffing & Recruitment (existing V1): keep as the top priority, split into sub-segments
Over half the client base, and the only cluster with repeat depth. Run it as sub-segments with their own
messaging and case studies, all from the same V1 sourcing:

| Sub-segment | Proof clients | LinkedIn industries / keyword gate |
|---|---|---|
| 1a. Healthcare and life-sciences staffing | Epic Physician, Epic Special Ed, Rosman, Meet Life Sciences | Staffing and Recruiting + physician, locum, nurse, allied health, pharma, clinical |
| 1b. Retained and boutique executive search | TTSP, Harrison Stone, Leah Yosef, SIG, Sequel, Brick, Solutions Driven, Harrison Davies, Logix | Executive Search Services + Staffing and Recruiting with "retained / executive search" |
| 1c. Technical, engineering and industrial recruitment | Mastrovito, JBL, Core Group, Excel Resourcing, Astro Talent, Trillium | Staffing and Recruiting + engineering, defence, aerospace, manufacturing, automotive, maritime, energy |
| 1d. IT, tech and finance/accounting staffing | Brilliant, Abacus, Talent Edge, PTY Tech, Local World, Quanta, Rosenstein | Staffing and Recruiting + IT, SaaS, accounting, finance |
| 1e. Nearshore / offshore talent providers | Zipdev, Alcor | Staffing and Recruiting / IT Services + nearshore, LatAm, remote developers (US/UK/EU HQ only) |

**Decision needed:** 12 of the 35 recruitment clients have 10 or fewer staff on LinkedIn, mostly boutique
retained-search firms. Today's "headcount >= 10" rule excludes them. Recommendation: keep the rule for the main
V1 list and add a separate test segment, "boutique executive search, 2-10 employees, revenue >= $1M".

### 2. B2B software and AI companies (new V4): strongest new vertical
13 clients (20%), mostly venture-backed, 10-250 staff, founder-led, selling to enterprises. Common thread:
**vertical AI and data products** (health tech, fintech / financial data, legal tech, HR and payroll tech, defence
and industrial software, retail and martech).
- Industries: Software Development, Technology Information and Internet, Information Services (legacy: Computer
  Software, Internet).
- Filters: 10-250 employees, revenue >= $1M, US/UK/Europe HQ, founders and C-suite / VP Sales / Growth.
- Expect a large TAM; narrow by the end markets above if the first preview is too broad.

### 3. IT services and technology consulting (new V5)
7 clients plus Local World, which straddles V1. Implementation partners (SAP, Salesforce, Siemens PLM), managed
IT / MSPs, data and AI consultancies, and infrastructure resellers (POS, backup).
- Industries: IT Services and IT Consulting (legacy: Information Technology and Services). A clean label, so
  low noise.
- Filters: 10-500 employees, revenue >= $1M, US/UK/Europe HQ.

### 4. Existing V2 Marketing: keep running, do not expand
Only one true agency client (The Matchstick Group, healthcare marketing), plus Tiffany Otten (RevOps consulting)
and Witzzy (AI lead-response software). The client base does not validate marketing agencies strongly. V2 has
already reached full TAM coverage (Progress Log, round 4). If it gets another pass, narrow it to specialist B2B and
healthcare agencies.

### 5. Existing V3 M&A: weakest evidence; reconsider before the full run
No M&A-advisory clients. The closest are Long Holding Company (an acquirer), Bluecat (land acquisition) and two
search firms that serve investment managers. If V3 continues, the client base points to **investors and
acquirers** (holding companies, search funds, lower-mid-market PE), not sell-side advisory boutiques. The V3
listbuild run queued behind V1 and V2 is a draft config and could be paused until this is decided.

### Not recommended as standalone verticals
- **Consulting and advisory boutiques:** 6 clients, but almost all solo or 5 staff or fewer, and the LinkedIn
  label ("Business Consulting and Services") is the noisiest catch-all there is. At most a small keyword-gated test.
- **Industrial manufacturing:** one client (Garrison Flood Control).

## Do-not-contact: clients are excluded from all outreach
- `sourcing/data/dnc_clients.csv` holds all 65 clients (company name, every known domain, company LinkedIn URL).
  `algo_bridge.py import` drops anyone whose company domain or company LinkedIn URL matches, and drops the
  companies from the companies file.
- **Found 2026-09-29:** 36 people at 9 clients were already sourced and pushed in earlier V1 rounds and sit in the
  V1 contacted ledger: Abacus (2), Brilliant (5), Core Group (5), JBL (3), Leah Yosef (3), Local World (3),
  Logix (5), Reesmarx (5), Rosman (5). Stopping them in HeyReach, and adding the clients to HeyReach's company
  blacklist, are outward actions that need the user's go-ahead.
- When a client signs, add it to `dnc_clients.csv` in the same commit.
