# finance-organizer

A complete, onboarding-driven finance organizer. The onboarding interview builds a per-user config; every other skill reads it, so the same engine works for any company structure.

## How it fits together

```
finance-onboard  ──writes──>  .finance-organizer/config.yaml   (the contract)
                              .finance-organizer/memory.md      (learned knowledge)
                              .finance-organizer/brand.md       (branding)
        │
        ▼  every skill reads the config
file-inbox → book-entries → (flag-expense)        ← core
related-party · claims-helper · payment-plan · bill-reminders · brand-output   ← optional modules
learn   ← invoked by any skill when something new should be remembered
```

## Skills

| Skill | Triggers | Purpose |
|---|---|---|
| **finance-onboard** | "set up my finances", "get me started", first session | Interview → config + memory + brand; recommend companion plugins; set up the ledger; offer a nightly inbox routine. |
| **file-inbox** | "clear my inbox", "file these" | Route each document to the right set of books, name per convention, dedup via the rename ledger, clear the inbox, hand off. |
| **book-entries** | "book [month]", "do my entries", "reconcile" | Post ledger entries (Beancount or simple) per the config; validate; book when confident, flag when unsure. |
| **flag-expense** | "flag that as…" | Annotate a transaction for later review without rebooking it. |
| **reports** | "show my P&L", "balance sheet", "where did my money go" | Income statement + balance sheet + a plain-English summary from the ledger (Beancount or simple). |
| **related-party** *(opt)* | related-company flows; "reimbursement owed" | Track inter-entity contributions and reimbursements; flag misdirected payments. |
| **claims-helper** *(opt)* | a benefit-eligible bill; "add to my claim" | Maintain a per-period claims tracker/form (e.g. a health-spending account); carry forward each period. |
| **payment-plan** *(opt)* | "build a payment plan" | Batch a one-off pile of invoices within a configurable daily transfer limit; save a plan; add calendar reminders. |
| **bill-reminders** *(opt)* | "track my due dates", "remind me when bills are due", after statements are filed | Read the latest statement per credit/loan account for the due date + minimum payment, maintain a Payments Due tracker, and put reminders on the calendar ahead of each (manual = "pay", pre-authorized = "ensure funds"); optional recurring refresh. |
| **brand-output** *(opt)* | "make an invoice/report" | Apply the captured branding to generated documents. |
| **sync-financials** *(opt)* | "sync Square/QuickBooks", "import my sales/invoices" | Pull invoices/sales from connected payment tools and reconcile against accounting tools, into the inbox/ledger flow. Tool-agnostic — see `CONNECTORS.md`. |
| **learn** | something new worth remembering | Propose adding a new rule/mapping to `memory.md` (or config) — always with confirm-before-save. |

## Config

Everything is driven by `.finance-organizer/config.yaml` in the user's working folder. See `references/config-schema.md` (schema) and `references/config.example.yaml` (a worked example). Conventions live in `references/conventions.md`; ledger setup in `references/ledger-beancount.md` and `references/ledger-simple.md`; the learning protocol in `references/learning.md`.

## Dependencies

- `bean-check` (Beancount) when the Beancount backend is chosen — onboarding can `pip install beancount` in the sandbox.
- `openpyxl` for spreadsheet outputs; `pdftotext` (poppler) for content-level dedup (optional).
- Calendar steps (payment-plan, bill-reminders, claims reminders) are **provider-agnostic** — they use whatever calendar connector you've linked (Google Calendar, Microsoft Outlook / Office 365, …). Onboarding recommends a dedicated "Finance" calendar and records `provider`/`id`/`timezone` in `config.yaml` → `calendar`. See `CONNECTORS.md`.
- *Optional:* the **finance** plugin for advanced close / GAAP statements / variance / audit — the built-in `reports` skill covers everyday statements.
- *Optional:* financial connectors — QuickBooks/Xero (accounting), Square/Stripe/PayPal (payments) — for the `sync-financials` module; link them via your connector settings (see `CONNECTORS.md`).

Scripts in `scripts/` take paths/values as arguments — no hardcoded machine paths — so the plugin is portable across computers and users.
