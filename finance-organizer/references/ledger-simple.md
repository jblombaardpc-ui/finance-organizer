# Ledger backend: simple (spreadsheet / CSV)

For users who don't want plain-text double-entry. One transactions ledger per set of books, easy to hand to an accountant at year-end.

## Structure

One file per set: `<set folder>/Ledger/<set-id>-ledger.csv` (plain CSV — the reports script reads CSV only; keep any spreadsheet copy as an export of this file). Columns:

`date, description, account, category, money_in, money_out, set, notes`

- `account` — the bank/card it touched (match a name in `config.accounts`).
- `category` — income or expense category (keep a consistent list; propose new ones via the learn protocol).
- `money_in` / `money_out` — one of them per row (keeps it readable for non-accountants).
- `notes` — anything useful (invoice #, tax portion, etc.).

Optionally keep a second tab/file `balances.csv` (`account, as_of, statement_close`) to reconcile against statements.

## "Booking"

- Append a categorized row per transaction. Reconcile monthly: the running total per account should match the statement close on `balances.csv`.
- **Overlap:** when one set pays another's cost, categorize it as `Due to/from <other set>` rather than a normal expense/income — that mirrors the shareholder-loan idea without double-entry.
- **Tax:** if registered, add a `tax_portion` note (or column) so totals can be split at filing time.

## Validation

There's no `bean-check`, so sanity-check instead: each month's `money_in - money_out` plus opening equals the statement close; flag anything that doesn't tie. Use **flag-expense** for items to revisit. Offer the user a Beancount upgrade later if they outgrow this.
