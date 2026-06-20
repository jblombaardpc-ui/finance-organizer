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
related-party · claims-helper · payment-plan · brand-output   ← optional modules
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
| **payment-plan** *(opt)* | "build a payment plan" | Batch invoices within a configurable daily transfer limit; save a plan; add calendar reminders. |
| **brand-output** *(opt)* | "make an invoice/report" | Apply the captured branding to generated documents. |
| **learn** | something new worth remembering | Propose adding a new rule/mapping to `memory.md` (or config) — always with confirm-before-save. |

## Config

Everything is driven by `.finance-organizer/config.yaml` in the user's working folder. See `references/config-schema.md` (schema) and `references/config.example.yaml` (a worked example). Conventions live in `references/conventions.md`; ledger setup in `references/ledger-beancount.md` and `references/ledger-simple.md`; the learning protocol in `references/learning.md`.

## Dependencies

- `bean-check` (Beancount) when the Beancount backend is chosen — onboarding can `pip install beancount` in the sandbox.
- `openpyxl` for spreadsheet outputs; `pdftotext` (poppler) for content-level dedup (optional).
- Calendar steps use the user's connected calendar.
- *Optional:* the **finance** plugin for advanced close / GAAP statements / variance / audit — the built-in `reports` skill covers everyday statements.

Scripts in `scripts/` take paths/values as arguments — no hardcoded machine paths — so the plugin is portable across computers and users.
