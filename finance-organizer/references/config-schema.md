# Config schema — `.finance-organizer/config.yaml`

The onboarding skill writes this file into the user's working folder; every other skill reads it. It is the single source of truth, so prefer updating it over hardcoding anything. Keep a human-readable copy of key facts in `memory.md` too.

All paths are **relative to the user's working folder** (portable across machines). Never write absolute machine paths here.

## Top-level keys

- `version` (int) — schema version, currently `1`.
- `company` — identity + locality:
  - `name`, `primary_contact`
  - `locality`: `country`, `region`, `currency`
  - `fiscal_year_end` — `MM-DD` for the main business (personal sets are usually `12-31`).
- `ledger`:
  - `backend` — `beancount` | `simple` (CSV/spreadsheet).
  - `beancount_main` — path to the main ledger file (if Beancount).
- `sets_of_books` — a list; **this is the generalization of "three sets of books."** Each item:
  - `id` (slug), `label`, `type` (`business` | `personal`), `fiscal_year_end`, `folder`, optional `ledger_main`.
- `overlap` — how personal/business overlap is booked (the shareholder-loan / due-to/from pattern):
  - `shareholder_loan_account` (e.g. `Liabilities:Current:DueToShareholder`)
  - `due_from_business_account` (e.g. `Assets:DueFromBusiness`)
  - `personal_card_expense_doc` — path to the "business expenses paid on personal cards" log.
- `accounts` — the account map; each item: `last4`, `name`, `set` (matches a `sets_of_books.id`), `role` (`operating`/`savings`/`card`/`loc`/`tax`/…), optional `owner`.
- `tax`:
  - `registrations` — list of `{kind, number, rate, filing}` (e.g. GST/HST, VAT, sales tax).
  - `notes` — free-text local rules the user described during onboarding.
- `filing`:
  - `inbox` — inbox folder name (default `Finance Inbox`).
  - `rename_ledger_per_set` (bool) — keep one `Reports/File Rename Ledger.csv` per set.
- `modules` — booleans: `related_party`, `claims_helper`, `payment_plan`, `brand_output`.
- `related_parties` *(if module on)* — list of `{name, type, cards[], notes}`.
- `claims` *(if module on)* — `plan_name`, `eligible[]`, `ineligible[]`, `admin_fee_pct`, `tax_on_fee_pct`, `form_path`, `period_end` (`MM-DD`).
- `payment_plan` *(if module on)* — `daily_limit`, `currency`, `calendar_id`.
- `branding` — `guidelines_path` (default `.finance-organizer/brand.md`).
- `cadence` — `inbox_processing` (cron or "off"), `check_in` (e.g. "weekly Monday").

## Reading config in a script

`scripts/config_get.py --config <path> --key company.locality.region` prints a value, so scripts stay config-driven without each re-parsing YAML.

## Editing rules

- Onboarding writes the first version after showing the user the full draft and getting approval.
- Any later change goes through the **learn** protocol (`references/learning.md`): propose → confirm → write. Never silently overwrite.
