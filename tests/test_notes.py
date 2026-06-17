from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cairn.validate import validate_vault
from cairn.vault import init_vault


def run_cairn(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run(
        [sys.executable, "-m", "cairn", *args],
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class NotesTests(unittest.TestCase):
    def test_cli_add_creates_valid_note_with_slug(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_vault(root, profile_name="engineering")

            result = run_cairn(
                root,
                "add",
                "--title",
                "Deploy 403 Fix",
                "--type",
                "Runbook",
                "--description",
                "Fix deploy authorization failures.",
                "--tag",
                "bug",
                "--tag",
                "deploy",
                "--system",
                "ci",
                "--signal",
                "http 403",
                "--body",
                "Rotate the CI token and verify workspace access.",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("knowledge/deploy-403-fix.md", result.stdout)
            created = root / "knowledge" / "deploy-403-fix.md"
            self.assertTrue(created.is_file())
            text = created.read_text(encoding="utf-8")
            self.assertIn("type: Runbook", text)
            self.assertIn("tags: [bug, deploy]", text)
            self.assertIn("systems: [ci]", text)
            self.assertEqual(validate_vault(root).errors, [])

    def test_cli_capture_alias_creates_note(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_vault(root, profile_name="personal")

            result = run_cairn(
                root,
                "capture",
                "--title",
                "Weekly workflow",
                "--description",
                "Personal workflow note.",
                "--tag",
                "workflow",
                "--body",
                "Review open loops every Friday.",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "knowledge" / "weekly-workflow.md").is_file())

    def test_cli_add_rejects_folder_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "vault"
            init_vault(root, profile_name="personal")

            result = run_cairn(
                root,
                "add",
                "--title",
                "Outside",
                "--description",
                "Should not escape the vault.",
                "--tag",
                "personal",
                "--folder",
                "..",
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("path must stay inside vault", result.stderr)
            self.assertFalse((root.parent / "outside.md").exists())

    def test_cli_update_appends_text_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_vault(root, profile_name="personal")
            run_cairn(
                root,
                "add",
                "--title",
                "Support handoff",
                "--description",
                "Workflow note.",
                "--tag",
                "workflow",
                "--body",
                "Initial note.",
            )

            first = run_cairn(root, "update", "knowledge/support-handoff.md", "--append", "Add reproduction steps.")
            second = run_cairn(root, "update", "knowledge/support-handoff.md", "--append", "Add reproduction steps.")

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            text = (root / "knowledge" / "support-handoff.md").read_text(encoding="utf-8")
            self.assertEqual(text.count("Add reproduction steps."), 1)
            self.assertIn("unchanged", second.stdout)


if __name__ == "__main__":
    unittest.main()
