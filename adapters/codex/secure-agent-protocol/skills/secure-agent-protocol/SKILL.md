---
name: secure-agent-protocol
description: "Apply the Secure Agent Protocol to Codex coding work: security first, schema and structure before implementation, reusable abstractions, minimal secure code, and concise fixed-format handoffs. Use when coding, debugging, refactoring, reviewing, or auditing a repository."
metadata:
  version: 1.1.0
---

<!-- GENERATED FILE. Edit protocol/ and run scripts/build_codex_adapter.py. -->

Apply the canonical protocol below. Before editing, inspect the repository and form a compact ChangeSpec. The ChangeSpec must include `objective`, `scope`, `security`, `structure`, `abstraction`, `implementation`, `verification`. Complete the implementation quality fields when they apply to the task. Do not print a long plan unless asked.

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
    behavior_contract: []
    invariants: []
    edge_cases: []
    side_effects: []
    compatibility_constraints: []
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

# Code Quality Policy

Code should be easy to understand, test, change, and remove. These are review heuristics,
not absolute rules; security, correctness, and the repository's established conventions take
precedence.

- Use names that communicate intent and use the same vocabulary for the same concept.
- Keep functions and modules focused on one responsibility and one level of abstraction.
- Prefer explicit control flow, inputs, outputs, and failure behavior over clever shortcuts.
- Keep side effects at clear boundaries and avoid hidden mutation or shared state.
- Prefer high cohesion and low coupling; do not extract a generic abstraction without a second
  credible use.
- Avoid flags or options that make one function perform unrelated behaviors; split the behavior
  when the boundary is real.
- Remove duplication when a stable domain abstraction exists, but tolerate local duplication
  when an abstraction would couple unrelated domains.
- Treat comments as explanations of intent, constraints, or non-obvious decisions. Do not use
  comments to excuse unclear code.
- Use explicit error types or the repository's established error contract. Preserve useful
  context without exposing secrets.
- Tests should be fast, independent, repeatable, and self-validating. Test observable behavior,
  failure paths, and important boundaries rather than implementation trivia.

Do not optimize for line count, perceived cleverness, or arbitrary coverage targets. A small
change is good when it is complete, understandable, and verifiable.

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

## Modes

# Bugfix Mode

1. Reproduce or identify the failing behavior.
2. Define the smallest secure ChangeSpec.
3. Locate the owning module, schema, and existing test pattern.
4. Add a regression test when practical.
5. Make the narrowest complete change.
6. Inspect the full diff and run applicable checks.
7. Return a concise completion status.

Do not mix unrelated cleanup, broad refactors, new dependencies, or public API changes into a focused bug fix unless the ChangeSpec requires them.

# Feature Mode

Use for adding or materially changing product behavior.

1. Define the observable behavior and acceptance conditions before editing.
2. Identify domain invariants, important edge cases, side effects, and compatibility constraints.
3. Locate the owning module, schema, existing abstraction, and established test pattern.
4. Choose names, boundaries, and interfaces that make the behavior easy to understand.
5. Write focused tests for the contract and important failure paths when practical.
6. Implement the smallest complete change with explicit error behavior.
7. Review the diff for unclear responsibilities, hidden mutation, duplication, dead code,
   speculative abstractions, and scope drift.
8. Run applicable tests, type checks, lint, formatting, and security checks.

Do not add unrelated cleanup, broad refactors, new dependencies, or compatibility layers unless
the behavior contract requires them.

# Review Mode

Use for evaluating existing or agent-written code without assuming it is correct because it
compiles or has tests.

1. Establish the intended behavior, trust boundaries, and compatibility constraints.
2. Trace the changed code from inputs through side effects to outputs and failures.
3. Check security controls, authorization, validation, error handling, and sensitive-data paths.
4. Check names, responsibility boundaries, abstraction levels, coupling, duplication, and hidden
   mutation.
5. Check tests for observable behavior, negative paths, boundaries, independence, and repeatability.
6. Run the repository's applicable checks and inspect the complete diff.
7. Report findings by severity with file locations, impact, and a concrete fix or verification
   needed. Do not rewrite code unless requested.

## Verification gate

Inspect the full diff. Check for scope drift, duplicate logic, dead code, accidental API changes, secrets, unsafe logging, and weakened security. Run applicable formatting, lint, type, test, and security checks. Do not claim completion when required verification failed.

## Codex adapter boundary

This file is generated from `protocol/`. Keep Codex-specific packaging here, but edit canonical behavior only under `protocol/`.
