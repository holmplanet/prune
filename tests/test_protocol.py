import json
import os
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

    def test_claude_adapter_is_generated_and_current(self):
        result = subprocess.run(
            [sys.executable, "scripts/build_claude_adapter.py", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_claude_adapter_declares_protocol_boundary(self):
        adapter = (
            ROOT
            / "adapters/claude/secure-agent-protocol/skills/secure-agent-protocol/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("GENERATED FILE", adapter)
        self.assertIn("Claude adapter boundary", adapter)
        self.assertIn("# Priority Order", adapter)
        self.assertIn("1. Security", adapter)
        self.assertIn("## Modes", adapter)
        self.assertIn("# Bugfix Mode", adapter)
        self.assertIn("Add a regression test when practical.", adapter)
        manifest = load_document(ROOT / "protocol/manifest.json")
        self.assertIn(f"version: {manifest['protocol_version']}", adapter)


class ClaudePluginPackagingTests(unittest.TestCase):
    """The Claude adapter is a local plugin, so its manifests are part of the contract."""

    PLUGIN = ROOT / "adapters/claude/secure-agent-protocol"

    def test_plugin_manifest_points_at_an_existing_hooks_file(self):
        plugin = load_document(self.PLUGIN / ".claude-plugin/plugin.json")
        self.assertEqual(plugin["name"], "secure-agent-protocol")
        hooks_relative = plugin["hooks"].lstrip("./")
        self.assertTrue((self.PLUGIN / hooks_relative).is_file(), plugin["hooks"])

    def test_marketplace_manifest_declares_the_plugin(self):
        marketplace = load_document(self.PLUGIN / ".claude-plugin/marketplace.json")
        names = [entry["name"] for entry in marketplace["plugins"]]
        self.assertIn("secure-agent-protocol", names)

    def test_hooks_register_session_start_against_an_existing_script(self):
        hooks = load_document(self.PLUGIN / "hooks/claude-hooks.json")["hooks"]
        self.assertIn("SessionStart", hooks)
        commands = [
            hook["command"]
            for event in hooks.values()
            for entry in event
            for hook in entry["hooks"]
        ]
        self.assertTrue(commands)
        for command in commands:
            # Every hook command must reference a script that actually ships in the plugin;
            # a typo here fails silently at session start, where nobody is watching.
            self.assertIn("${CLAUDE_PLUGIN_ROOT}", command)
            script = command.split("${CLAUDE_PLUGIN_ROOT}/")[1].rstrip('"')
            self.assertTrue((self.PLUGIN / script).is_file(), script)

    def test_session_start_hook_emits_the_protocol_as_additional_context(self):
        result = subprocess.run(
            ["node", "hooks/session-start.js"],
            cwd=self.PLUGIN,
            input='{"hook_event_name":"SessionStart"}',
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        context = payload["hookSpecificOutput"]["additionalContext"]
        self.assertEqual(payload["hookSpecificOutput"]["hookEventName"], "SessionStart")
        # Frontmatter is parsed by Claude Code separately; injecting it would be noise.
        self.assertFalse(context.startswith("---"))
        self.assertIn("# Priority Order", context)
        self.assertIn("Claude adapter boundary", context)

    def test_session_start_hook_fails_open_when_the_skill_is_missing(self):
        # A broken protocol file must not make Claude Code unusable: a non-zero exit would
        # surface as a hook error on every session start.
        result = subprocess.run(
            ["node", "hooks/session-start.js"],
            cwd=self.PLUGIN,
            input="{}",
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, "CLAUDE_PLUGIN_ROOT": str(ROOT / "tests/does-not-exist")},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {})


if __name__ == "__main__":
    unittest.main()
