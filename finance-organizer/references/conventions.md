# Filing & naming conventions (config-driven)

Generic version of a proven filing system. Everything keys off the user's `config.yaml` — the inbox name, the `sets_of_books`, and the `accounts` map. Read those first.

## Route first, then file

For each inbox document, decide **which set of books** it belongs to (from content **and** the account/card used — look it up in `accounts[]`), then file within that set's `folder`. A business expense paid on a personal account is **still a business expense** — book it to the business set and log it in the `overlap.personal_card_expense_doc`. If genuinely unsure of the set, or business-vs-personal, **ask the user** (and offer to remember the answer via the learn protocol).

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

## Dedup — rename ledger (one per set)

Each set keeps `<set folder>/Reports/File Rename Ledger.csv`: `timestamp, action, fiscal_year, original_path, original_name, md5, new_path, notes`. Log every move/rename/dedupe-delete with the file's md5.

When a new inbox file arrives:
1. `scripts/dedup_check.py --file <f> --ledger <set>/Reports/File Rename Ledger.csv`. An md5 or name match means it's already filed — don't refile.
2. md5 alone isn't enough for re-downloads (PDF metadata differs); also compare content (pdftotext hash + vendor/date/amount).
3. Before booking, confirm the ledger doesn't already contain that date + vendor + amount.
4. Append moves with `scripts/append_rename_ledger.py`. Never create a duplicate file or ledger row; when unsure, compare content, then ask.
