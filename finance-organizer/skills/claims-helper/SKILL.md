---
name: claims-helper
description: >
  Maintain a per-period benefit/health claim (e.g. a health-spending account / PHSP).
  Use when a benefit-eligible out-of-pocket bill is filed, or the user says "add this
  to my claim", "update my claim form", "fill in my health spending claim". Adds line
  items to the current period's claim tracker and carries it forward each period.
  Enabled when config.modules.claims_helper is true.
---

# Benefit / health claims helper

Read `.finance-organizer/config.yaml` → `claims` (plan_name, eligible[], ineligible[], admin_fee_pct, tax_on_fee_pct, form_path, period_end).

## Eligibility first

Add only **eligible** out-of-pocket amounts (config `eligible`), e.g. amounts not covered by other insurance, prescriptions, dental, vision. Exclude anything in `ineligible` (e.g. cosmetics, gym) and note what you excluded. If a document mixes both, claim only the eligible portion.

## Procedure

1. Find the current period's tracker at `claims.form_path` (substitute the period). If none exists for this period, create it.
2. Add a line per eligible expense with `${CLAUDE_PLUGIN_ROOT}/scripts/claims_tracker.py --tracker "<path>" --item "Patient|YYYY-MM-DD|Description|Amount|Y" --admin-fee-pct <config> --tax-on-fee-pct <config>`. It appends the row and reports Total Claim, admin fee, tax, and total payable.
3. Report the new totals and anything excluded as ineligible.

## Period rollover

At each new period (config `period_end`), start a fresh tracker for the new period and carry the template/structure forward. Offer to set a reminder to submit before `period_end` (a calendar event or scheduled task). Propose remembering any new eligibility decision via the learn protocol.
