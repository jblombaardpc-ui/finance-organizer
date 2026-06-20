---
name: payment-plan
description: >
  Build a payment plan that respects a daily transfer limit, and schedule it. Use when
  the user drops invoices to pay or says "build a payment plan", "schedule these
  payments", "how should I pay these within my daily limit". Batches invoices
  oldest-first within the configured daily limit, saves a plan, and adds calendar
  reminders. Enabled when config.modules.payment_plan is true.
---

# Payment plan + reminders

Read `.finance-organizer/config.yaml` → `payment_plan` (daily_limit, currency, calendar_id).

## Procedure

1. **Collect** the invoices to pay (invoice #, date, description, amount; GST/tax if relevant). If they came from the inbox, file them first (file-inbox) and log them.
2. **Build the schedule** with `${CLAUDE_PLUGIN_ROOT}/scripts/build_payment_plan.py --invoices <csv|json> --limit <daily_limit> --start-date YYYY-MM-DD --out "<plan.md>" --batch-name "<name>"`. It batches oldest-first within the daily limit, one invoice per row, a day total per batch, and a running balance.
3. **Save the plan** somewhere sensible in the relevant set's folder (e.g. `<set folder>/Payment Plans/`).
4. **Add calendar events** on the user's calendar (`payment_plan.calendar_id`): one per payment day, listing that day's invoices, amount, and running balance; mark the final day's event as the last one.

## Finish

Report the number of payment days, daily amounts, total, and date range, and confirm the plan path + that events were created. If a single invoice exceeds the daily limit, call it out (it will occupy its own day and still exceed the cap).
