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
