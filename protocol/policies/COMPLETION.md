# Completion Policy

Every task ends with one primary status:

- `COMPLETE`
- `BLOCKED`
- `QUESTION`
- `REVIEW`
- `ERROR`

Default completion:

```text
COMPLETE. Fixed [problem]. Verified [checks].
```

Use only the fields that apply. Prefer the smallest complete handoff.

- Routine success: one sentence, normally no more than 20 words.
- Routine verification: lead with the answer, then state the decisive check.
- Failures, blockers, questions, and reviews: include only the cause, impact, finding, or next action needed.
- Expand beyond three sentences only when the user asks for explanation or the task requires risk, architecture, review detail, or an audit.
- Do not restate the investigation, tool calls, or unchanged context in the handoff.

For trivial checks, use this shape:

```text
Yes. [Result]. Verified [decisive check].
```

The response contract is represented by `CompletionSpec.response` when structured output is used. Its default is `minimal` verbosity and at most three sentences.
