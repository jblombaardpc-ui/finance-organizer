---
name: file-inbox
description: >
  Triage and clear the Finance Inbox for a finance-organizer user. Use when they say
  "clear my inbox", "file these", "process my inbox", "what's in my inbox", drop
  documents into their inbox folder, or want paperwork sorted/filed. Routes each
  document to the correct set of books per their config, names it by the convention,
  dedups via the rename ledger, clears the inbox, and hands eligible items to
  book-entries and the enabled optional modules.
---

# Clear & file the Finance Inbox

Read `.finance-organizer/config.yaml` first (and `memory.md`). If there's no config, run **finance-onboard** instead. Then read `../../references/conventions.md`. Operate on the user's working folder; the inbox is `config.filing.inbox` (default `Finance Inbox`).

## Procedure (per file)

1. **Identify** the document (date, vendor/payer, total or invoice #, the account/card it touches). Read PDFs/scans as needed.
2. **Dedup** before filing: `${CLAUDE_PLUGIN_ROOT}/scripts/dedup_check.py --file "<inbox file>" --ledger "<set folder>/Reports/File Rename Ledger.csv"`. On a match, don't refile — dedupe-delete (request delete permission if blocked) and log it. md5 alone isn't enough for re-downloads; also compare content + vendor/date/amount.
3. **Route** to a set using `config.accounts` + content (see conventions). Business spend on a personal account is still business → book to the business set, log it in `config.overlap.personal_card_expense_doc`, and **keep a COPY of the invoice in the business books** at `config.overlap.personal_card_expense_copies_dir` (default `<business set>/Expenses/Paid on Personal Accounts/`; use its `Candidates (pending review)/` subfolder when unconfirmed). Log that copy in the business set's rename ledger with `action=copy`. Travel receipts excepted (stay with the trip, cross-referenced by path). **Reason about business use:** proactively flag any personal-account charge that could reasonably be a business expense (judged against the user's business in `memory.md` and locality/tax in `config.tax`) as a candidate for manual review — flag rather than guess, flag rather than silently treat as personal, and never book a flagged candidate until the user confirms. **If unsure of the set or business-vs-personal, flag it and ask** — then offer to remember the answer (learn protocol).
4. **Name & move** per the convention into the right folder for that set.
5. **Log** the move with `${CLAUDE_PLUGIN_ROOT}/scripts/append_rename_ledger.py` into that set's rename ledger.
6. **Hand off** eligible items (only for enabled `config.modules`):
   - Postable transactions → **book-entries**.
   - Benefit/health-eligible bills → **claims-helper** (if `modules.claims_helper`).
   - Related-party invoices → **related-party** / **payment-plan** (if those modules are on).
7. **Clear** the inbox — everything filed or deduped.

## Learn as you go

When you decide a new vendor's category, encounter a new account, or the user corrects a routing, propose saving it (`../../references/learning.md`) — don't bake it in silently.

## Finish

Summarize what was filed, routed, deduped, handed off, and anything flagged for the user. Keep each set's rename ledger current. If a nightly run is configured, behave consistently with it (use the ledger so nothing double-files).
