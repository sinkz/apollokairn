from __future__ import annotations

from typing import Sequence


def rrf_merge(runs: Sequence[Sequence[str]], k: int = 60) -> list[str]:
    if k <= 0:
        raise ValueError("k must be positive")

    scores: dict[str, float] = {}
    best_rank: dict[str, int] = {}
    first_seen: dict[str, int] = {}
    order = 0

    for run in runs:
        seen_in_run: set[str] = set()
        for rank, item_id in enumerate(run, start=1):
            if item_id in seen_in_run:
                continue
            seen_in_run.add(item_id)
            if item_id not in first_seen:
                first_seen[item_id] = order
                order += 1
            scores[item_id] = scores.get(item_id, 0.0) + (1 / (k + rank))
            best_rank[item_id] = min(best_rank.get(item_id, rank), rank)

    return sorted(
        scores,
        key=lambda item_id: (
            -scores[item_id],
            best_rank[item_id],
            first_seen[item_id],
            item_id,
        ),
    )
