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

## Explicitly excluded

- Companies whose only real HQ/operating base is outside the USA, UK, or
  Europe, even if they list a US/UK/EU mailing address.
- Below $1M revenue or below 10 employees.

## Note on the earlier draft of this criterion

The user's first phrasing of the geo filter was "no South East Asian and
African origin companies and people," which was clarified on request to mean:
**HQ location in USA/UK/Europe with founders locally present** — a
company-location and presence filter, not an exclusion based on the ethnicity
or national origin of people or founders. Use the clarified version above for
all sourcing logic, Clay filters, and qualifier prompts.
