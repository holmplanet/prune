import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

from scripts.validate_protocol import load_document, validate_document


ROOT = Path(__file__).resolve().parents[1]


class ProtocolSchemaTests(unittest.TestCase):
    def test_manifest_matches_schema_and_declares_existing_files(self):
        manifest = load_document(ROOT / "protocol/manifest.json")
        validate_document(
            ROOT / "protocol/manifest.json",
            ROOT / "protocol/schemas/manifest.schema.json",
        )
        for relative_path in manifest["schemas"] + manifest["policies"] + manifest["modes"]:
            self.assertTrue((ROOT / "protocol" / relative_path).is_file(), relative_path)

    def test_example_bugfix_matches_change_spec_schema(self):
        validate_document(
            ROOT / "examples/bugfix.yaml",
            ROOT / "protocol/schemas/change-spec.schema.json",
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
        schema = load_document(ROOT / "protocol/schemas/change-spec.schema.json")
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(change)

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
        schema = load_document(ROOT / "protocol/schemas/change-spec.schema.json")
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate(change)

    def test_completion_spec_accepts_each_status(self):
        schema = load_document(ROOT / "protocol/schemas/completion-spec.schema.json")
        for status in ("complete", "blocked", "question", "review", "error"):
            Draft202012Validator(schema).validate({"status": status})

    def test_completion_spec_rejects_unknown_status(self):
        schema = load_document(ROOT / "protocol/schemas/completion-spec.schema.json")
        with self.assertRaises(ValidationError):
            Draft202012Validator(schema).validate({"status": "done"})


class AdapterConformanceTests(unittest.TestCase):
    def test_protocol_cli_validates_example(self):
        result = subprocess.run(
            [
                sys.executable,
                "scripts/validate_protocol.py",
                "examples/bugfix.yaml",
                "--schema",
                "protocol/schemas/change-spec.schema.json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

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
        self.assertIn("## Modes", adapter)
        self.assertIn("# Bugfix Mode", adapter)
        self.assertIn("Add a regression test when practical.", adapter)
        manifest = load_document(ROOT / "protocol/manifest.json")
        self.assertIn(f"version: {manifest['protocol_version']}", adapter)


if __name__ == "__main__":
    unittest.main()
