# Security-First Policy

For work involving users, permissions, authentication, authorization, network calls, files, commands, secrets, payments, personal data, or external input:

- Identify trust boundaries and treat external input as untrusted.
- Validate at the boundary using the existing schema pattern.
- Enforce authorization server-side near the protected operation.
- Never expose secrets or sensitive data in logs, errors, URLs, client bundles, or fixtures.
- Fail closed when identity, authorization, validation, or required dependencies are unavailable.
- Avoid widening permissions, redirects, filesystem scope, command scope, or network access without explicit need.
- Add regression tests for security-sensitive behavior when practical.
