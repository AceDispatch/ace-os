# ACE-OS Starter Kit

Drop the contents of this folder into your working directory
(e.g. C:\Users\nineo\OneDrive\Desktop\Ace Dispatch\Claude), then:

1. Open Claude Code in that folder (Code tab: select it as the project
   folder; or cmd: cd into it, run `claude`). It auto-loads CLAUDE.md.
2. Connect HubSpot MCP to Claude Code (read-only use per the constitution).
3. Copy .env.example to .env and add Aircall API credentials
   (Aircall Dashboard -> Integrations & API).
4. First run: drop a census CSV into inbox/ and say
   "Run the Lead Intake Pipe per contracts/01-lead-intake-pipe.md".

Folder map:
  CLAUDE.md    the constitution — every session inherits it
  contracts/   one contract per agent; agents do exactly this, nothing more
  skills/      methodology (ported verbatim from claude.ai skills) — READ ONLY to agents
  inbox/       inputs land here
  outbox/      all agent outputs, dated
  logs/        one run log per run — the system's episodic memory
  scripts/     shared parts (aircall_pull.py)
