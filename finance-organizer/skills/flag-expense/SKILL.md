---
name: flag-expense
description: >
  Flag (annotate) a transaction for later review without rebooking it. Use when the
  user says "flag that as…", "mark this as due from [party]", "flag for
  reclassification", or wants something noted but not yet changed. Flagging means
  annotate and leave the numbers as-booked until the user confirms — never silently
  rebook.
---

# Flag a transaction (annotate, don't rebook)

When the user asks to "flag" something they mean **note it for later review, not change the numbers**. Leave the entry as-booked so reconciled figures don't move until they confirm. Read `.finance-organizer/config.yaml` for the relevant accounts/parties. If there's no config, run **finance-onboard** first.

## Apply in BOTH places

1. **In the ledger:**
   - Beancount — above the entry add a comment and tag: `;; FLAG: <vendor> <amount> — <reason>; <suggested treatment>; left as-booked pending confirmation.` and a `#flag-...` tag on the transaction line.
   - Simple ledger — set a `flag` note on the row (e.g. `notes: FLAG: due from <party> — pending`).
2. **In a flags doc:** `<set folder>/Reports/Reimbursements & Flags.md` — add a row: #, date, vendor, account paid from, currently-booked account, amount, status. Bump its "Last updated" date.

## Then

- Validate (Beancount: `bean-check`).
- **Offer** to do the actual reclassification and refresh affected periods — but don't do it unprompted. The user (or their accountant) actions reclassifications after review.

## Why

Flagging keeps an audit trail without disturbing reconciled figures, and lets the user confirm before the books change. Related-party reimbursements use this — see the **related-party** module.
