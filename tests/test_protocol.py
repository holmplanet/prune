import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_document(relative_path):
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    return yaml.safe_load(text)


def assert_valid(instance, schema):
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=str)
    if errors:
        messages = "\n".join(error.message for error in errors)
        raise AssertionError(messages)


class ProtocolSchemaTests(unittest.TestCase):
    def test_example_bugfix_matches_change_spec_schema(self):
        assert_valid(
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
            assert_valid(change, load_document("protocol/schemas/change-spec.schema.json"))

    def test_change_spec_requires_security_and_abstraction(self):
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
        }
        with self.assertRaises(AssertionError):
            assert_valid(change, load_document("protocol/schemas/change-spec.schema.json"))

    def test_completion_spec_accepts_each_status(self):
        schema = load_document("protocol/schemas/completion-spec.schema.json")
        for status in ("complete", "blocked", "question", "review", "error"):
            assert_valid({"status": status}, schema)

    def test_completion_spec_rejects_unknown_status(self):
        with self.assertRaises(AssertionError):
            assert_valid(
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
