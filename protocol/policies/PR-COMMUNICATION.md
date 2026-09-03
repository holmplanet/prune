# PR Communication Policy

This policy applies to pull request bodies, review comments, and completion handoffs. It does not require README or product documentation to use the same format.

Write in a stoic style:

- Keep sentences short, direct, and informative.
- State one fact, decision, or result per sentence.
- Remove filler, hype, repetition, and unnecessary hedging.
- Prefer bullets for lists and short paragraphs for reasoning.
- Lead with the problem, cause, fix, verification, or scope decision.
- Make comments useful. Add intent, constraints, evidence, or an action. Do not restate the diff.

Tables are opt-in:

- Use a table only for exact comparisons, repeated field mappings, or state transitions where it materially improves comprehension.
- Do not use tables for generic summaries of objective, scope, implementation, or verification.
- A table should reduce reading effort. If prose or bullets are clearer, use them.

Keep the PR surface smaller than the internal ChangeSpec. Publish the conclusions a reviewer needs, not every planning field.
