---
name: learn
description: >
  Remember a new finance fact, rule, or preference — with confirmation. Use when the
  user says "remember that…", "save this", "from now on…", "always/never do X", or
  when any finance-organizer skill discovers something durable (a vendor's category, a
  new account, a corrected routing, a tax detail) that should persist. Never saves
  silently — always confirms first.
---

# Learn (confirm before saving)

Follow `../../references/learning.md`. The point: the organizer should get smarter over time without ever remembering things behind the user's back.

## Procedure

1. **State the fact** in one line.
2. **Say where it goes:** a structured `config.yaml` field (accounts, modules, tax, sets of books, related parties) or a dated bullet in `.finance-organizer/memory.md` (vendor→category mappings, judgement calls, routing rules, decisions).
3. **Ask "want me to remember this?"** Write only on a clear yes.
4. **Write it:** update the config field, or append a dated, grouped bullet to `memory.md`. Show what you wrote.

## Rules

- One clear fact per entry; date memory bullets.
- Never store secrets — no passwords, tokens, or full card numbers (last 4 only).
- If the user contradicts a remembered fact later, show old vs new and replace it on confirmation — don't keep both.
- On a return session, read `config.yaml` + `memory.md` first so what was learned actually gets applied.
