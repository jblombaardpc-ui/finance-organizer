# Learning protocol — confirm before saving

The organizer gets better as it learns the user's specifics, but it must **never silently remember things**. Any skill that discovers a durable fact follows this protocol.

## When to propose remembering something

Trigger when you encounter something that will recur and isn't already in the config/memory, e.g.:
- a vendor → category mapping you had to decide ("Acme Supplies → Office Supplies"),
- a new account, card, or set of books,
- a routing/business-vs-personal rule the user corrected you on,
- a related party, a tax detail, or a filing-convention tweak,
- any decision you'd otherwise have to re-derive next time.

## How to propose

1. State the new fact in one line.
2. Say exactly **what you'll write and where** — a `config.yaml` field (structured facts: accounts, modules, tax, sets of books) or a dated bullet in `memory.md` (judgement calls, mappings, decisions).
3. Ask: *"Want me to remember this?"* Only write on a clear yes.

## Where things live

- **`.finance-organizer/config.yaml`** — structured configuration (see `config-schema.md`). Update the relevant field.
- **`.finance-organizer/memory.md`** — human-readable learned knowledge, grouped under headings and dated:

```
# Finance Organizer — learned knowledge

## Vendors & categories
- 2026-06-20 — Acme Supplies → Expenses:Office Supplies (business set)

## Accounts
- ...

## Conventions & routing
- ...

## Tax
- ...

## Decisions
- ...
```

## Rules

- One clear fact per entry; date it.
- Never store secrets — no passwords, tokens, or full card numbers (last 4 only).
- On a **return session**, read `config.yaml` + `memory.md` first so you apply what was learned.
- If the user later contradicts a remembered fact, show the old vs new and update on confirmation — don't keep both.
