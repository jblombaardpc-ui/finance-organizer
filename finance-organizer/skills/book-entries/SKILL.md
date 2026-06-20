---
name: book-entries
description: >
  Post bookkeeping entries to a finance-organizer user's ledger. Use when they say
  "book [month]", "do my entries", "post these", "reconcile [account]", or after the
  inbox is filed and documents need to hit the books. Reads their config for the
  ledger backend, account map, overlap accounts, and tax profile; books autonomously
  when confident, validates, and asks only when genuinely unsure.
---

# Post ledger entries

Read `.finance-organizer/config.yaml` (and `memory.md`) first. Pick the backend from `config.ledger.backend` and follow the matching reference: `../../references/ledger-beancount.md` or `../../references/ledger-simple.md`. If there's no config, run **finance-onboard** first.

## Procedure

1. **Pick the set + ledger** for the documents in hand (`config.sets_of_books`). Reconcile by statement cycle.
2. **Apply the conventions** for the chosen backend: book card/LOC payments once from the bank side; route overlap to `config.overlap` accounts (and log personal-card business spend); split tax per `config.tax` if registered; reuse stable categories.
3. **Decide autonomously when confident; ask when unsure.** Post the entries you're confident about. **Stop and ask** for business-vs-personal ambiguity, unmatched transfers, a new/unknown account or vendor, or anything that would move an already-reconciled figure. For note-don't-rebook items, use **flag-expense**.
4. **Validate.** Beancount: `bean-check <ledger main>` must pass with assertions intact. Simple ledger: sanity-check that the period ties to the statement close.
5. **Learn.** Propose any new category/account/mapping for saving (learn protocol) before relying on it next time. Avoid double-booking re-dropped docs — check the rename ledger for the same date + vendor + amount first.

## Finish

Report what you booked, the validation result, and anything flagged or held for the user.
