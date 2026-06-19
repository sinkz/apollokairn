from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "bench" / "fixtures" / "vault-large"
TOPICS = ROOT / "bench" / "topics-large.jsonl"
QRELS = ROOT / "bench" / "qrels-large.tsv"
GOLDEN = ROOT / "bench" / "golden-large.json"
TASKS = ROOT / "bench" / "agent" / "tasks-large.jsonl"


def run_bench(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    env.setdefault("APOLLOKAIRN_REGISTRY_PATH", str(ROOT / ".cairn" / f"test-registry-{os.getpid()}.json"))
    return subprocess.run(
        [sys.executable, "bench/run_eval.py", *args],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def load_topics() -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in TOPICS.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_qrels() -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for line in QRELS.read_text(encoding="utf-8").splitlines():
        topic_id, path, relevance = line.split("\t")
        rows.setdefault(topic_id, []).append(path)
        int(relevance)
    return rows


def load_tasks() -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in TASKS.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


class LargeBenchmarkTests(unittest.TestCase):
    def test_large_fixture_has_required_inventory_and_slices(self) -> None:
        topics = load_topics()
        qrels = load_qrels()
        markdown_paths = sorted(VAULT.rglob("*.md"))
        category_counts: dict[str, int] = {}
        for topic in topics:
            category = str(topic["category"])
            category_counts[category] = category_counts.get(category, 0) + 1

        self.assertGreaterEqual(len(markdown_paths), 300)
        self.assertEqual(len(topics), 80)
        self.assertGreaterEqual(category_counts["no_answer"] / len(topics), 0.05)
        self.assertGreaterEqual(category_counts["paraphrase"], 10)
        self.assertGreaterEqual(category_counts["role_workflow"], 10)
        self.assertGreaterEqual(category_counts["passage_budget"], 10)
        self.assertGreaterEqual(category_counts["pt_br"], 8)

        answerable_topics = [topic for topic in topics if topic["category"] != "no_answer"]
        self.assertGreaterEqual(
            sum(len(paths) for paths in qrels.values()) / len(answerable_topics),
            2.0,
        )

        for topic in topics:
            topic_id = str(topic["id"])
            paths = qrels.get(topic_id, [])
            if topic["category"] == "no_answer":
                self.assertEqual(paths, [])
                continue
            self.assertGreaterEqual(len(paths), 1)
            if topic["category"] == "filtered":
                self.assertEqual(len(paths), 1)
                self.assertTrue(paths[0].startswith("knowledge/"), paths)

        for paths in qrels.values():
            for rel_path in paths:
                self.assertNotIn(" ", rel_path)
                self.assertTrue((VAULT / rel_path).exists(), rel_path)

    def test_large_agent_tasks_match_topics_qrels_and_fixture_paths(self) -> None:
        topics = {str(topic["id"]): topic for topic in load_topics()}
        qrels = load_qrels()
        tasks = load_tasks()
        tasks_by_query_id = {str(task["query_id"]): task for task in tasks}

        self.assertEqual(len(tasks_by_query_id), len(tasks), "duplicate task query_id")
        self.assertEqual(set(tasks_by_query_id), set(topics))

        for query_id, task in tasks_by_query_id.items():
            topic = topics[query_id]
            self.assertEqual(task["question"], topic["query"], query_id)
            self.assertEqual(task["slice"], topic["category"], query_id)
            self.assertGreaterEqual(int(task["budget"]), int(topic["budget"]), query_id)
            for field in ("mode", "ranker", "type", "tag", "system"):
                if field in task or field in topic:
                    self.assertEqual(task.get(field), topic.get(field), f"{query_id} {field}")

            expected_paths = list(task["expected_paths"])
            qrel_paths = qrels.get(query_id, [])
            if topic["category"] == "no_answer":
                self.assertTrue(task["expect_abstention"], query_id)
                self.assertEqual(expected_paths, [], query_id)
                self.assertEqual(task["expected_facts"], [], query_id)
                self.assertEqual(qrel_paths, [], query_id)
                continue

            self.assertFalse(task["expect_abstention"], query_id)
            self.assertGreaterEqual(len(expected_paths), 1, query_id)
            self.assertIn(query_id, qrels)
            self.assertLessEqual(set(expected_paths), set(qrel_paths), query_id)
            for rel_path in set(expected_paths) | set(qrel_paths):
                self.assertTrue((VAULT / rel_path).is_file(), f"{query_id}: {rel_path}")
            if topic["category"] == "filtered":
                self.assertEqual(expected_paths, qrel_paths, query_id)
                self.assertEqual(len(qrel_paths), 1, query_id)
                self.assertTrue(qrel_paths[0].startswith("knowledge/"), query_id)

    def test_large_fixture_matches_golden_with_quality_floor(self) -> None:
        result = run_bench(
            "--fixture",
            str(VAULT),
            "--topics",
            str(TOPICS),
            "--qrels",
            str(QRELS),
            "--min-recall",
            "0.9",
            "--min-mrr",
            "0.9",
            "--min-ndcg",
            "0.85",
            "--quiet",
            "--compare-golden",
            str(GOLDEN),
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("bench ok", result.stdout)

    def test_large_fixture_reports_slice_metrics(self) -> None:
        result = run_bench(
            "--fixture",
            str(VAULT),
            "--topics",
            str(TOPICS),
            "--qrels",
            str(QRELS),
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        metrics = {row["slice"]: row for row in payload["slice_metrics"]}
        self.assertEqual(metrics["no_answer"]["topics"], 5)
        self.assertEqual(metrics["no_answer"]["false_positive_rate"], 0.0)
        self.assertEqual(metrics["paraphrase"]["topics"], 10)
        self.assertEqual(metrics["role_workflow"]["topics"], 10)
        self.assertEqual(metrics["cross_doc"]["topics"], 10)
        self.assertGreaterEqual(metrics["cross_doc"]["mean_recall_at_k"], 0.9)


if __name__ == "__main__":
    unittest.main()
