import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_document(relative_path):
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    return json.loads(text) if relative_path.endswith(".json") else yaml.safe_load(text)


def validate(instance, schema, path="$"):
    expected = schema.get("type")
    type_matches = {
        "object": isinstance(instance, dict),
        "array": isinstance(instance, list),
        "string": isinstance(instance, str),
    }
    if expected in type_matches and not type_matches[expected]:
        raise AssertionError(f"{path}: expected {expected}")

    if "enum" in schema and instance not in schema["enum"]:
        raise AssertionError(f"{path}: value is not allowed")
    if isinstance(instance, str) and len(instance) < schema.get("minLength", 0):
        raise AssertionError(f"{path}: string is too short")

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                raise AssertionError(f"{path}: missing {key}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            unknown = set(instance) - set(properties)
            if unknown:
                raise AssertionError(f"{path}: unknown properties {sorted(unknown)}")
        for key, value in instance.items():
            if key in properties:
                validate(value, properties[key], f"{path}.{key}")
    elif isinstance(instance, list):
        for index, value in enumerate(instance):
            validate(value, schema.get("items", {}), f"{path}[{index}]")


class ProtocolSchemaTests(unittest.TestCase):
    def test_example_bugfix_matches_change_spec_schema(self):
        validate(
            load_document("examples/bugfix.yaml"),
            load_document("protocol/schemas/change-spec.schema.json"),
        )

    def test_change_spec_rejects_unknown_fields(self):
        change = {
            "objective": "test",
            "scope": {"allowed_files": [], "forbidden_changes": []},
            "structure": {
                "existing_patterns": [],
                "reusable_modules": [],
                "proposed_interfaces": [],
                "schema_changes": [],
            },
            "implementation": {"smallest_secure_design": "test"},
            "verification": {"tests": []},
            "unexpected": True,
        }
        with self.assertRaises(AssertionError):
            validate(change, load_document("protocol/schemas/change-spec.schema.json"))

    def test_completion_spec_accepts_each_status(self):
        schema = load_document("protocol/schemas/completion-spec.schema.json")
        for status in ("complete", "blocked", "question", "review", "error"):
            validate({"status": status}, schema)

    def test_completion_spec_rejects_unknown_status(self):
        with self.assertRaises(AssertionError):
            validate(
                {"status": "done"},
                load_document("protocol/schemas/completion-spec.schema.json"),
            )


class AdapterConformanceTests(unittest.TestCase):
    def test_codex_adapter_is_generated_and_current(self):
        result = subprocess.run(
            [sys.executable, "scripts/build_codex_adapter.py", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_codex_adapter_declares_protocol_boundary(self):
        adapter = (
            ROOT
            / "adapters/codex/secure-agent-protocol/skills/secure-agent-protocol/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("GENERATED FILE", adapter)
        self.assertIn("Codex adapter boundary", adapter)
        self.assertIn("# Priority Order", adapter)
        self.assertIn("1. Security", adapter)


if __name__ == "__main__":
    unittest.main()
