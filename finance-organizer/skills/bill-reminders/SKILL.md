---
name: bill-reminders
description: >
  Track recurring statement due dates and minimum payments, and put reminders on the
  user's calendar ahead of each. Use when the user says "track my payment due dates",
  "remind me when bills are due", "when are my cards/loans due", "set up bill
  reminders", or after new statements are filed. Reads the latest statement per
  credit/loan account, extracts the due date + minimum payment + balance, maintains a
  Payments Due tracker, and creates calendar reminders (lead time configurable;
  manual accounts say "pay", pre-authorized accounts say "ensure funds"). Enabled when
  config.modules.bill_reminders is true. Distinct from payment-plan, which schedules
  paying down a one-off batch of invoices.
---

# Bill reminders — recurring due dates + minimum payments

Read `.finance-organizer/config.yaml` → `bill_reminders` (`calendar_id`, `lead_days`,
`accounts[]`, `refresh`, optional `tracker_path`) and the global `accounts[]` map.
Operate on the user's working folder. This is a **read-only** pass over statements — it
never books or moves money; it only reads statements and writes a tracker doc + calendar
events.

## What this is (and isn't)

This tracks **recurring obligations** — the minimum payment and due date that print on
each monthly credit-card / line-of-credit statement, and the fixed instalment on each
loan — and reminds the user ahead of time. It does **not** pay anything, and it is
separate from **payment-plan** (which batches a one-off pile of invoices within a daily
transfer limit). Reminders are the floor (the minimum); most users pay cards in full —
say so in the event so the minimum isn't mistaken for the amount to pay.

## Procedure

1. **Pick the accounts.** From `bill_reminders.accounts[]`, take each account flagged for
   reminders. Each entry references a `last4` from the global account map and carries a
   `mode`:
   - `manual` — revolving cards and lines of credit the user pays by hand → reminder verb **"Pay"**.
   - `auto_debit` — loans / bills on pre-authorized debit → reminder verb **"Ensure funds for"** (the payment happens automatically; the risk is an empty account).
   If `accounts[]` is empty, offer to infer a starting list from the global map
   (`role: card` / `loc` → manual; `role: loan` / fixed instalments → auto_debit) and
   confirm it with the user before saving via the **learn** protocol.

2. **Read the latest statement for each.** In that account's statement folder (e.g.
   `<set folder>/Bank Statements/<account name>/`), open the most recent statement PDF and
   extract:
   - revolving cards / LOC → **payment due date**, **minimum payment**, **new balance**;
   - loans → **next payment date** and **fixed payment amount** (from the loan/account-detail
     statement).
   Statement layouts vary by bank, so read the PDF and pull these fields directly rather
   than assuming a fixed format. If the latest statement is older than ~35 days (or
   missing), flag that the data may be stale and that a newer statement should be filed.

3. **Update the tracker.** Maintain a single "Payments Due" table at
   `bill_reminders.tracker_path` (default `Reports/Payments Due.md` in the primary set, or
   a sensible per-set location). One row per account: account, set, balance, minimum / fixed
   payment, due date, mode, and the statement date it came from. Overwrite the row for an
   account each time you refresh it.

4. **Create the calendar reminders.** On `bill_reminders.calendar_id`, create one event per
   account, `lead_days` (default 3) **before** the due date, at ~09:00 local time:
   - title: `Pay <account> — due <Mon D>` (manual) or `Ensure funds: <account> — auto-debit <Mon D>` (auto_debit);
   - description: balance, minimum (or fixed) payment, exact due date, the source statement date, and the "minimum is the floor — you normally pay in full" note for revolving accounts;
   - `overrideReminders`: a popup the day before (1440 min) and at start (0 min).
   If a reminder for the same account + due date already exists, update it rather than
   duplicating. Keep events short (15 min) and use the calendar's local timezone.

5. **Keep it current (refresh).** Honour `bill_reminders.refresh`, captured at onboarding:
   - `recurring` — ensure a scheduled task exists that re-runs this skill on
     `bill_reminders.refresh_cron` (e.g. monthly, a few days after statements typically land)
     so due dates never go stale as new statements are filed. Create it if missing.
   - `on_demand` — do nothing extra; the user re-runs the skill (or it runs after file-inbox
     files a new statement).

## Finish

Report the accounts covered, each due date + amount, the tracker path, how many calendar
events were created/updated, and the refresh mode. Call out any account whose statement is
stale or missing, and any account in the global map that has no reminder configured yet
(offer to add it via **learn**).
