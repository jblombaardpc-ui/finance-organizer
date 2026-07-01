# Config schema — `.finance-organizer/config.yaml`

The onboarding skill writes this file into the user's working folder; every other skill reads it. It is the single source of truth, so prefer updating it over hardcoding anything. Keep a human-readable copy of key facts in `memory.md` too.

All paths are **relative to the user's working folder** (portable across machines). Never write absolute machine paths here.

## Top-level keys

- `version` (int) — schema version, currently `1`.
- `company` — identity + locality:
  - `name`, `primary_contact`
  - `locality`: `country`, `region`, `currency`
  - `fiscal_year_end` — `MM-DD` for the main business (personal sets are usually `12-31`).
- `household` — `size` (number of household members to track) and `members` (list of names). Set from the onboarding question "how many household members?"; used to size the personal sets and to scope whose expenses are claimable (e.g. the claims module).
- `ledger`:
  - `backend` — `beancount` | `simple` (CSV/spreadsheet).
  - `beancount_main` — path to the main ledger file (if Beancount).
- `sets_of_books` — a list; **this is the generalization of "three sets of books."** The number of `type: business` entries = how many companies you track, and the `type: personal` entries correspond to household members — both come from the two onboarding counts. The **first entry is the primary set** — skills that need a single default location (e.g. bill-reminders' Payments Due tracker) use it, so onboarding should list the main business (or main set) first. Each item:
  - `id` (slug), `label`, `type` (`business` | `personal`), `fiscal_year_end`, `folder`, optional `ledger_main`.
- `overlap` — how personal/business overlap is booked (the shareholder-loan / due-to/from pattern):
  - `shareholder_loan_account` (e.g. `Liabilities:Current:DueToShareholder`)
  - `due_from_business_account` (e.g. `Assets:DueFromBusiness`)
  - `personal_card_expense_doc` — path to the "business expenses paid on personal cards" log.
  - `personal_card_expense_copies_dir` — folder in the business set holding COPIES of invoices for business expenses paid on a personal account (default `<business set>/Expenses/Paid on Personal Accounts/`; has a `Candidates (pending review)/` subfolder for unconfirmed items).
- `accounts` — the account map; each item: `last4`, `name`, `set` (matches a `sets_of_books.id`), `role` (`operating`/`savings`/`card`/`loc`/`tax`/…), optional `owner` (**reserved — not yet read by any skill**; capture it anyway for joint accounts).
- `prior_financials` — *optional*; prior-year **audited / accountant-prepared** financial statements the user chose to provide at onboarding. Used two ways: as **context** (so every skill knows how the books have historically been presented) and to **lock the chart of accounts** to the accountant's category names, so new entries and reports line up with prior years' comparatives. A list, one entry per set of books:
  - `set` — which `sets_of_books.id` these belong to.
  - `statements` — paths (relative to the working folder) to the filed prior-year statements (PDF/Excel). File the originals into that set's `Reports/` per the conventions; record their paths here.
  - `accountant` — the firm/person who prepared them (free text), if known.
  - `years` — which fiscal years are covered (e.g. `["FY2024", "FY2025"]`).
  - `chart_of_accounts` — the income/expense categories the accountant used, captured verbatim so they can be reused: `income` (list of category names) and `expenses` (list of category names). The ledger scaffold (`scripts/init_beancount.py`) opens an `Income:<Category>` / `Expenses:<Category>` account for each, so the user starts on the accountant's chart instead of `Uncategorized`.
  - `notes` — anything to remember (e.g. "match these names so year-over-year comparatives tie out", mapping quirks).
- `tax`:
  - `registrations` — list of `{kind, number, rate, filing}` (e.g. GST/HST, VAT, sales tax).
  - `notes` — free-text local rules the user described during onboarding.
- `filing`:
  - `inbox` — inbox folder name (default `Finance Inbox`).
  - `rename_ledger_per_set` (bool) — keep one `Reports/File Rename Ledger.csv` per set (**reserved — not yet read by any skill**; the per-set ledger is currently always used per `conventions.md`).
- `modules` — booleans: `related_party`, `claims_helper`, `payment_plan`, `bill_reminders`, `brand_output`, `integrations`.
- `related_parties` *(if module on)* — list of `{name, type, cards[], notes}`.
- `claims` *(if module on)* — `plan_name`, `eligible[]`, `ineligible[]`, `admin_fee_pct`, `tax_on_fee_pct`, `form_path`, `period_end` (`MM-DD`).
- `calendar` — the calendar the plugin writes events/reminders to, **provider-agnostic** (used by `payment_plan`, `bill_reminders`, and claims reminders): `provider` (`google` | `microsoft` | `apple` | `other` — whichever calendar connector the user linked, e.g. Google Calendar or Microsoft Outlook / Office 365), `id` (the target calendar's id or name — a **dedicated "Finance" calendar** is recommended; Google uses an id like `…@group.calendar.google.com`, Microsoft/Outlook a calendar name or id), and `timezone` (IANA, e.g. `America/Edmonton`). The plugin uses the connected calendar tool (`~~calendar`) via its create/list/update-event operations and **never creates a calendar itself** — onboarding guides the user to create the Finance calendar in their provider, then records its id here. See `CONNECTORS.md`.
- `payment_plan` *(if module on)* — `daily_limit`, `currency`, and an optional `calendar_id` (defaults to `calendar.id`). One-off invoice paydown within a daily limit — distinct from `bill_reminders`.
- `bill_reminders` *(if module on)* — recurring statement due-date + minimum-payment reminders. Optional `calendar_id` (defaults to `calendar.id`), `lead_days` (default 3), `tracker_path` (where the "Payments Due" table lives), `refresh` (`recurring` | `on_demand`) and `refresh_cron` (cron if recurring), and `accounts` — a list of `{last4, mode}` where `mode` is `manual` (pay by hand → "Pay") or `auto_debit` (pre-authorized → "Ensure funds"). Drives the **bill-reminders** skill.
- `branding` — `guidelines_path` (default `.finance-organizer/brand.md`).
- `integrations` *(if module on)* — financial connectors the user has linked, tool-agnostic: `accounting` (`quickbooks` | `xero` | `none`), `payments` (list, e.g. `square`, `stripe`, `paypal`), `bank_feed` (bool; **reserved — not yet read by any skill**), `notes`. Drives the **sync-financials** skill. The plugin never links a tool itself — the user connects each via their connector settings (see `CONNECTORS.md`).
- `cadence` — `inbox_processing` (cron or "off"), `check_in` (e.g. "weekly Monday").

## Reading config in a script

`scripts/config_get.py --config <path> --key company.locality.region` prints a value, so scripts stay config-driven without each re-parsing YAML.

## Editing rules

- Onboarding writes the first version after showing the user the full draft and getting approval.
- Any later change goes through the **learn** protocol (`references/learning.md`): propose → confirm → write. Never silently overwrite.
