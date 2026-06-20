# Finance Organizer — Cowork plugin (shareable)

An onboarding-driven finance organizer for individuals and small businesses. It interviews the user about how their finances are set up, then keeps a **Finance Inbox** tidy and the **books** current — adapting to *their* company structure, accounts, locality/tax, and branding rather than anyone's hardcoded setup. It's built to handle the common reality that personal and business accounts overlap.

This is a self-contained marketplace holding one plugin, **`finance-organizer`**. Nothing here touches anyone's live books — a user's data and settings live in a `.finance-organizer/` folder inside *their own* working folder, created during onboarding.

## Install / share

- **On one computer:** install the packaged `finance-organizer.plugin`, or **Settings → Capabilities → Plugins → add marketplace** pointing at this repo, then install **finance-organizer**.
- **Share with a friend:** send them this repo (or the `.plugin` file). They add it the same way, then just say **"set up my finances"** to start onboarding.

## Recommended companions (optional)

Onboarding will offer to use these if installed — they make setup richer but aren't required:

- **smb-onboard** (small-business plugin) — business-context interview + connector setup.
- **discover-brand** (brand-voice plugin) — pulls brand guidelines from connected platforms.

## First run

Say **"set up my finances"** / **"get me started"** → the `finance-onboard` skill walks through company structure, accounts, overlap rules, locality & tax, ledger choice (Beancount recommended; it can be installed automatically), branding, and which optional modules to turn on. It writes everything to `.finance-organizer/` (with your approval) and offers a nightly inbox routine.

See `finance-organizer/README.md` for the skill list and `finance-organizer/references/config-schema.md` for the config contract.

## License

MIT — see [LICENSE](LICENSE). Free to use, modify, and share. Keep your own `.finance-organizer/` data private (it's gitignored).
