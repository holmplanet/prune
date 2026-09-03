# Codex Adapter

This is the installable Codex plugin for the protocol. The adapter skill is intentionally concise; the normative schemas and policies live in the repository root under `protocol/`.

Regenerate the skill after changing canonical protocol files:

```bash
python3 scripts/build_codex_adapter.py
python3 scripts/build_codex_adapter.py --check
```

Do not hand-edit the generated `skills/prune/SKILL.md`.
