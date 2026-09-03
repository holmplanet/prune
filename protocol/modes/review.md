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
