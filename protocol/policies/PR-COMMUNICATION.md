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

## Shell-safe transport

Treat PR bodies, review comments, commit messages, and other Markdown passed to a shell as data.

- Never pass multiline Markdown through a shell command's `--body` argument. Use stdin or a body file so the shell cannot interpret backticks, `$()`, quotes, or newlines.
- For GitHub CLI, pass multiline content with `--body-file` and a body-file path:

  ```sh
  gh pr edit 123 --body-file /path/to/pr-body.md
  ```

- Use `--body-file -` with a single-quoted heredoc only when the full command path is known to forward stdin unchanged. A command proxy may consume or rewrite stdin; use its explicit passthrough mode or a body-file path instead.
- Do not escape newlines into literal `\n` text.
- Run the repository's PR-body checker against the exact payload before submitting when one exists.
- After creating or editing a PR, read the submitted body back and confirm headings, line breaks, and inline code rendered as intended.
- Before executing a command, inspect arguments for accidental interpolation and secret exposure.
