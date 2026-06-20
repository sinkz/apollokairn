from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cairn.indexer import rebuild_index
from cairn.vault import init_vault


def run_cairn(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    env.setdefault("APOLLOKAIRN_REGISTRY_PATH", str(ROOT / ".cairn" / f"test-registry-{os.getpid()}.json"))
    return subprocess.run(
        [sys.executable, "-m", "cairn", *args],
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def write_note(root: Path, name: str = "deploy-403.md") -> str:
    rel = f"knowledge/{name}"
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        "type: Runbook\n"
        "title: Deploy 403 token rotation\n"
        "description: Fix deploy failures after token rotation.\n"
        "tags: [deploy, bug]\n"
        "timestamp: 2026-06-18T00:00:00Z\n"
        "aliases: [deploy forbidden]\n"
        "systems: [ci]\n"
        "---\n\n"
        "# Resolution\n\n"
        "Update the CI secret and rerun the failed deployment job.\n",
        encoding="utf-8",
    )
    return rel


def read_events(root: Path) -> list[dict[str, object]]:
    path = root / ".cairn" / "usage" / "events.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


class UsageTests(unittest.TestCase):
    def test_usage_is_disabled_by_default_and_does_not_log_searches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_vault(root, profile_name="engineering")
            write_note(root)
            rebuild_index(root)

            result = run_cairn(root, "search", "deploy 403")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((root / ".cairn" / "usage" / "events.jsonl").exists())

    def test_usage_enable_updates_config_gitignore_and_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_vault(root, profile_name="engineering")

            enabled = run_cairn(root, "usage", "enable", "--json")
            status = run_cairn(root, "usage", "status", "--json")

            self.assertEqual(enabled.returncode, 0, enabled.stderr)
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertTrue(json.loads(status.stdout)["enabled"])
            config = json.loads((root / ".cairn" / "config.json").read_text(encoding="utf-8"))
            self.assertIs(config["usage_tracking"], True)
            gitignore = (root / ".gitignore").read_text(encoding="utf-8")
            self.assertIn(".cairn/usage/", gitignore)
            self.assertIn(".cairn/reports/", gitignore)

    def test_usage_records_search_retrieve_write_similar_and_show_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_vault(root, profile_name="engineering")
            note_path = write_note(root)
            rebuild_index(root)
            self.assertEqual(run_cairn(root, "usage", "enable").returncode, 0)

            commands = [
                run_cairn(root, "search", "deploy 403", "--json"),
                run_cairn(root, "retrieve", "deploy 403", "--budget", "300", "--json"),
                run_cairn(root, "similar", "deploy forbidden token", "--json"),
                run_cairn(root, "show", note_path, "--json"),
                run_cairn(root, "capture", "--title", "JWT Clock Skew", "--description", "Clock skew fix.", "--type", "Runbook", "--tag", "bug", "--body", "Check server time."),
                run_cairn(root, "update", note_path, "--append", "Also verify the deployment token scope."),
            ]

            for result in commands:
                self.assertEqual(result.returncode, 0, result.stderr)
            events = read_events(root)
            self.assertEqual(
                [event["command"] for event in events],
                ["search", "retrieve", "similar", "show", "capture", "update"],
            )
            self.assertEqual(events[0]["data"]["result_count"], 1)
            self.assertEqual(events[1]["data"]["used_tokens"], json.loads(commands[1].stdout)["used_tokens"])
            self.assertIn(note_path, events[1]["data"]["source_paths"])
            serialized = json.dumps(events)
            self.assertNotIn("Update the CI secret", serialized)
            self.assertNotIn("content", serialized)
            self.assertNotIn("snippet", serialized)

    def test_usage_report_generates_terminal_json_and_html_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_vault(root, profile_name="engineering")
            write_note(root)
            rebuild_index(root)
            run_cairn(root, "usage", "enable")
            run_cairn(root, "search", "deploy 403")

            terminal = run_cairn(root, "usage", "report")
            as_json = run_cairn(root, "usage", "report", "--json")
            html = run_cairn(root, "usage", "report", "--html", "--json")

            self.assertEqual(terminal.returncode, 0, terminal.stderr)
            self.assertIn("events: 1", terminal.stdout)
            payload = json.loads(as_json.stdout)
            self.assertEqual(payload["event_count"], 1)
            html_payload = json.loads(html.stdout)
            report_path = root / html_payload["report_path"]
            self.assertTrue(report_path.is_file())
            page = report_path.read_text(encoding="utf-8")
            self.assertIn("ApolloKairn Usage Report", page)
            self.assertIn("deploy", page)

    def test_usage_evidence_generates_decision_pack_from_local_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_vault(root, profile_name="engineering")
            note_path = write_note(root)
            rebuild_index(root)
            run_cairn(root, "usage", "enable")
            commands = [
                run_cairn(root, "search", "deploy 403", "--json"),
                run_cairn(root, "search", "constellation payroll", "--json"),
                run_cairn(root, "retrieve", "deploy 403", "--mode", "passages", "--ranker", "auto", "--budget", "300", "--json"),
                run_cairn(root, "retrieve", "constellation payroll", "--mode", "passages", "--ranker", "auto", "--budget", "300", "--json"),
                run_cairn(root, "update", note_path, "--append", "Also verify token scope."),
            ]
            for result in commands:
                self.assertEqual(result.returncode, 0, result.stderr)

            evidence = run_cairn(root, "usage", "evidence", "--json")

            self.assertEqual(evidence.returncode, 0, evidence.stderr)
            payload = json.loads(evidence.stdout)
            self.assertEqual(payload["event_count"], 5)
            self.assertEqual(payload["observation_counts"]["searches"], 2)
            self.assertEqual(payload["observation_counts"]["retrieves"], 2)
            self.assertEqual(payload["observation_counts"]["writes"], 1)
            self.assertEqual(payload["observation_counts"]["zero_result_searches"], 1)
            self.assertEqual(payload["observation_counts"]["zero_source_retrieves"], 1)
            self.assertEqual(payload["observation_counts"]["passage_retrieves"], 2)
            self.assertEqual(payload["rates"]["zero_result_search_rate"], 0.5)
            self.assertEqual(payload["rates"]["zero_source_retrieve_rate"], 0.5)
            self.assertEqual(payload["rates"]["retrieve_per_search_rate"], 1.0)
            self.assertEqual(payload["privacy"]["stores_note_bodies"], False)
            self.assertEqual(payload["privacy"]["stores_snippets"], False)
            self.assertIn("ranker_or_embedding_decision", payload["decision_notes"])
            report_path = root / payload["report_path"]
            self.assertTrue(report_path.is_file())
            self.assertEqual(json.loads(report_path.read_text(encoding="utf-8"))["event_count"], 5)

    def test_usage_evidence_does_not_store_note_bodies_snippets_or_secret_like_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_vault(root, profile_name="engineering")
            write_note(root)
            rebuild_index(root)
            run_cairn(root, "usage", "enable")
            token = "ghp_1234567890abcdefghijklmnop"
            search = run_cairn(root, "search", f"deploy {token}", "--json")
            retrieve = run_cairn(root, "retrieve", "deploy 403", "--budget", "300", "--json")
            self.assertEqual(search.returncode, 0, search.stderr)
            self.assertEqual(retrieve.returncode, 0, retrieve.stderr)

            evidence = run_cairn(root, "usage", "evidence", "--json")

            self.assertEqual(evidence.returncode, 0, evidence.stderr)
            serialized = json.dumps(json.loads(evidence.stdout))
            report_path = root / json.loads(evidence.stdout)["report_path"]
            artifact = report_path.read_text(encoding="utf-8")
            self.assertNotIn(token, serialized)
            self.assertNotIn(token, artifact)
            self.assertNotIn("Update the CI secret", artifact)
            self.assertNotIn('"snippet":', artifact)
            self.assertIn("[REDACTED:GitHub token]", artifact)

    def test_usage_events_redact_secret_like_query_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_vault(root, profile_name="engineering")
            write_note(root)
            rebuild_index(root)
            run_cairn(root, "usage", "enable")
            token = "ghp_1234567890abcdefghijklmnop"

            result = run_cairn(root, "search", f"deploy {token}")

            self.assertEqual(result.returncode, 0, result.stderr)
            serialized = json.dumps(read_events(root))
            self.assertNotIn(token, serialized)
            self.assertIn("[REDACTED:GitHub token]", serialized)
