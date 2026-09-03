# Prune Protocol

A harness-agnostic protocol for secure, schema-first, clean AI-assisted software work.

The protocol gives an agent a repeatable contract for planning, implementation, review, and
completion:

```text
security -> correctness -> structure -> reuse -> minimal implementation -> concise handoff
```

The canonical source is `protocol/`. Adapters translate it for specific agent runtimes. They do
not define a second source of truth.

## What the protocol covers

### ChangeSpec

Before editing, an agent forms a compact ChangeSpec. The JSON Schema requires these areas:

- Objective.
- Scope, including allowed files and forbidden changes.
- Security, including trust boundaries, untrusted inputs, sensitive data, authorization, and failure behavior.
- Structure, including existing patterns, reusable modules, proposed interfaces, and schema changes.
- Abstraction, including whether a new abstraction is justified.
- Implementation, including the smallest secure design, behavior contract, invariants, edge cases, side effects, and compatibility constraints.
- Verification, including security checks, tests, type checking, and linting.

The examples at [`examples/`](examples/) are valid ChangeSpec instances:

- `bugfix.yaml` — expired refresh-token reuse.
- `feature.yaml` — verified, idempotent billing webhook ingestion.
- `review.yaml` — file-upload security review before release.

### Policies

The protocol applies these priorities and policies:

- Security first.
- Correctness before structure and reuse.
- Clear, narrow abstractions.
- Minimal implementation without weakening validation or error handling.
- Explicit code quality standards.
- Short, direct PR communication.
- Concise completion statuses: `COMPLETE`, `BLOCKED`, `QUESTION`, `REVIEW`, or `ERROR`.

The PR communication policy requires useful comments and handoffs that state intent, constraints,
evidence, or action. It favors prose and bullets. Tables are reserved for comparisons, mappings,
or state transitions where they materially improve comprehension.

### Task modes

The protocol defines workflows for:

- **Bugfixes:** reproduce the defect, add a regression test when practical, make the narrowest complete change, and verify it.
- **Features:** define observable behavior, identify invariants and edge cases, implement the smallest complete design, and verify all applicable checks.
- **Reviews:** trace inputs through side effects and failures, inspect security and structure, run checks, and report findings without rewriting code unless requested.

## Repository layout

- `protocol/manifest.json` — protocol version and the canonical file list.
- `protocol/schemas/` — JSON Schema contracts for ChangeSpec, CompletionSpec, and the manifest.
- `protocol/policies/` — priority, security, abstraction, minimal-code, code-quality, PR communication, and completion policies.
- `protocol/modes/` — bugfix, feature, and review workflows.
- `adapters/` — runtime-specific skills, plugins, hooks, and packaging.
- `examples/` — valid protocol documents.
- `scripts/` — adapter generators, protocol validation, and PR-body checks.
- `tests/` — schema, guardrail, adapter, packaging, and hook conformance tests.
- `.github/workflows/` — repository CI and PR guardrails.

The manifest currently declares protocol version `1.2.0`.

## Adapters

### Codex

The Codex adapter is the first adopter. It packages the generated protocol skill as an installable
Codex plugin at `adapters/codex/prune/`.

The generated skill lives at:

```text
adapters/codex/prune/skills/prune/SKILL.md
```

It is generated from `protocol/` and must not be hand-edited.

### Claude Code

The Claude adapter is a local Claude Code plugin at `adapters/claude/prune/`.
Install it from a local marketplace:

```text
/plugin marketplace add /absolute/path/to/prune/adapters/claude/prune
/plugin install prune
```

The generated skill reaches Claude in two ways:

1. It is auto-discovered as `skills/prune/SKILL.md`.
2. The `SessionStart` and `SubagentStart` hooks read the same file and inject it as session context.

The hook fails open with `{}` if the skill is missing or unreadable, so a broken protocol file does
not make Claude Code unusable. To test the hook directly:

```bash
echo '{"hook_event_name":"SessionStart"}' \
  | node adapters/claude/prune/hooks/session-start.js
```

### Pi

The Pi adapter directory is reserved for a later integration. It must consume the neutral protocol
rather than define a second contract.

## Pull request guardrails

The PR template asks for these sections:

- Objective
- Scope
- Security
- Structure and abstraction
- Implementation
- Verification
- Not in scope

The guardrail workflow checks that each section contains meaningful content. It updates one bot
comment with the result and fails the job when required sections are missing. The guardrail checks
structure only. Repository CI remains responsible for tests and security checks.

## Local development

The project requires Python with the development dependencies in `requirements-dev.txt`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Run the full conformance suite:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

Validate protocol documents:

```bash
python scripts/validate_protocol.py \
  examples/bugfix.yaml \
  --schema protocol/schemas/change-spec.schema.json

python scripts/validate_protocol.py \
  protocol/manifest.json \
  --schema protocol/schemas/manifest.schema.json
```

Regenerate and check the runtime adapters:

```bash
python scripts/build_codex_adapter.py
python scripts/build_codex_adapter.py --check

python scripts/build_claude_adapter.py
python scripts/build_claude_adapter.py --check
```

Check a PR body locally:

```bash
python scripts/check_pr_body.py < pull-request-body.md
```

The command prints a JSON array of missing sections. An empty array means the body satisfies the
structural guardrail.

## Continuous integration

GitHub Actions runs the conformance suite on pushes and pull requests against Python 3.11, 3.12,
and 3.13. CI installs `requirements-dev.txt`, validates the example and manifest, checks both
generated adapters, and runs `git diff --check`.

The separate PR guardrail workflow runs on pull request edits and enforces the required review
contract.

## Contributing

Contributions are welcome. Keep `protocol/` as the canonical source of truth and regenerate both
adapters when canonical files change. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the development
checks and pull request expectations.

Report security vulnerabilities privately. See [`SECURITY.md`](SECURITY.md).

## License

Prune Protocol is available under the [MIT License](LICENSE).

## Status

The protocol is an experimental open-source project. Codex and Claude adapters are implemented. Pi
remains reserved for future work.
