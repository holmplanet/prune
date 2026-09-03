---
name: secure-agent-protocol
description: "Apply the Secure Agent Protocol to Codex coding work: security first, schema and structure before implementation, reusable abstractions, minimal secure code, and concise fixed-format handoffs. Use when coding, debugging, refactoring, reviewing, or auditing a repository."
metadata:
  version: 1.0.0
---

<!-- GENERATED FILE. Edit protocol/ and run scripts/build_codex_adapter.py. -->

Apply the canonical protocol below. Before editing, inspect the repository and form a compact ChangeSpec. The ChangeSpec must include `objective`, `scope`, `security`, `structure`, `abstraction`, `implementation`, `verification`. Do not print a long plan unless asked.

```yaml
change:
  objective:
  scope:
    allowed_files: []
    forbidden_changes: []
  security:
    trust_boundaries: []
    untrusted_inputs: []
    sensitive_data: []
    authorization_rules: []
    failure_behavior:
  structure:
    existing_patterns: []
    reusable_modules: []
    proposed_interfaces: []
    schema_changes: []
  abstraction:
    stable_concept:
    existing_abstraction_to_extend:
    new_abstraction_justified: false
    reason:
  implementation:
    smallest_secure_design:
  verification:
    security_checks: []
    tests: []
    type_check:
    lint:
```

# Priority Order

Apply these priorities in order:

1. Security
2. Correctness
3. Clear structure
4. Reusable abstractions
5. Minimal implementation
6. Concise communication

Less code is valuable only when it preserves security, correctness, clarity, and behavior. The goal is reduced accidental surface area, not code golf.

# Security-First Policy

For work involving users, permissions, authentication, authorization, network calls, files, commands, secrets, payments, personal data, or external input:

- Identify trust boundaries and treat external input as untrusted.
- Validate at the boundary using the existing schema pattern.
- Enforce authorization server-side near the protected operation.
- Never expose secrets or sensitive data in logs, errors, URLs, client bundles, or fixtures.
- Fail closed when identity, authorization, validation, or required dependencies are unavailable.
- Avoid widening permissions, redirects, filesystem scope, command scope, or network access without explicit need.
- Add regression tests for security-sensitive behavior when practical.

# Abstraction Policy

Think in reusable concepts, not reusable-looking code.

1. Reuse an existing abstraction.
2. Extend it when the new behavior belongs to the same concept and boundary.
3. Extract a genuinely repeated domain or security concept.
4. Keep one-off behavior local and explicit.
5. Reject speculative generic frameworks.

An abstraction needs a clear name, narrow responsibility, stable inputs and outputs, and more than one credible use in the current project. Centralize security rules, domain invariants, normalization, and repeated integration behavior.

# Minimal-Code Policy

Before adding code, check in this order:

1. Does this need to exist?
2. Can the repository's existing code solve it?
3. Can the standard library solve it?
4. Can the platform or framework solve it?
5. Can an installed dependency solve it?
6. Can a smaller clear abstraction solve it?
7. Write the minimum secure implementation that remains readable and verifiable.

Do not add a dependency, wrapper, configuration layer, abstraction, compatibility path, or future-facing extension without a demonstrated requirement. Never remove meaningful validation, error handling, tests, accessibility, or security controls merely to reduce line count.

# Completion Policy

Every task ends with one primary status:

- `COMPLETE`
- `BLOCKED`
- `QUESTION`
- `REVIEW`
- `ERROR`

Default completion:

```text
COMPLETE
Fixed [problem] in [file].
Cause: [cause].
Verified: [checks].
```

Use only the fields that apply. Keep the default handoff to two or three sentences. Expand only when the user asks for explanation, architecture, review detail, or an audit.

## Verification gate

Inspect the full diff. Check for scope drift, duplicate logic, dead code, accidental API changes, secrets, unsafe logging, and weakened security. Run applicable formatting, lint, type, test, and security checks. Do not claim completion when required verification failed.

## Codex adapter boundary

This file is generated from `protocol/`. Keep Codex-specific packaging here, but edit canonical behavior only under `protocol/`.
