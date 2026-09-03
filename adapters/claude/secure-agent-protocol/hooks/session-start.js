#!/usr/bin/env node
// Secure Agent Protocol — Claude Code SessionStart / SubagentStart hook.
//
// Emits the generated protocol skill as hidden session context, so the protocol governs every
// session without relying on the model electing to invoke the skill.
//
// It READS the generated skill rather than carrying its own copy of the protocol. The repo's
// rule is that adapters must not redefine the contract locally, and a second copy here would be
// exactly that — plus a copy that `build_claude_adapter.py --check` could not detect as stale.
//
// Fails OPEN by design: a missing or unreadable skill file exits 0 with empty output. A broken
// protocol file must not make Claude Code unusable, and a non-zero exit here would surface as a
// hook error on every single session start.

'use strict';

const fs = require('fs');
const path = require('path');

// `CLAUDE_PLUGIN_ROOT` is set by Claude Code when it runs a plugin hook. The `..` fallback keeps
// the hook runnable directly (e.g. `node hooks/session-start.js`) for local testing.
const pluginRoot = process.env.CLAUDE_PLUGIN_ROOT || path.resolve(__dirname, '..');
const skillPath = path.join(pluginRoot, 'skills', 'secure-agent-protocol', 'SKILL.md');

/** Strips the YAML frontmatter block that Claude Code parses separately from the skill body. */
function stripFrontmatter(text) {
  if (!text.startsWith('---')) return text;
  // Match only a frontmatter block that is closed. An unterminated `---` means the file is
  // malformed; returning it whole is safer than silently discarding the entire protocol.
  const closing = text.indexOf('\n---', 3);
  if (closing === -1) return text;
  const afterClosing = text.indexOf('\n', closing + 1);
  return afterClosing === -1 ? '' : text.slice(afterClosing + 1);
}

function readEventName() {
  // Claude Code passes hook input as JSON on stdin. Read it to echo the correct event name back,
  // since this same script serves both SessionStart and SubagentStart.
  try {
    const raw = fs.readFileSync(0, 'utf8');
    if (!raw.trim()) return 'SessionStart';
    const parsed = JSON.parse(raw);
    return typeof parsed.hook_event_name === 'string' ? parsed.hook_event_name : 'SessionStart';
  } catch {
    // No stdin, not JSON, or no such field — the event name is cosmetic here, so default rather
    // than fail and lose the protocol injection.
    return 'SessionStart';
  }
}

function main() {
  let body;
  try {
    body = stripFrontmatter(fs.readFileSync(skillPath, 'utf8')).trim();
  } catch {
    process.stdout.write('{}');
    return;
  }

  if (!body) {
    process.stdout.write('{}');
    return;
  }

  process.stdout.write(
    JSON.stringify({
      systemMessage: 'SECURE AGENT PROTOCOL ACTIVE',
      hookSpecificOutput: {
        hookEventName: readEventName(),
        additionalContext: body,
      },
    }),
  );
}

main();
