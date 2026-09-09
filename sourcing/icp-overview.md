# Algo Acquisition — Shared ICP Criteria (all verticals)

Agreed with the user (moeez@algoacquisition.ai) on 2026-09-08. These filters apply
across all three verticals unless a vertical doc overrides them.

## Verticals in scope

1. Staffing & Recruitment companies
2. Marketing companies
3. M&A (mergers & acquisitions) firms

## Firmographic filters

- **Minimum company revenue:** $1,000,000
- **Minimum headcount:** 10 employees

## Geographic / presence filter

- **Company HQ must be in the USA, UK, or Europe.**
- **Founders must be locally present** in that HQ region — i.e. exclude
  companies that are only nominally registered/HQ'd in US/UK/Europe but whose
  founders/leadership actually operate out of an offshore location. This is a
  genuine presence check (registered address + verifiable local leadership
  presence), not a filter on any individual's nationality, ethnicity, or
  background — do not implement it as a person-level ethnicity/origin filter.
- Practical implication for sourcing: verify company HQ address AND do a quick
  check that the founder(s)/leadership listed on LinkedIn/company site are
  based in that same HQ region before qualifying a company.

## Seniority filter (standing rule, all verticals — added 2026-09-08)

**Only target senior stakeholders who are genuine decision-makers** — people
with real authority to approve or champion a BD/outbound engagement. This
applies to people-sourcing in every vertical, not just wherever it was first
noticed as a problem (Vertical 2's test run — see its Progress Log entry
2026-09-08 11:39 UTC — found free-text title matching pulling in junior
BDR/associate-level people under keywords like "Business Development").

**Include (seniority level) — Director and above, confirmed by the user
2026-09-09:**
- Director / Senior Director / Director-level (any function relevant to the
  vertical — Sales, BD, Growth, Revenue, Marketing, New Business, Partnerships)
- Owner / Founder / Co-Founder / Managing Partner / Partner
- C-suite: CEO, COO, CFO, CRO, CMO, CTO, CGO, or any "Chief ... Officer"
- President / Managing Director / Executive Director
- VP and above (VP, SVP, EVP) in Sales, Business Development, Growth,
  Revenue, Marketing, New Business, or Partnerships

(An earlier draft of this rule, written 2026-09-08, excluded Director by
default and treated it as a per-vertical override for M&A only. The user
confirmed 2026-09-09 that Director-and-above is fine everywhere — this
supersedes that draft. Vertical 1's stored tracking-clients ICP config
already includes Director, so no change needed there on this point.)

**Explicit exclude (regardless of an include-keyword match):** Representative,
Associate, Coordinator, Specialist, Analyst, Assistant, Intern, Trainee, BDR,
SDR, Account Executive, and bare "Manager" (an individual-contributor title in
most orgs — does not count as senior on its own, even if it shows up inside a
longer title string). Apply this exclude list as a second pass even after an
include match succeeds — a title can contain an include keyword as a
substring while still being a junior role (e.g. "Business Development
Representative" contains "Business Development").

**Matching method — this is what actually went wrong in the Vertical 2
test run, apply the fix everywhere:**
- Free-text/loose keyword title search over-matches badly — e.g. searching
  loosely for "VP Sales" matched "VP Learning and Development", "VP Design",
  etc., because the matcher was scoring token overlap ("VP") rather than the
  full phrase.
- Use **bracket-exact / exact-phrase matching** for short, generic titles
  (`[CEO]`, `[Founder]`, `[President]`, `[Owner]`, `[Managing Partner]`) —
  the syntax a given tool supports for exact rather than fuzzy matching.
- For multi-word functional titles (VP Business Development, Head of
  Growth), require the full phrase, not token-overlap.
- Prefer a structured seniority/job-level field when the tool offers one
  (e.g. Blitz's people-search seniority buckets) over pure title-string
  matching, and combine both when available for the tightest result.
- Always run the exclude list above as a second pass, even on results that
  already matched an include title/seniority filter.

## Explicitly excluded

- Companies whose only real HQ/operating base is outside the USA, UK, or
  Europe, even if they list a US/UK/EU mailing address.
- Below $1M revenue or below 10 employees.
- People whose title matches the seniority exclude list above, or who don't
  meet the include criteria, regardless of company fit.

## Note on the earlier draft of this criterion

The user's first phrasing of the geo filter was "no South East Asian and
African origin companies and people," which was clarified on request to mean:
**HQ location in USA/UK/Europe with founders locally present** — a
company-location and presence filter, not an exclusion based on the ethnicity
or national origin of people or founders. Use the clarified version above for
all sourcing logic, Clay filters, and qualifier prompts.
