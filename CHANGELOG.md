# Changelog

All notable changes to the finance-organizer plugin are recorded here.
This project uses [semantic versioning](https://semver.org/).

## [0.5.0] — 2026-06-29

### Added
- **Prior-year financials in onboarding.** `finance-onboard` now offers to take audited / accountant-prepared statements from previous years. They're used as context and to **lock the chart of accounts to the accountant's category names**, so new entries and reports line up with prior-year comparatives.
- New optional `prior_financials` block in the config (per set of books): `statements` paths, `accountant`, `years`, and a `chart_of_accounts` of income/expense category names. Documented in `references/config-schema.md` with a worked example in `references/config.example.yaml`.
- `init_beancount.py` seeds an `Income:`/`Expenses:` account for each category in `prior_financials.chart_of_accounts` (falling back to `Uncategorized` when none are provided).
- Booking guidance updated (`book-entries`, `conventions.md`, `ledger-beancount.md`) to prefer the accountant's chart.

### Fixed
- Scripts (`init_folders`, `init_beancount`, `reports`) now open the config with a context manager instead of leaking the file handle.
- `config_get.py` prints YAML-style `true`/`false` for booleans (and an empty line for null) so shell callers can compare values reliably.
- `claims_tracker.py` now errors clearly when an `--item` contains extra `|` separators instead of silently mis-parsing the row.

## [0.4.0] and earlier

Initial onboarding-driven release: interview → per-user config; Finance Inbox filing; configurable ledger (Beancount or simple); optional related-party, claims, payment-plan, bill-reminders, brand-output, and integrations modules. (Predates this changelog.)
