---
name: finance-onboard
description: >
  Onboarding for the finance-organizer plugin — Claude as the setup guide. Use when
  the user says "set up my finances", "get me started", "onboard me", "configure the
  finance organizer", when they first install the plugin, or whenever no
  `.finance-organizer/config.yaml` exists yet in their working folder. Interviews the
  user about their company structure, sets of books, account map, personal/business
  overlap, locality & tax, ledger choice, branding, and which optional modules to turn
  on, then writes a per-user config + memory with their approval and offers a nightly
  inbox routine.
---

# Finance Organizer — onboarding

Be the friendly setup guide. The goal: in one conversational pass, learn enough about the user's finances to drive every other skill, and write it to `.finance-organizer/` in their working folder. Ask **one thing at a time**, keep it plain-language, and **never write anything without showing it first and getting a yes**.

Read `../../references/config-schema.md` (the contract you're filling), `../../references/learning.md` (the confirm-before-save rule), and `../../references/conventions.md`.

## 0. Return-session check

If `.finance-organizer/config.yaml` already exists, do **not** re-interview. Load it (and `memory.md`), show the current profile, ask what's changed, and update only those fields (through the learn protocol). Otherwise continue.

## 1. Welcome + recommend companions

Greet briefly and say what onboarding will cover (structure → accounts → overlap → locality/tax → ledger → branding → modules), ~15 minutes.

Mention two optional companions and offer to let the user install them — **guide, never install on their behalf**:
- **smb-onboard** (small-business plugin) — a deeper business-context interview and connector setup.
- **discover-brand** (brand-voice plugin) — pulls brand guidelines from their connected platforms.
- **finance** (finance plugin) — *optional, power users only* — formal month-end close, GAAP statements, variance/flux, reconciliation, and audit/SOX. The built-in **reports** skill covers everyday statements, so only suggest this if they want enterprise-grade reporting.

If any are already installed, use them at the relevant step. If not, proceed without — onboarding is self-sufficient.

## 2. Interview (one question at a time)

Wait for a full answer before the next question. Map answers onto the config schema.

1. **Company structure → sets of books.** Start with two explicit counts: **(a) how many companies/businesses should I keep track of?** and **(b) how many household members?** Together these define the sets of books — one **business** set per company, and one **personal** set per household member you want tracked. Then, for each set, capture a label, business vs personal, and fiscal year-end (businesses vary; personal is usually Dec 31) → `sets_of_books[]`; and record the household size + names → `household`. Most small operators have at least one business + one personal set, and household members often share accounts — call that overlap out as normal (handled in step 3 and the account map).
2. **Account map.** Walk through their accounts: last 4 digits, a friendly name, which set it belongs to, and its role (operating / savings / card / line-of-credit / tax). Capture joint accounts and any personal cards used for business — these are where overlap happens. Never store full card numbers; last 4 only. → `accounts[]`.
3. **Personal/business overlap.** Explain the pattern plainly: when the business pays a personal cost (or vice-versa), it's tracked as a loan between the owner and the business rather than an expense. Capture the account names they (or their accountant) want to use → `overlap`. If they have an accountant with preferences, note to ask them.
4. **Locality & tax.** Country, region, currency. Tax registrations (GST/HST, VAT, sales tax): number, rate, filing cadence. Ask them to describe any local rules in their own words → `tax`. If smb-onboard ran, reuse what it captured. Do not assert tax law you're unsure of — record what they tell you and flag anything to confirm with their accountant.
5. **Ledger choice.** Recommend **Beancount** (plain-text, auditable, and you can set it up for them — `pip install beancount` in the sandbox and scaffold a starter ledger with `scripts/init_beancount.py`). Offer the **simple** spreadsheet/CSV ledger for non-technical users. Set `ledger.backend` and create the starter ledger per `../../references/ledger-beancount.md` or `../../references/ledger-simple.md`.
6. **Branding.** If discover-brand is installed, offer to run it and save results to `.finance-organizer/brand.md`. Otherwise do a 3-question intake (logo location, colors, voice/tone) — or skip. Used by the brand-output module.
7. **Optional modules.** Explain each in one line and ask which to enable → `modules`:
   - related-party & reimbursements, health/benefit claims, payment plans + reminders, brand-aware outputs.
   For each enabled module, ask the few extra fields it needs (e.g. claims: plan name + eligible/ineligible lists + period end; payment-plan: daily transfer limit + calendar).

## 3. Write the config (approval gate)

Show the **full** drafted `config.yaml` (and the `brand.md` summary) before writing. Wait for explicit approval. Then write:
- `.finance-organizer/config.yaml`
- `.finance-organizer/memory.md` (seed it with a dated "Setup" note summarizing key decisions)
- `.finance-organizer/brand.md` (if branding captured)

Confirm: "Saved — every finance-organizer skill will now use this."

## 4. Set up the structure + ledger

Now that the config exists, lay everything out so documents have a home and stay organised:
- **Folders:** run `${CLAUDE_PLUGIN_ROOT}/scripts/init_folders.py --config .finance-organizer/config.yaml` to scaffold the Finance Inbox + a tidy tree for each set of books. It's idempotent — re-run it any time the structure drifts.
- **Ledger:** create the chosen ledger so they leave ready to book. Beancount → install it and scaffold with `${CLAUDE_PLUGIN_ROOT}/scripts/init_beancount.py --config .finance-organizer/config.yaml --set <id> --out "<set folder>/Beancount"`, then validate. Simple → create the ledger CSV with the agreed columns.

## 5. Keep-it-organised workflow + what to try

Set up the ongoing routine that keeps the structure tidy with no effort: offer to create a **recurring scheduled task** that runs the **file-inbox** skill (e.g. nightly at 10pm, the `cadence.inbox_processing` cron) so anything dropped in the Finance Inbox is automatically triaged into the right folders and books. On these unattended runs it flags anything ambiguous instead of guessing. Also offer a weekly check-in phrase and a monthly **reports** cadence. Then tell them what to try now: drop documents in the Finance Inbox and say **"clear my inbox"**, **"book last month"**, or **"show my P&L"**.

## 6. Learning, going forward

Tell them: as you work together, when something new comes up (a vendor's category, a new account, a rule), you'll **ask before saving it** to their config/memory — nothing is remembered silently. See `../../references/learning.md`.

## Approval gates (always)

- Show the config/profile draft before writing; wait for a yes.
- Never overwrite an existing config silently — show current vs proposed.
- Never install a plugin or connect a tool on the user's behalf; guide them to do it.
