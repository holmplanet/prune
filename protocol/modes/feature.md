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
