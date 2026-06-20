---
name: related-party
description: >
  Track related-party flows and reimbursements between a user's entities. Use when
  the user mentions a related company/person they fund or get funded by, says
  "reimbursement owed", "due from [party]", "we paid [related co]'s bill", or when
  inbox routing finds a payment from one of their accounts to a related party's
  card/account. Enabled when config.modules.related_party is true.
---

# Related-party & reimbursements

Read `.finance-organizer/config.yaml` → `related_parties[]` and `overlap`. This generalizes the pattern where a business funds (or is funded by) a related company/person, and where one entity's money sometimes pays another's bill.

## What to do

1. **Regular flows.** When the user funds a related party (e.g. a monthly contribution), book it per their config/accountant treatment (often a draw or due-to/from, not an expense). Confirm the treatment once, then remember it (learn protocol).
2. **Misdirected / cross-paid items.** When funds from one of the user's accounts pay a **related party's** card or bill (look up the party's `cards[]` in config), that's a **reimbursement owed**. Do **not** silently rebook it — use the **flag-expense** skill to:
   - annotate the ledger entry, and
   - add a row to `<set folder>/Reports/Reimbursements & Flags.md` (#, date, payer account, party/card, amount, status).
3. **Detection tip.** A recurring "card/LOC payment" debit from the user's account that matches a credit on a related party's card by date+amount is the tell. Confirm with the user before treating it as owed.
4. **Report.** Summarize total owed to/from each related party and what's outstanding.

## Boundaries

Never reclassify reconciled figures on your own — flag and let the user (or their accountant) action it. Propose any new related party or rule for saving via the learn protocol.
