# Finance Organizer — Cowork plugin (shareable)

An onboarding-driven finance organizer for individuals and small businesses. It interviews the user about how their finances are set up, then keeps a **Finance Inbox** tidy and the **books** current — adapting to *their* company structure, accounts, locality/tax, and branding rather than anyone's hardcoded setup. It's built to handle the common reality that personal and business accounts overlap.

This is a self-contained marketplace holding one plugin, **`finance-organizer`**. Nothing here touches anyone's live books — a user's data and settings live in a `.finance-organizer/` folder inside *their own* working folder, created during onboarding.

## Setup

This is a standard `SKILL.md` plugin/marketplace, so it works on any agent that supports the SKILL.md (AgentSkills) standard. After installing, say **"set up my finances"** to start onboarding.

### Claude (Cowork / desktop)

- **Marketplace (recommended):** open **Settings → Capabilities → Plugins**, add a marketplace **from a repository**, and point it at this GitHub repo. Then install **finance-organizer**.
- **Or the packaged file:** install `finance-organizer-0.6.0.plugin` (at the repo root) directly (Settings → Capabilities → Plugins → upload a custom plugin).

See Anthropic's [Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude).

### Hermes (Nous Research)

Hermes follows the SKILL.md standard and can consume Claude-compatible marketplaces.

- Add this repository as a skills source through Hermes' **Skills Hub / marketplace**, **or** clone the repo and copy the skill folders from `finance-organizer/skills/` into your Hermes skills directory.
- Confirm the exact command for your Hermes version in the [Hermes skills docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills).

### OpenClaw

OpenClaw discovers any `SKILL.md` under a configured skills root.

- **Whole bundle (recommended):** clone this repo, then add its skills folder to `skills.load.extraDirs` in `~/.openclaw/openclaw.json` — OpenClaw picks up every skill automatically:

  ```json5
  { skills: { load: { extraDirs: ["<cloned-repo>/finance-organizer/skills"] } } }
  ```

- **Or per skill** (from a clone): `openclaw skills install ./finance-organizer/skills/<name> --as <name>`.

See the [OpenClaw skills docs](https://docs.openclaw.ai/tools/skills).

### Note on the bundled scripts

The skills call helper scripts via Claude's `${CLAUDE_PLUGIN_ROOT}` path variable, which Claude resolves automatically. On Hermes, OpenClaw, or any other agent, those scripts live at `finance-organizer/scripts/` in the cloned repo — point the agent there if a script path doesn't resolve on its own. (Beancount/openpyxl still install in the sandbox as described below.)

### Share with a friend

Send them this repo (or the `finance-organizer-0.6.0.plugin` file); they set it up with any of the above, then say **"set up my finances"**.

## Recommended companions (optional)

Onboarding will offer to use these if installed — they make setup richer but aren't required:

- **smb-onboard** (small-business plugin) — business-context interview + connector setup.
- **discover-brand** (brand-voice plugin) — pulls brand guidelines from connected platforms.

## First run

Say **"set up my finances"** / **"get me started"** → the `finance-onboard` skill walks through company structure, accounts, overlap rules, locality & tax, ledger choice (Beancount recommended; it can be installed automatically), branding, and which optional modules to turn on. It writes everything to `.finance-organizer/` (with your approval) and offers a nightly inbox routine.

See `finance-organizer/README.md` for the skill list and `finance-organizer/references/config-schema.md` for the config contract.

## License

MIT — see [LICENSE](LICENSE). Free to use, modify, and share. Keep your own `.finance-organizer/` data private (it's gitignored).
