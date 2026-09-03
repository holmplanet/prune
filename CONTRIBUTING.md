# Contributing

Thanks for contributing to Prune Protocol.

## Before opening an issue or pull request

- Check existing issues and pull requests.
- Keep changes focused.
- Preserve `protocol/` as the canonical source of truth.
- Do not hand-edit generated adapter skills.
- Do not include secrets, credentials, private prompts, or sensitive fixtures.

## Development

Create a virtual environment and install the development dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Run the full test and validation commands before opening a pull request:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/validate_protocol.py examples/bugfix.yaml --schema protocol/schemas/change-spec.schema.json
python scripts/validate_protocol.py protocol/manifest.json --schema protocol/schemas/manifest.schema.json
python scripts/build_codex_adapter.py --check
python scripts/build_claude_adapter.py --check
git diff --check
```

If you change a canonical protocol file, regenerate both adapters and include the generated output
in the same change:

```bash
python scripts/build_codex_adapter.py
python scripts/build_claude_adapter.py
```

## Pull requests

Use the repository pull request template. Explain the objective, scope, security considerations,
structure and abstraction choices, implementation, verification, and exclusions. Keep comments
short and evidence-based.

## License

By contributing, you agree that your contributions are provided under the MIT License in
[`LICENSE`](LICENSE).
