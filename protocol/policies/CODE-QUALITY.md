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
- Avoid comments by default. Add one only when the intent or constraint cannot be made clear
  through names, structure, or tests.
- Use explicit error types or the repository's established error contract. Preserve useful
  context without exposing secrets.
- Tests should be fast, independent, repeatable, and self-validating. Test observable behavior,
  failure paths, and important boundaries rather than implementation trivia.

Do not optimize for line count, perceived cleverness, or arbitrary coverage targets. A small
change is good when it is complete, understandable, and verifiable.
