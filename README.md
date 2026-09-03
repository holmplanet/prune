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

## What changes in a PR

The protocol makes the work behind a PR explicit before implementation. For example, a request to add a webhook endpoint might look like this without the protocol:

```text
Add POST /webhooks/stripe.

- Added a route and controller.
- Parsed the request body and saved the event.
- Updated the README.
```

The same PR using the protocol would narrow the scope, identify the trust boundary, and make failure behavior and verification visible:

```text
Add POST /webhooks/stripe with replay protection.

ChangeSpec
- Objective: accept verified Stripe events exactly once.
- Allowed files: webhook route, event schema, event store, focused tests.
- Trust boundary: raw HTTP request and Stripe signature header are untrusted.
- Security: verify the signature against the raw body; reject missing or invalid
  signatures; never log the signing secret or raw sensitive payload.
- Structure: extend the existing request-validation and event-store abstractions;
  do not add a generic webhook framework.
- Invariants: an event ID is processed at most once; persistence failure returns
  a retryable error without acknowledging the event.
- Verification: valid, invalid, expired, duplicate, malformed, and persistence-
  failure cases; formatter, type check, lint, and full test suite.

Implementation
- Added the route, schema validation, signature verification, and idempotency
  check at the boundary.
- Kept provider-specific behavior in the Stripe adapter.

Verification
- Tests: 9 passed, including duplicate and invalid-signature regressions.
- Checks: formatter, type check, lint, and security scan passed.

COMPLETE
Fixed Stripe webhook intake in [files].
Cause: the endpoint previously had no authenticated or idempotent boundary.
Verified: focused tests and repository checks above.
```

The second example is not just a longer description: it records the contract that reviewers need to evaluate security, correctness, scope, and completion.
