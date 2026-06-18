from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import statistics
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cairn.indexer import rebuild_index
from cairn.notes import append_to_note, create_note
from cairn.similar import SimilarResult, find_similar


DEFAULT_THRESHOLD = 0.70
FIXED_TIMESTAMP = "2026-06-18T00:00:00Z"


@dataclass(frozen=True)
class WritebackCase:
    id: str
    query: str
    append: str
    title: str
    description: str
    typ: str
    tags: tuple[str, ...]
    category: str
    expected_action: str
    expected_reason: str
    expected_path: str | None = None
    folder: str = "knowledge"
    systems: tuple[str, ...] = ()
    signals: tuple[str, ...] = ()
    type_filter: str | None = None
    tag_filters: tuple[str, ...] = ()
    system_filters: tuple[str, ...] = ()
    simulate_conflict: bool = False


def _string_tuple(value: object) -> tuple[str, ...]:
    if isinstance(value, str) and value:
        return (value,)
    if isinstance(value, list):
        return tuple(item for item in value if isinstance(item, str) and item)
    return ()


def load_cases(path: Path) -> list[WritebackCase]:
    cases: list[WritebackCase] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        cases.append(
            WritebackCase(
                id=row["id"],
                query=row["query"],
                append=row["append"],
                title=row["title"],
                description=row["description"],
                typ=row.get("type", "Note"),
                tags=_string_tuple(row.get("tags")),
                category=row.get("category", "general"),
                expected_action=row["expected_action"],
                expected_reason=row["expected_reason"],
                expected_path=row.get("expected_path") if isinstance(row.get("expected_path"), str) else None,
                folder=row.get("folder", "knowledge"),
                systems=_string_tuple(row.get("systems")),
                signals=_string_tuple(row.get("signals")),
                type_filter=row.get("type_filter") if isinstance(row.get("type_filter"), str) else None,
                tag_filters=_string_tuple(row.get("tag_filter")),
                system_filters=_string_tuple(row.get("system_filter")),
                simulate_conflict=bool(row.get("simulate_conflict", False)),
            )
        )
    return cases


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _candidate_summary(candidates: Sequence[SimilarResult]) -> list[dict[str, object]]:
    return [
        {
            "path": candidate.path,
            "similarity": candidate.similarity,
            "kind": candidate.kind,
        }
        for candidate in candidates
    ]


def _similarity_margin(candidates: Sequence[SimilarResult]) -> float:
    if not candidates:
        return 0.0
    if len(candidates) == 1:
        return round(candidates[0].similarity, 4)
    return round(candidates[0].similarity - candidates[1].similarity, 4)


def evaluate_case(root: Path, case: WritebackCase, threshold: float) -> dict[str, object]:
    candidates = find_similar(
        root,
        case.query,
        limit=5,
        type_filter=case.type_filter,
        tag_filters=case.tag_filters,
        system_filters=case.system_filters,
    )
    top = candidates[0] if candidates else None
    target_path = top.path if top and top.similarity >= threshold else None
    sha256_before: str | None = None
    sha256_after: str | None = None
    append_present_after: bool | None = None
    actual_action = "create"
    reason = "below_threshold"

    if target_path is None:
        result = create_note(
            root,
            title=case.title,
            description=case.description,
            typ=case.typ,
            tags=case.tags,
            folder=case.folder,
            body=case.append,
            systems=case.systems,
            signals=case.signals,
            timestamp=FIXED_TIMESTAMP,
        )
        actual_action = "create"
        reason = "created"
        target_path = result.path
        sha256_after = result.sha256_after
        append_present_after = True
    else:
        path = root / target_path
        sha256_before = _sha256(path)
        expected_hash = sha256_before
        if case.simulate_conflict:
            path.write_text(path.read_text(encoding="utf-8") + "\nConcurrent edit.\n", encoding="utf-8")
        try:
            result = append_to_note(
                root,
                target_path,
                case.append,
                expected_sha256=expected_hash,
                timestamp=FIXED_TIMESTAMP,
            )
        except ValueError as exc:
            actual_action = "conflict" if "expected sha256" in str(exc) else "error"
            reason = "conflict"
            sha256_after = _sha256(path)
            append_present_after = case.append in path.read_text(encoding="utf-8")
        else:
            sha256_after = result.sha256_after
            append_present_after = case.append in path.read_text(encoding="utf-8")
            if result.changed:
                actual_action = "update"
                reason = result.reason
            elif result.reason == "already_present":
                actual_action = "noop"
                reason = result.reason
            else:
                actual_action = "noop"
                reason = result.reason

    expected_path = case.expected_path
    decision_correct = actual_action == case.expected_action
    target_correct = expected_path is None or target_path == expected_path
    reason_correct = reason == case.expected_reason
    correct = decision_correct and target_correct and reason_correct

    return {
        "id": case.id,
        "category": case.category,
        "expected_action": case.expected_action,
        "actual_action": actual_action,
        "expected_path": expected_path,
        "target_path": target_path,
        "expected_reason": case.expected_reason,
        "reason": reason,
        "correct": correct,
        "decision_correct": decision_correct,
        "target_path_correct": target_correct,
        "reason_correct": reason_correct,
        "candidate_count": len(candidates),
        "similarity_margin": _similarity_margin(candidates),
        "top_similarity": candidates[0].similarity if candidates else 0.0,
        "candidates": _candidate_summary(candidates),
        "sha256_before": sha256_before,
        "sha256_after": sha256_after,
        "hash_stable": sha256_before == sha256_after if sha256_before and sha256_after else None,
        "append_present_after": append_present_after,
    }


def _rate(values: Sequence[bool]) -> float:
    if not values:
        return 1.0
    return round(sum(1 for value in values if value) / len(values), 4)


def _case_golden(per_case: Sequence[dict[str, object]]) -> dict[str, dict[str, object]]:
    return {
        str(item["id"]): {
            "actual_action": item["actual_action"],
            "target_path": item["target_path"],
            "reason": item["reason"],
        }
        for item in per_case
    }


def summarize(per_case: Sequence[dict[str, object]], threshold: float) -> dict[str, object]:
    expected_updates = [item for item in per_case if item["expected_action"] == "update"]
    actual_updates = [item for item in per_case if item["actual_action"] == "update"]
    expected_creates = [item for item in per_case if item["expected_action"] == "create"]
    actual_creates = [item for item in per_case if item["actual_action"] == "create"]
    expected_noops = [item for item in per_case if item["expected_action"] == "noop"]
    expected_conflicts = [item for item in per_case if item["expected_action"] == "conflict"]
    expected_non_creates = [item for item in per_case if item["expected_action"] != "create"]
    cases_with_target = [item for item in per_case if item["expected_path"]]
    cases_with_reason = [item for item in per_case if item["expected_reason"]]
    margins = [float(item["similarity_margin"]) for item in per_case]
    candidate_counts = [int(item["candidate_count"]) for item in per_case]

    output = {
        "suite": "writeback",
        "strategy": "similarity-threshold-v1",
        "threshold": threshold,
        "cases": len(per_case),
        "actions": sorted({str(item["expected_action"]) for item in per_case}),
        "categories": sorted({str(item["category"]) for item in per_case}),
        "decision_accuracy": _rate([bool(item["decision_correct"]) for item in per_case]),
        "target_path_accuracy": _rate([bool(item["target_path_correct"]) for item in cases_with_target]),
        "reason_accuracy": _rate([bool(item["reason_correct"]) for item in cases_with_reason]),
        "update_precision": _rate([bool(item["correct"]) for item in actual_updates]),
        "update_recall": _rate([bool(item["correct"]) for item in expected_updates]),
        "create_precision": _rate([bool(item["correct"]) for item in actual_creates]),
        "create_recall": _rate([bool(item["correct"]) for item in expected_creates]),
        "noop_accuracy": _rate([bool(item["correct"]) for item in expected_noops]),
        "conflict_detection_rate": _rate(
            [item["actual_action"] == "conflict" for item in expected_conflicts]
        ),
        "conflict_write_block_rate": _rate(
            [item["append_present_after"] is False for item in expected_conflicts]
        ),
        "duplicate_avoidance_rate": _rate(
            [
                item["actual_action"] != "create" and bool(item["target_path_correct"])
                for item in expected_non_creates
            ]
        ),
        "false_update_rate": _rate([item["actual_action"] == "update" for item in expected_creates]),
        "false_create_rate": _rate([item["actual_action"] == "create" for item in expected_non_creates]),
        "idempotency_rate": _rate(
            [
                item["actual_action"] == "noop" and item["hash_stable"] is True
                for item in expected_noops
            ]
        ),
        "sha256_stability_rate": _rate([item["hash_stable"] is True for item in expected_noops]),
        "median_candidate_count": statistics.median(candidate_counts) if candidate_counts else 0,
        "mean_similarity_margin": round(sum(margins) / len(margins), 4) if margins else 0.0,
        "per_case": list(per_case),
    }
    return output


def compare_golden(actual: dict[str, dict[str, object]], golden_path: Path) -> list[str]:
    expected = json.loads(golden_path.read_text(encoding="utf-8"))
    cases = expected.get("cases") if isinstance(expected, dict) else None
    if not isinstance(cases, dict):
        return [f"writeback golden regression: {golden_path} must contain a cases object"]
    failures: list[str] = []
    for case_id, expected_case in cases.items():
        if not isinstance(expected_case, dict):
            failures.append(f"writeback golden regression: {case_id} must be an object")
            continue
        actual_case = actual.get(str(case_id))
        if actual_case != expected_case:
            failures.append(
                "writeback golden regression: "
                f"{case_id} expected {expected_case}, got {actual_case}"
            )
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run deterministic Cairn writeback benchmarks.")
    parser.add_argument("--fixture", default=str(ROOT / "bench" / "writeback" / "fixtures" / "vault"))
    parser.add_argument("--cases", default=str(ROOT / "bench" / "writeback" / "decisions.jsonl"))
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument("--write-golden")
    parser.add_argument("--compare-golden")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    cases = load_cases(Path(args.cases))
    per_case: list[dict[str, object]] = []
    for case in cases:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "vault"
            shutil.copytree(Path(args.fixture), root)
            rebuild_index(root)
            per_case.append(evaluate_case(root, case, args.threshold))

    output = summarize(per_case, args.threshold)
    actual_golden = {"cases": _case_golden(per_case)}
    if args.write_golden:
        golden_path = Path(args.write_golden)
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(json.dumps(actual_golden, indent=2) + "\n", encoding="utf-8")

    golden_failures: list[str] = []
    if args.compare_golden:
        golden_failures = compare_golden(actual_golden["cases"], Path(args.compare_golden))
        for failure in golden_failures:
            print(failure, file=sys.stderr)

    if args.quiet:
        print(
            "writeback ok "
            f"decision_accuracy={output['decision_accuracy']} "
            f"target_path_accuracy={output['target_path_accuracy']} "
            f"noop_accuracy={output['noop_accuracy']} "
            f"conflict_detection={output['conflict_detection_rate']} "
            f"duplicate_avoidance={output['duplicate_avoidance_rate']}"
        )
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))

    if golden_failures:
        return 1
    if (
        output["decision_accuracy"] < 1.0
        or output["target_path_accuracy"] < 1.0
        or output["noop_accuracy"] < 1.0
        or output["conflict_detection_rate"] < 1.0
    ):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
