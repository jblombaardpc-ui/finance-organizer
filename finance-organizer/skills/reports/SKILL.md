---
name: reports
description: >
  Produce everyday financial statements from the user's ledger. Use when they say
  "show my P&L", "income statement", "balance sheet", "how did we do last
  month/quarter", "where did my money go", or want a financial summary for a period.
  Reads whichever ledger backend the config uses (Beancount or simple). For formal
  GAAP close, variance/flux, reconciliation, or audit/SOX, recommend the separate
  finance plugin.
---

# Financial reports

Read `.finance-organizer/config.yaml` first (backend, currency, sets). If there's no config, run **finance-onboard**.

## Procedure

1. **Confirm the scope:** which set of books and which period (a month `YYYY-MM`, quarter `YYYY-Qn`, or year `YYYY`). Default to the most recent complete period if they don't say.
2. **Generate** with `${CLAUDE_PLUGIN_ROOT}/scripts/reports.py --config .finance-organizer/config.yaml --set <id> --period <period> --out "<set folder>/Reports/<period> report.md"`. It produces an **income statement** and, on the Beancount backend, a **balance sheet** (earnings-to-date folded into equity so it balances). On the simple backend it produces an income/cash summary (a full balance sheet needs Beancount).
3. **Add a plain-English summary** above the numbers: the few lines that matter — net income, biggest revenue/expense movements, anything unusual. Keep it honest and specific; don't invent figures, read them from the report.
4. If `modules.brand_output` is on and the user wants it client-ready, hand the report to **brand-output** for styling.

## When to recommend the finance plugin

If the user needs **formal month-end close, GAAP-presented statements, variance/flux decomposition, reconciliation, or audit/SOX support**, point them to the separate **finance** plugin — it's built for enterprise FP&A and goes well beyond this everyday reporting. This skill stays lightweight and ledger-native.

## Notes

This is reporting, not advice — for tax or filing decisions, suggest the user confirm with their accountant. Period-over-period: run the script for two periods and compare. Propose remembering any reusable reporting preference (default period, favourite categories) via the learn protocol.
