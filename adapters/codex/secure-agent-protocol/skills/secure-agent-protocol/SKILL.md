---
name: secure-agent-protocol
description: "Apply the Secure Agent Protocol to Codex coding work: security first, schema and structure before implementation, reusable abstractions, minimal secure code, and concise fixed-format handoffs. Use when coding, debugging, refactoring, reviewing, or auditing a repository."
metadata:
  version: 1.0.0
---

Apply the Secure Agent Protocol in this order:

```text
security -> correctness -> structure -> reuse -> minimal implementation -> concise handoff
```

Before editing, inspect the repository and form a compact ChangeSpec. Do not print a long plan unless asked.

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

## Security

- Treat external input as untrusted and validate it at the boundary.
- Enforce authorization near the protected operation.
- Never expose secrets or sensitive data in logs, errors, URLs, client bundles, or fixtures.
- Fail closed when identity, authorization, validation, or required dependencies are unavailable.
- Do not widen permissions, redirects, filesystem scope, command scope, or network access without explicit need.

## Structure and abstraction

- Find the canonical schema, type, interface, service, and source of truth before adding another.
- Reuse an existing abstraction first.
- Extend an abstraction only when the behavior belongs to the same concept and boundary.
- Extract stable repeated domain or security concepts; keep one-off behavior local.
- Reject speculative generic frameworks and catch-all helpers.
- Keep focused bug fixes focused.

## Minimal implementation

Check in this order before adding code:

1. Does this need to exist?
2. Can existing repository code solve it?
3. Can the standard library, platform, framework, or installed dependency solve it?
4. Can a smaller clear abstraction solve it?
5. Write the minimum secure implementation that remains readable and verifiable.

Less code is not a reason to remove meaningful validation, error handling, tests, accessibility, or security controls.

## Verification and handoff

Inspect the full diff. Check for scope drift, duplicate logic, dead code, accidental API changes, secrets, unsafe logging, and weakened security. Run applicable formatting, lint, type, test, and security checks; never claim completion when required verification failed.

End with one status:

```text
COMPLETE
Fixed [problem] in [file].
Cause: [cause].
Verified: [checks].
```

Use `BLOCKED`, `QUESTION`, `REVIEW`, or `ERROR` when appropriate. Keep the default handoff to two or three sentences. Expand only when asked.
