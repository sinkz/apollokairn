from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "bench"))

from cairn.ranking import query_tokens
from cairn.retriever import approx_tokens
from cairn.validate import RESERVED_NAMES
from run_eval import _quality, compare_golden, corpus_metadata, load_qrels, load_topics, run_map, validate_inputs


def concept_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for path in root.rglob("*.md"):
        rel_parts = path.relative_to(root).parts
        if ".cairn" in rel_parts or "_templates" in rel_parts:
            continue
        if path.name in RESERVED_NAMES:
            continue
        out.append(path)
    return sorted(out)


def grep_docs(root: Path, query: str, max_files: int) -> list[str]:
    tokens = [token.casefold() for token in query_tokens(query)]
    if not tokens:
        return []
    docs: list[str] = []
    for path in concept_files(root):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        haystack = f"{rel}\n{text}".casefold()
        if all(token in haystack for token in tokens):
            docs.append(rel)
        if len(docs) >= max_files:
            break
    return docs


def evaluate_topic(root: Path, topic: object, relevant: dict[str, int], max_files: int) -> dict[str, object]:
    docs = grep_docs(root, topic.query, max_files)
    returned_tokens = sum(approx_tokens((root / doc).read_text(encoding="utf-8")) for doc in docs)
    return {
        "id": topic.id,
        "query": topic.query,
        "category": topic.category,
        "docs": docs,
        "files_read": len(docs),
        "returned_tokens": returned_tokens,
        **_quality(docs, relevant, max_files),
    }


def false_positive_rate(per_topic: Sequence[dict[str, object]]) -> float:
    no_answer = [item for item in per_topic if item["category"] == "no_answer"]
    if not no_answer:
        return 0.0
    positives = [item for item in no_answer if item["docs"]]
    return round(len(positives) / len(no_answer), 4)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run deterministic grep/raw-read retrieval baseline.")
    parser.add_argument("--fixture", default=str(ROOT / "bench" / "fixtures" / "vault"))
    parser.add_argument("--topics", default=str(ROOT / "bench" / "topics.jsonl"))
    parser.add_argument("--qrels", default=str(ROOT / "bench" / "qrels.tsv"))
    parser.add_argument("--max-files", type=int, default=20)
    parser.add_argument("--write-golden")
    parser.add_argument("--compare-golden")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    try:
        topics = load_topics(Path(args.topics))
        qrels = load_qrels(Path(args.qrels))
        validate_inputs(Path(args.fixture), topics, qrels)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"grep baseline input error: {exc}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "vault"
        shutil.copytree(Path(args.fixture), root)
        per_topic = [
            evaluate_topic(root, topic, qrels.get(topic.id, {}), args.max_files)
            for topic in topics
        ]
        mean_recall = sum(float(item["recall_at_k"]) for item in per_topic) / len(per_topic)
        mean_mrr = sum(float(item["mrr_at_k"]) for item in per_topic) / len(per_topic)
        mean_ndcg = sum(float(item["ndcg_at_k"]) for item in per_topic) / len(per_topic)
        files_read = sum(int(item["files_read"]) for item in per_topic)
        returned_tokens = sum(int(item["returned_tokens"]) for item in per_topic)
        output = {
            "suite": "grep_raw_read",
            "topics": len(topics),
            "max_files": args.max_files,
            "corpus": corpus_metadata(root, topics, qrels),
            "mean_recall_at_k": round(mean_recall, 4),
            "mean_mrr_at_k": round(mean_mrr, 4),
            "mean_ndcg_at_k": round(mean_ndcg, 4),
            "false_positive_rate": false_positive_rate(per_topic),
            "files_read": files_read,
            "mean_files_read": round(files_read / len(per_topic), 4),
            "returned_tokens": returned_tokens,
            "mean_returned_tokens": round(returned_tokens / len(per_topic), 4),
            "per_topic": per_topic,
        }

    actual_run = run_map(per_topic)
    if args.write_golden:
        golden_path = Path(args.write_golden)
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(json.dumps(actual_run, indent=2) + "\n", encoding="utf-8", newline="\n")
    golden_failures: list[str] = []
    if args.compare_golden:
        golden_failures = compare_golden(actual_run, Path(args.compare_golden))
        for failure in golden_failures:
            print(failure, file=sys.stderr)

    if args.quiet:
        print(
            "grep baseline ok "
            f"recall@{args.max_files}={output['mean_recall_at_k']} "
            f"mrr@{args.max_files}={output['mean_mrr_at_k']} "
            f"ndcg@{args.max_files}={output['mean_ndcg_at_k']} "
            f"files_read={output['files_read']} "
            f"tokens={output['returned_tokens']}"
        )
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))

    return 1 if golden_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
