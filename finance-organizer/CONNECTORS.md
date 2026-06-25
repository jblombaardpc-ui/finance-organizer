# Connectors

This plugin is **tool-agnostic**: it works with whatever financial tools you connect, referenced by *category* rather than a specific product. In skill files, `~~category` is a placeholder for the tool you've linked in that category.

## How tool references work

A skill might say "pull recent invoices from `~~payments`." At runtime that means *whichever* payments tool you've connected (Square, Stripe, PayPal, …). You record your choices in `.finance-organizer/config.yaml` under `integrations`, and onboarding sets this up with you.

## Categories

| Category | Placeholder | Examples |
|---|---|---|
| Accounting | `~~accounting` | QuickBooks, Xero |
| Payments / POS | `~~payments` | Square, Stripe, PayPal |
| Bank feed | `~~bank` | bank/aggregator feeds, where available |
| Calendar | `~~calendar` | Google Calendar, Microsoft Outlook / Office 365, Apple/other (whichever calendar connector you've linked) |

## Calendar (reminders & payment plans)

The **bill-reminders** and **payment-plan** skills (and claims-submission reminders) write events to `~~calendar` — whatever calendar tool you've connected. It works the same whether that's **Google Calendar** or **Microsoft Outlook / Office 365**; the skill calls your connected calendar's create/list/update-event tools rather than any one provider's API.

You record your choice in `config.yaml` under `calendar` (`provider`, `id`, `timezone`). A **dedicated "Finance" calendar** is recommended so money events stay separate from your main calendar. The plugin **does not create the calendar for you** — most calendar connectors can add events but not new calendars — so onboarding walks you through creating the Finance calendar in your provider, then captures its id.

## Connecting a tool

1. Link the tool through your agent's connector settings — in Claude: **Settings → Connectors** (or the Customize → Connectors area). On other agents, use their connector/MCP configuration.
2. List it in `config.yaml` under `integrations` (onboarding does this).
3. The **sync-financials** skill then uses it.

**The plugin never connects a tool on your behalf** — it only uses connectors you've already linked. If a skill needs a connector you haven't linked, it will tell you and stop rather than guess.
