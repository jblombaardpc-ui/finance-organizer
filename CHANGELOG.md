# Changelog

All notable changes to the finance-organizer plugin are recorded here.
This project uses [semantic versioning](https://semver.org/).

## [0.6.0] — 2026-07-01

Audit-fix release: script correctness, doc accuracy, and packaging.

### Fixed
- `append_rename_ledger.py` now logs the md5 for `delete`/`dedupe-delete` rows too (when the file still exists at logging time — log before deleting); previously those rows always got a blank md5, weakening duplicate detection for re-downloaded files.
- `reports.py` no longer silently falls back to the global `ledger.beancount_main` when a set has no `ledger_main` — it now exits with a clear "add one under sets_of_books" error, so a report can never be built from the wrong entity's ledger.
- `reports.py` simple backend tolerates formatted amounts (`"1,200"`, `"$45.00"`) via the same `num()` cleaner used by `build_payment_plan.py`; `references/ledger-simple.md` now documents the simple ledger as **CSV-only** (the `.xlsx` mention is gone).
- `claims_tracker.py` validates **all** `--item` arguments before writing any rows, so a bad item can no longer leave a partial append in the tracker.
- `init_beancount.py` escapes double quotes (and backslashes) in the set label used in `option "title" "…"`.
- `init_folders.py` now matches `references/conventions.md`: business sets get a top-level `Receipts/` folder (previously `Expenses/Receipts`), and when the config has an `overlap` section it creates `overlap.personal_card_expense_copies_dir` plus its `Candidates (pending review)/` subfolder that file-inbox relies on.
- `references/ledger-beancount.md`: the fallback Python validator one-liner was broken (`from beancount import loader,sys` → ImportError); replaced with a tested working one-liner that also exits non-zero on errors.
- `skills/bill-reminders/SKILL.md` no longer uses Google-specific `overrideReminders` wording — event reminders are described provider-neutrally.
- `skills/finance-onboard/SKILL.md`: the ledger step now says `pip install beancount --break-system-packages` (matching every script's error message), and the prior-financials step notes that set folders are scaffolded later in step 4 (create `Reports/` early if needed).

### Changed
- **Breaking (script):** `build_payment_plan.py --limit` is now **required** (the `6000` default is gone) so the daily limit always comes from `config.payment_plan.daily_limit`; added an optional `--skip-weekends` flag that shifts Sat/Sun payment dates to the next Monday.
- `references/config-schema.md`: defined the **primary set** (the first entry in `sets_of_books`, used for default tracker paths); marked `filing.rename_ledger_per_set`, `accounts[].owner`, and `integrations.bank_feed` as **reserved — not yet read by any skill**.
- `skills/flag-expense/SKILL.md` gained the standard "if there's no config, run finance-onboard first" line the other core skills have.
- Docs: `EXPLAINER.md` now includes **bill-reminders** in the architecture diagram, the skills table (12 skills), and the trimmed config example; `finance-organizer/README.md` dependencies list `pyyaml` (required by the config-driven scripts) and `pypdf` (required by `split_scan.py`); install wording unified to "Settings → Capabilities → Plugins"; `.plugin` references point at the actual packaged file.

### Added
- Packaged plugin file `finance-organizer-0.6.0.plugin` at the repo root (zip of the `finance-organizer/` directory, excluding `__pycache__`/`.DS_Store`).
- Repo-root `.gitignore` (`__pycache__/`, `*.pyc`, `.DS_Store`, …).

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
