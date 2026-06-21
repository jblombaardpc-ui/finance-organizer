---
name: sync-financials
description: >
  Pull data from the user's connected financial tools into the inbox/ledger flow.
  Use when they say "sync my Square / Stripe / PayPal", "import my sales/invoices",
  "pull my card payments", "sync QuickBooks/Xero", "reconcile against my accounting",
  or on a scheduled financial sync. Tool-agnostic — works with whichever connectors
  the user has linked. Enabled when config.modules.integrations is true.
---

# Sync from connected financial tools

Read `.finance-organizer/config.yaml` → `integrations` (and `../../CONNECTORS.md`). This skill is **tool-agnostic**: `~~payments` and `~~accounting` mean whichever products the user linked (Square/Stripe/PayPal; QuickBooks/Xero). If `modules.integrations` is off or nothing is linked, there's nothing to do — say so.

**Never link a connector on the user's behalf.** If a needed tool isn't connected, tell them to link it via their connector settings (see `CONNECTORS.md`) and stop.

## Payments / POS (`~~payments`: Square, Stripe, PayPal, …)

1. Pull recent invoices / sales / payouts from the connected payments MCP.
2. For each, create an income document filed per the convention into the right **business** set's `Income/` folder (e.g. an invoices subfolder), and **dedup by the external id** (invoice/transaction number) against that set's rename ledger so repeated syncs never double-file.
3. If `modules.brand_output` is on and the user wants client copies, render a branded PDF via **brand-output**.
4. Hand the **deposit/settlement side** to **book-entries** (it remains the system of record); don't post income twice.

## Accounting (`~~accounting`: QuickBooks, Xero)

Treat the user's configured ledger (Beancount or simple) as the source of truth unless they say otherwise. Use the accounting connector to **cross-check and reconcile** — compare period totals or balances, and **flag discrepancies** (via flag-expense) rather than silently importing. Only import transactions when the user explicitly asks, and dedup by external id.

## Always

- Dedup by external id on every sync (idempotent — safe to run on a schedule).
- Summarize what was pulled, filed, reconciled, and any discrepancies flagged.
- Propose remembering new mappings (e.g. a Square item → a category) via the **learn** protocol before relying on them.
