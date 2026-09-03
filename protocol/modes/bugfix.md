# Bugfix Mode

1. Reproduce or identify the failing behavior.
2. Define the smallest secure ChangeSpec.
3. Locate the owning module, schema, and existing test pattern.
4. Add a regression test when practical.
5. Make the narrowest complete change.
6. Inspect the full diff and run applicable checks.
7. Return a concise completion status.

Do not mix unrelated cleanup, broad refactors, new dependencies, or public API changes into a focused bug fix unless the ChangeSpec requires them.
