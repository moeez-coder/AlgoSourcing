# Preview: v3_ma_advisory  (2026-09-29 11:24)
Blitz filter canary: every ICP filter narrows the unfiltered database (no filter silently ignored).
Blitz (free, plan ['Agency - Premium'], 10,869,153 records left this cycle):
  main-list contacts (core industries ['Investment Banking']): ~13,564  by HQ country: US 8,613, GB 1,583, IE 43, FR 705, DE 304, ES 391, IT 383, NL 182, BE 93, PT 85, CH 160, AT 58, SE 83, NO 372, DK 27, FI 82, PL 97, CZ 45, SK 11, HU 51, RO 12, BG 9, GR 27, HR 4, SI 0, EE 33, LV 5, LT 21, LU 6, MT 0, CY 2, IS 13, LI 11, MC 0, AD 0, SM 0, UA 53, RS 0, ME 0, MK 0, AL 0, BA 0, MD 0
  plus ~359,908 in catch-all industries -> candidates file
  estimated sweep time: ~10 min
Clay: WARNING quota exhausted right now (HTTP 402 from https://api.clay.com/public/v0/search/query-mode/search_0tm4idsMr2bmkGrCX2Z/run: {"mes). The run will still attempt Clay, report the stop, and continue with the other providers. Tell the requester before starting.
DiscoLike: no bucket maps to these industries -> stage skipped
Catch-all industries ['Business Consulting and Services', 'Management Consulting', 'Financial Services']: exported separately as *_consulting_candidates (keyword gate is ~30% precise), never in the main list
Prior lists (1 file(s), 67,123 LinkedIn URLs): 0 of 155 sampled contacts already prospected; the run excludes them