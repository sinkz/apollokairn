from __future__ import annotations

import unittest

from cairn.ranking import rrf_merge


class RankingTests(unittest.TestCase):
    def test_rrf_merge_is_deterministic(self) -> None:
        runs = [
            ["doc-a", "doc-b", "doc-c"],
            ["doc-b", "doc-a", "doc-d"],
            ["doc-a", "doc-d", "doc-b"],
        ]

        self.assertEqual(rrf_merge(runs, k=60), ["doc-a", "doc-b", "doc-d", "doc-c"])

    def test_rrf_merge_keeps_first_seen_order_for_exact_ties(self) -> None:
        runs = [
            ["doc-b", "doc-a"],
            ["doc-a", "doc-b"],
        ]

        self.assertEqual(rrf_merge(runs, k=60), ["doc-b", "doc-a"])

    def test_rrf_merge_ignores_duplicate_ids_within_same_run(self) -> None:
        runs = [
            ["doc-a", "doc-a", "doc-b"],
            ["doc-b"],
        ]

        self.assertEqual(rrf_merge(runs, k=60), ["doc-b", "doc-a"])


if __name__ == "__main__":
    unittest.main()
