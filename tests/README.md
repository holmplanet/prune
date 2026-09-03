# Tests

Run the protocol and adapter conformance suite from the repository root:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Install the test dependency first with `python3 -m pip install -r requirements-dev.txt`.
The same checks run in GitHub Actions for pushes and pull requests.

The suite validates the checked-in example against the ChangeSpec contract, exercises
CompletionSpec status boundaries, and detects stale Codex adapter output.
