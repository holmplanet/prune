# Abstraction Policy

Think in reusable concepts, not reusable-looking code.

1. Reuse an existing abstraction.
2. Extend it when the new behavior belongs to the same concept and boundary.
3. Extract a genuinely repeated domain or security concept.
4. Keep one-off behavior local and explicit.
5. Reject speculative generic frameworks.

An abstraction needs a clear name, narrow responsibility, stable inputs and outputs, and more than one credible use in the current project. Centralize security rules, domain invariants, normalization, and repeated integration behavior.
