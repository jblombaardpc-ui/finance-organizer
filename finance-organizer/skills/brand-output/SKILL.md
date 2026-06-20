---
name: brand-output
description: >
  Produce finance documents (invoices, reports, summaries, statements) styled to the
  user's brand. Use when the user asks to "make an invoice", "create a report",
  "write up a summary", "put our branding on this", or wants any client-facing finance
  document. Enabled when config.modules.brand_output is true.
---

# Brand-aware outputs

Read `.finance-organizer/config.yaml` → `branding.guidelines_path` (default `.finance-organizer/brand.md`) and apply it to anything client-facing you generate.

## Procedure

1. **Load branding.** Read `brand.md` for logo location, colors, fonts, and voice/tone. If it's missing or thin and **discover-brand** is installed, offer to run it to (re)build the guidelines; otherwise do a quick 3-question intake or proceed with sensible defaults.
2. **Generate the document** the user asked for (invoice, report, summary). Pull the numbers from the ledger/config; never invent figures. Apply brand colors/logo/voice consistently. Respect the user's locality/currency from config.
3. **Output** in the format they want (PDF/DOCX/XLSX/Markdown/HTML). Save it to the relevant set's folder and show it to the user.

## Notes

Keep financial accuracy first — branding styles the presentation, it must not change the numbers. If brand guidelines conflict with a legal/tax requirement on an invoice (required fields, tax numbers), the requirement wins. Propose saving any reusable brand decision via the learn protocol.
