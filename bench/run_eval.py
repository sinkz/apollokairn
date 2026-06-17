from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cairn.indexer import rebuild_index, search
from cairn.retriever import approx_tokens, retrieve


@dataclass(frozen=True)
class Topic:
    id: str
    query: str
    budget: int


def load_topics(path: Path) -> list[Topic]:
    topics: list[Topic] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        topics.append(Topic(id=row["id"], query=row["query"], budget=int(row.get("budget", 600))))
    return topics


def load_qrels(path: Path) -> dict[str, dict[str, int]]:
    qrels: dict[str, dict[str, int]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        qid, doc, rel = line.split("\t")
        qrels.setdefault(qid, {})[doc] = int(rel)
    return qrels


def dcg(rels: list[int]) -> float:
    total = 0.0
    for idx, rel in enumerate(rels, start=1):
        total += ((2**rel) - 1) / math.log2(idx + 1)
    return total


def evaluate_topic(root: Path, topic: Topic, relevant: dict[str, int], limit: int) -> dict[str, object]:
    results = search(root, topic.query, limit=limit)
    docs = [result.path for result in results]
    relevant_docs = {doc for doc, rel in relevant.items() if rel > 0}
    retrieved_relevant = [doc for doc in docs[:limit] if doc in relevant_docs]
    first_rank = next((idx for idx, doc in enumerate(docs[:limit], start=1) if doc in relevant_docs), None)
    gains = [relevant.get(doc, 0) for doc in docs[:limit]]
    ideal = sorted(relevant.values(), reverse=True)[:limit]
    ndcg = dcg(gains) / dcg(ideal) if ideal and dcg(ideal) else 0.0
    packet = retrieve(root, topic.query, limit=limit, budget_tokens=topic.budget)
    returned_tokens = approx_tokens(packet)
    return {
        "id": topic.id,
        "query": topic.query,
        "docs": docs,
        "recall_at_k": len(retrieved_relevant) / len(relevant_docs) if relevant_docs else 1.0,
        "mrr_at_k": 1 / first_rank if first_rank else 0.0,
        "ndcg_at_k": ndcg,
        "returned_tokens": returned_tokens,
        "budget_tokens": topic.budget,
        "within_budget": returned_tokens <= topic.budget,
    }


def corpus_tokens(root: Path) -> int:
    total = 0
    for path in root.rglob("*.md"):
        if ".cairn" in path.parts:
            continue
        total += approx_tokens(path.read_text(encoding="utf-8"))
    return total


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run deterministic Cairn search benchmarks.")
    parser.add_argument("--fixture", default=str(ROOT / "bench" / "fixtures" / "vault"))
    parser.add_argument("--topics", default=str(ROOT / "bench" / "topics.jsonl"))
    parser.add_argument("--qrels", default=str(ROOT / "bench" / "qrels.tsv"))
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    topics = load_topics(Path(args.topics))
    qrels = load_qrels(Path(args.qrels))
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "vault"
        shutil.copytree(Path(args.fixture), root)
        rebuild_index(root)
        per_topic = [
            evaluate_topic(root, topic, qrels.get(topic.id, {}), limit=args.limit)
            for topic in topics
        ]
        full_tokens = corpus_tokens(root)
        mean_recall = sum(float(item["recall_at_k"]) for item in per_topic) / len(per_topic)
        mean_mrr = sum(float(item["mrr_at_k"]) for item in per_topic) / len(per_topic)
        mean_ndcg = sum(float(item["ndcg_at_k"]) for item in per_topic) / len(per_topic)
        returned_tokens = sum(int(item["returned_tokens"]) for item in per_topic)
        full_context_tokens = full_tokens * len(per_topic)
        output = {
            "topics": len(topics),
            "limit": args.limit,
            "mean_recall_at_k": round(mean_recall, 4),
            "mean_mrr_at_k": round(mean_mrr, 4),
            "mean_ndcg_at_k": round(mean_ndcg, 4),
            "full_context_tokens": full_context_tokens,
            "returned_tokens": returned_tokens,
            "context_reduction": round(1 - (returned_tokens / full_context_tokens), 4)
            if full_context_tokens
            else 0,
            "per_topic": per_topic,
        }
    if args.quiet:
        print(
            "bench ok "
            f"recall@{args.limit}={output['mean_recall_at_k']} "
            f"mrr@{args.limit}={output['mean_mrr_at_k']} "
            f"ndcg@{args.limit}={output['mean_ndcg_at_k']} "
            f"context_reduction={output['context_reduction']}"
        )
    else:
        print(json.dumps(output, indent=2))
    if mean_recall < 1.0 or mean_mrr < 0.8 or mean_ndcg < 0.8:
        return 1
    if any(not item["within_budget"] for item in per_topic):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
