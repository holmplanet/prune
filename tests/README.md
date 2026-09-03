# Tests

Run the protocol and adapter conformance suite from the repository root (requires PyYAML
to read the checked-in YAML example):

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The suite validates the checked-in example against the ChangeSpec contract, exercises
CompletionSpec status boundaries, and detects stale Codex adapter output.
