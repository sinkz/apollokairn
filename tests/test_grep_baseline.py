from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_grep_baseline(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    env.setdefault("APOLLOKAIRN_REGISTRY_PATH", str(ROOT / ".cairn" / f"test-registry-{os.getpid()}.json"))
    return subprocess.run(
        [sys.executable, "bench/run_grep_baseline.py", *args],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class GrepBaselineTests(unittest.TestCase):
    def test_grep_baseline_outputs_quality_and_raw_read_metrics(self) -> None:
        result = run_grep_baseline("--compare-golden", "bench/grep-golden.json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["suite"], "grep_raw_read")
        self.assertEqual(payload["topics"], 28)
        self.assertEqual(payload["max_files"], 20)
        self.assertGreater(payload["files_read"], 0)
        self.assertGreater(payload["returned_tokens"], 0)
        self.assertLess(payload["mean_ndcg_at_k"], 1.0)

    def test_grep_baseline_compare_golden_detects_regression(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            golden = Path(tmp) / "golden.json"
            golden.write_text('{"q1":["wrong.md"]}\n', encoding="utf-8")

            result = run_grep_baseline("--compare-golden", str(golden))

        self.assertEqual(result.returncode, 1)
        self.assertIn("golden regression", result.stderr)

    def test_grep_baseline_runs_against_large_fixture(self) -> None:
        result = run_grep_baseline(
            "--fixture",
            "bench/fixtures/vault-large",
            "--topics",
            "bench/topics-large.jsonl",
            "--qrels",
            "bench/qrels-large.tsv",
            "--quiet",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("grep baseline ok", result.stdout)
        self.assertIn("recall@20=", result.stdout)


if __name__ == "__main__":
    unittest.main()
