#!/usr/bin/env python3
"""Generate the Codex adapter skill from the canonical protocol files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "protocol"
OUTPUT = ROOT / "adapters/codex/prune/skills/prune/SKILL.md"


def manifest() -> dict:
    return json.loads((PROTOCOL / "manifest.json").read_text(encoding="utf-8"))


def read_protocol_file(path: str) -> str:
    return (PROTOCOL / path).read_text(encoding="utf-8").strip()


def change_spec_fields() -> list[str]:
    schema = json.loads(
        (PROTOCOL / "schemas/change-spec.schema.json").read_text(encoding="utf-8")
    )
    return schema["required"]


def render() -> str:
    protocol_manifest = manifest()
    policies = "\n\n".join(
        read_protocol_file(path) for path in protocol_manifest["policies"]
    )
    modes = "\n\n".join(
        read_protocol_file(path) for path in protocol_manifest["modes"]
    )
    required = ", ".join(f"`{field}`" for field in change_spec_fields())
    return f'''---
name: prune
description: "Apply the Prune Protocol to Codex coding work: security first, schema and structure before implementation, reusable abstractions, minimal secure code, and concise fixed-format handoffs. Use when coding, debugging, refactoring, reviewing, or auditing a repository."
metadata:
  version: {protocol_manifest["protocol_version"]}
---

<!-- GENERATED FILE. Edit protocol/ and run scripts/build_codex_adapter.py. -->

Apply the canonical protocol below. Before editing, inspect the repository and form a compact ChangeSpec. The ChangeSpec must include {required}. Complete the implementation quality fields when they apply to the task. Do not print a long plan unless asked.

```yaml
change:
  objective:
  scope:
    allowed_files: []
    forbidden_changes: []
  security:
    trust_boundaries: []
    untrusted_inputs: []
    sensitive_data: []
    authorization_rules: []
    failure_behavior:
  structure:
    existing_patterns: []
    reusable_modules: []
    proposed_interfaces: []
    schema_changes: []
  abstraction:
    stable_concept:
    existing_abstraction_to_extend:
    new_abstraction_justified: false
    reason:
  implementation:
    smallest_secure_design:
    behavior_contract: []
    invariants: []
    edge_cases: []
    side_effects: []
    compatibility_constraints: []
  verification:
    security_checks: []
    tests: []
    type_check:
    lint:
```

{policies}

## Modes

{modes}

## Verification gate

Inspect the full diff. Check for scope drift, duplicate logic, dead code, accidental API changes, secrets, unsafe logging, and weakened security. Run applicable formatting, lint, type, test, and security checks. Do not claim completion when required verification failed.

## Codex adapter boundary

This file is generated from `protocol/`. Keep Codex-specific packaging here, but edit canonical behavior only under `protocol/`.
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if output is stale")
    args = parser.parse_args()

    rendered = render()
    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != rendered:
            raise SystemExit(f"stale generated adapter: {OUTPUT}")
        print(f"Codex adapter is up to date: {OUTPUT}")
        return

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"Generated: {OUTPUT}")


if __name__ == "__main__":
    main()
