# Filing & naming conventions (config-driven)

Generic version of a proven filing system. Everything keys off the user's `config.yaml` — the inbox name, the `sets_of_books`, and the `accounts` map. Read those first.

## Route first, then file

For each inbox document, decide **which set of books** it belongs to (from content **and** the account/card used — look it up in `accounts[]`), then file within that set's `folder`. A business expense paid on a personal account is **still a business expense** — book it to the business set and log it in the `overlap.personal_card_expense_doc`. If genuinely unsure of the set, or business-vs-personal, **ask the user** (and offer to remember the answer via the learn protocol).

### Business expenses paid on a personal account — keep a copy in the business books

When a business expense is paid on a personal account, the **original** stays in the personal set, but place a **copy** of the invoice in the business set too, so that set holds its own supporting documents at year-end. Put copies in `overlap.personal_card_expense_copies_dir` (default `<business set>/Expenses/Paid on Personal Accounts/`); use its `Candidates (pending review)/` subfolder when the business-vs-personal call isn't yet confirmed. Log the copy in the **business** set's rename ledger with `action=copy` (it shares the personal original's md5 — dedup is per-set, so a copy in another set is legitimate, not a duplicate). **Exception:** travel receipts stay only with their trip and are cross-referenced in the report by path.

### Reason about business use — flag candidates, don't guess

For anything on a personal account, actively judge whether it could *reasonably* be a business expense given the user's business (`memory.md`) and their locality/tax rules (`config.tax`, e.g. deductibility and any input-tax-credit on the embedded tax). If it's plausibly business, **flag it as a candidate** — add it to `overlap.personal_card_expense_doc` and drop a copy in the `Candidates (pending review)/` folder — for the user to confirm later. **Flag rather than guess, flag rather than silently treat as personal, and never book a flagged candidate until the user confirms.** Typical candidates: software/subscriptions used for work, professional memberships/licences/dues, tools/supplies/equipment, training/courses/conferences, work travel, and the business-use share of phone/internet.

## Filenames (all source docs except bank statements)

- `YYYY-MM-DD Vendor Amount.ext` — receipts/expenses/payments with a clear total (e.g. `2025-11-01 GoDaddy 149.09.pdf`). Amount = total, no currency symbol; foreign-currency docs named in their own currency.
- `YYYY-MM-DD Vendor INV<number>.ext` — invoices, incoming or outgoing.
- `YYYY-MM-DD Vendor Description.ext` — docs with no single amount (statements, letters, confirmations).
- Date = the document's own date (not the download date), ISO so files sort chronologically. Vendor in Title Case, cleaned of "Gmail - ", "Your … receipt", scanner codes, trailing `_0001`, and commas. Never use `|` (a common ledger delimiter).

## Bank statements

Folder `<Bank> <Type> <Last4>`, file `<Bank> <Type> <Last4> YYYY-MM.pdf`.

## Folder structure (per set)

A sensible default the onboarding can tailor:
- **Business set:** `Income/` (by stream) and `Expenses/` (by category, with per-vendor subfolders where useful), `Receipts/YYYY-MM/`, `Travel/YYYY-MM Place/` (trip receipts live with the trip only), `Bank Statements/`, `Reports/`, `Beancount/`.
- **Personal set:** `Bank Statements/`, `Receipts/`, `Property/`, `Investments/`, `Insurance/`, `Tax/`, `Reports/`, `Beancount/`, plus module folders (e.g. `Claims/`).

## Categories follow the accountant's chart

If the user supplied prior-year accountant/audited statements at onboarding (`config.prior_financials`), treat that `chart_of_accounts` as the canonical income/expense category list for the set. Reuse those names verbatim when filing and booking so the books and reports match prior-year comparatives. Only introduce a new category when nothing fits, and route it through the learn protocol first.

## Dedup — rename ledger (one per set)

Each set keeps `<set folder>/Reports/File Rename Ledger.csv`: `timestamp, action, fiscal_year, original_path, original_name, md5, new_path, notes`. Log every move/rename/dedupe-delete with the file's md5.

When a new inbox file arrives:
1. `scripts/dedup_check.py --file <f> --ledger <set>/Reports/File Rename Ledger.csv`. An md5 or name match means it's already filed — don't refile.
2. md5 alone isn't enough for re-downloads (PDF metadata differs); also compare content (pdftotext hash + vendor/date/amount).
3. Before booking, confirm the ledger doesn't already contain that date + vendor + amount.
4. Append moves with `scripts/append_rename_ledger.py`. Never create a duplicate file or ledger row; when unsure, compare content, then ask.
