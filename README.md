# Secure Agent Protocol

A harness-agnostic protocol for secure, schema-first, clean AI-assisted software work.

The protocol prioritizes:

```text
security -> correctness -> structure -> reuse -> minimal implementation -> concise handoff
```

The core lives under `protocol/`. Integrations for Codex, Pi, Claude, CI, and other runtimes live under `adapters/`.

## Repository shape

- `protocol/schemas/` — versioned machine-readable contracts.
- `protocol/policies/` — stable engineering policies.
- `protocol/modes/` — task-specific workflows.
- `adapters/` — harness-specific renderers and integrations.
- `examples/` — valid protocol instances.
- `tests/` — schema and adapter conformance tests.

The first adopter is Codex. Pi is a later adapter. Neither owns the source of truth.

## Status

Early design and protocol prototype. The repository is private while the workflow is validated on real coding tasks.
