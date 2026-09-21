# Vertical 4 — B2B SaaS Companies

## Status

New vertical, initialized 2026-09-21. HeyReach campaign structure and Con Req
webhook are live; Open Check campaign/webhook is pending a manual start (see
below). No sourcing runs have happened yet. No tracking-clients `icp_config`
/ `sourcing_config` exists yet for this vertical.

### HeyReach campaigns (workspace 126779)

Cloned from Vertical 1's templates, "US & Europe | ... | Vertical 4 |Moe 1.0"
naming, senders = Vertical 1's account pool (4 disconnected/invalid accounts
swapped out for other valid Vertical 1 accounts to keep the pool at 100).

| Stage | Campaign name | Campaign ID | List ID | Status (2026-09-21) |
|---|---|---|---|---|
| Con Req | US & Europe \| Con Req \| Vertical 4 \|Moe 1.0 | 612584 | 954767 | PAUSED (started once to unlock webhook, then paused — empty list, no leads sent) |
| Con Acc | US & Europe \| Con Acc \| Vertical 4 \|Moe 1.0 | 612586 | 954768 | DRAFT (terminal, no webhook needed) |
| Open Check | US & Europe \| Open Check \| Vertical 4 \|Moe 1.0 | 612587 | 954769 | **DRAFT — needs manual start in HeyReach UI.** `start_campaign` returned a platform-side 500 three times in a row (2026-09-21); this blocks its webhook (HeyReach rejects webhook creation for DRAFT campaigns). Someone needs to start (and may then re-pause) 612587 in the UI, then its `VIEWED_PROFILE` webhook can be created via `mcp__Algo__create_webhook`. |
| Open Profile | US & Europe \| Open Profile \| Vertical 4 \|Moe 1.0 | 612588 | 954770 | DRAFT (terminal, no webhook needed) |

All 4 cloned sequences were confirmed structurally correct against the
`heyreach-vertical-launch` skill's spec (Con Req: single CONNECTION_REQUEST;
Con Acc: 3-message MESSAGE chain with `{message1}`/`{message2}`/`{message3}`;
Open Check: CHECK_IS_OPEN_PROFILE → VIEW_PROFILE; Open Profile: single INMAIL
with `{subject}`/`{inmail}`).

**Push targets once ready:** Con Req 612584 and Open Check 612587 (per the
standing instruction in `../heyreach-campaign-map.md` — push sourced leads to
both, never to Con Acc/Open Profile, which fill automatically via Clay
webhook).

### Clay webhooks

| Webhook | Event | Scoped campaign | Webhook ID | Status |
|---|---|---|---|---|
| Vertical 4 \| Moe \| Acc | CONNECTION_REQUEST_ACCEPTED | Con Req 612584 | 82967 | Active, verified |
| Vertical 4 \| Moe \| Open | VIEWED_PROFILE | Open Check 612587 | — | **Not yet created** — blocked on Open Check's manual start above |

## Target companies (draft — confirm/refine before large sourcing runs)

- B2B SaaS companies (software sold to other businesses, subscription/ARR
  model) doing active outbound BD/growth motion — i.e. companies that would
  be a buyer of Algo's own outbound sourcing/BD service, mirroring the
  self-referential logic used for the other 3 verticals (each vertical
  targets companies structurally similar to Algo's own ICP for that segment).
- Apply shared filters from `../icp-overview.md`: revenue ≥ $1M, headcount ≥
  10, HQ in USA/UK/Europe with founders locally present.
- No `fixed_signals` defined yet — candidate signals to consider: recent
  funding round (fresh budget for GTM hires), new VP/Head of Sales or
  Marketing hire, notable product launch or new pricing tier, job postings
  for AE/SDR/BDR roles (signals active outbound investment), G2/Capterra
  review velocity uptick.

## Target personas / titles (draft, mirrored from Vertical 1's buyer profile)

- **Seniority include:** CXO, VP, Head of, Director, Founder
- **Job titles (draft):** CEO, Founder, Co-Founder, VP Sales, VP Marketing,
  Head of Growth, Head of Demand Generation, Director of Revenue Operations,
  CRO
- Drafted from Algo's stated buyer profile; not yet validated specifically
  for the B2B SaaS vertical. Refine once real results come back.

## To do before next sourcing run

- [ ] Get Open Check campaign 612587 manually started (then may be re-paused)
      in the HeyReach UI, then create its `VIEWED_PROFILE` webhook scoped to
      612587
- [ ] Create a proper `icp_config` + `sourcing_config` in tracking-clients for
      this vertical (mirror the Vertical 1 structure)
- [ ] Confirm/replace the draft target-company and persona lists above with
      the user
- [ ] Confirm the >100-account sender cap: only Vertical 1's first 100 valid
      accounts were attached to each campaign (4 disconnected ones swapped
      out); the remaining accounts (from Vertical 1's fuller pool) can be
      added manually in the HeyReach UI later if desired — this is a hard API
      cap, not a choice made here
- [ ] Write outbound copy (message1/2/3 for Con Acc, subject/inmail for Open
      Profile) before pushing real leads — the cloned campaigns currently
      carry Vertical 1's template placeholders unfilled

## Dedup ledger

`sourcing/data/vertical-4-b2b-saas/contacted_ledger.csv` does not exist yet —
create it (header row only) before the first sourcing run. See
`../pipeline.md`, "The contacted ledger."

## Progress Log (append-only — newest entry on top; do not edit or delete other sessions' entries)

- **2026-09-21** (hub session): Initialized Vertical 4 (B2B SaaS). Created 4
  HeyReach lists + 4 campaigns cloned from Vertical 1's templates (IDs above),
  confirmed all 4 sequences structurally correct. Started-then-paused Con Req
  (612584) successfully to unlock webhook eligibility; Open Check (612587)
  hit a repeated platform-side 500 on `start_campaign` (3 attempts) and is
  still DRAFT — **needs manual start in the HeyReach UI before its webhook
  can be attached**. Created and verified the Acc webhook (82967, scoped to
  Con Req 612584). Open webhook not yet created — blocked on the above. No
  sourcing, no leads pushed, no `icp_config`/`sourcing_config` created yet.
