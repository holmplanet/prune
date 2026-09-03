# Claude Adapter

Translates the neutral protocol into a **local Claude Code plugin**. Claude-specific packaging
belongs here; the canonical schemas and policies remain under `protocol/`.

## What Claude Code expects

A plugin is a directory containing a `.claude-plugin/` manifest dir:

| Path | Role |
|---|---|
| `.claude-plugin/plugin.json` | Plugin identity, and a `hooks` pointer to a hooks config file |
| `.claude-plugin/marketplace.json` | Lets the directory be added as a local marketplace and installed |
| `skills/<name>/SKILL.md` | **Auto-discovered** — skills are conventional, not declared in `plugin.json` |
| `hooks/claude-hooks.json` | Hook registrations, keyed by event name |

Hook commands resolve `${CLAUDE_PLUGIN_ROOT}`, and a hook communicates by writing JSON to stdout:

```json
{
  "systemMessage": "shown to the user",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "injected into the model's context"
  }
}
```

## How this adapter is wired

One generated artifact — `skills/prune/SKILL.md` — reaches Claude two ways:

1. **As a skill.** Auto-discovered, so the protocol is invocable by name.
2. **As always-on session context.** `hooks/claude-hooks.json` registers `session-start.js` on
   `SessionStart` (matching `startup|resume|clear|compact`) and on `SubagentStart`. The hook reads
   that same `SKILL.md` at runtime, strips its frontmatter, and emits the body as
   `additionalContext`.

The hook reads the generated file rather than embedding its own copy of the protocol. A second
copy would violate the repo's rule that adapters must not redefine the contract locally, and it
would be a copy that `build_claude_adapter.py --check` could not detect as stale.

The hook **fails open**: a missing or unreadable skill file exits 0 with `{}`. A broken protocol
file must not make Claude Code unusable, and a non-zero exit would surface as a hook error on
every session start.

## Build

```bash
python scripts/build_claude_adapter.py           # regenerate
python scripts/build_claude_adapter.py --check   # fail if stale (CI gate)
```

## Install locally

```bash
/plugin marketplace add /absolute/path/to/prune/adapters/claude/prune
/plugin install prune
```

Then restart the session (or `/clear`) so `SessionStart` fires. `systemMessage` should report
`PRUNE ACTIVE`.

To verify the hook in isolation, without Claude Code:

```bash
echo '{"hook_event_name":"SessionStart"}' \
  | node adapters/claude/prune/hooks/session-start.js
```
