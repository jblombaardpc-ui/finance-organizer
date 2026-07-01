# Ledger backend: Beancount (recommended)

Plain-text, auditable double-entry. Works for any number of sets of books.

## Setup (onboarding does this once)

1. Install: `pip install beancount --break-system-packages` (in the sandbox). Provides `bean-check` and `bean-report`.
2. Scaffold a starter ledger per set: `scripts/init_beancount.py --config .finance-organizer/config.yaml --set <set-id> --out "<set folder>/Beancount"`. This writes `main.beancount` (options + includes), `accounts.beancount` (open directives for the config's mapped accounts + the overlap accounts + an `Income:`/`Expenses:` account per the accountant's chart from `prior_financials.chart_of_accounts`, or `Uncategorized` roots if none were provided), and `opening.beancount` (opening balances placeholder to fill from statements).
3. Validate: `bean-check "<set folder>/Beancount/main.beancount"`. If `bean-check` isn't on PATH (pip often puts it in `~/.local/bin`), call it by full path, or validate version-proof with:
   `python3 -c "import sys; from beancount import loader; e,err,_=loader.load_file('<main>'); print(len(err),'errors'); [print(x) for x in err[:10]]; sys.exit(1 if err else 0)"`

## Structure

- `main.beancount` — options (`operating_currency` = config currency; Fava fiscal-year-end = the set's FYE) and `include`s.
- `accounts.beancount` — `open` directives.
- Monthly files `fyYYYY-MM.beancount` (business sets follow the FYE; personal sets follow the calendar year), each `include`d in `main.beancount`.

## Booking conventions

- Reconcile each account by its statement cycle; a month-end `balance` assertion equals the statement close (diff $0.00).
- Book card / line-of-credit payments and cash-advances-to-bank **once, from the bank side** — skip the matching line on the card/LOC statement.
- **Overlap:** owner-paid business costs (or business-paid personal costs) post to the config's `overlap.shareholder_loan_account` / `overlap.due_from_business_account` rather than an expense/income line. Also log business spend on personal cards in `overlap.personal_card_expense_doc`.
- **Tax:** if the user has a registration in `config.tax`, split the tax out of tax-inclusive revenue into a liability (e.g. `Liabilities:Tax:Collected`) at the configured rate. Leave input-tax credits for their accountant unless told otherwise.
- Categories: keep them stable; reuse what's in `accounts.beancount` and `memory.md`. If the user provided prior-year accountant statements at onboarding (`config.prior_financials`), the scaffold has already opened an `Income:`/`Expenses:` account per the accountant's category — **book to those names** so reports tie out against prior-year comparatives. Propose any genuinely new category via the learn protocol before relying on it.

## Autonomy & validation

Book entries you're confident about, then run `bean-check` (must pass, assertions intact). **Stop and ask** on anything ambiguous (business vs personal, unmatched transfer, unknown account/vendor, or anything that would move a reconciled figure) — or use the **flag-expense** skill to annotate without rebooking.
