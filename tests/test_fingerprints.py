from __future__ import annotations

import unittest

from cairn.fingerprints import fingerprint_similarity


class FingerprintTests(unittest.TestCase):
    def test_fingerprint_similarity_is_high_for_near_duplicate_text(self) -> None:
        original = "Update the CI secret after rotating workspace access and rerun the failed deployment job."
        duplicate = "After workspace access rotation, update the CI secret and rerun the failed deploy job."

        self.assertGreaterEqual(fingerprint_similarity(original, duplicate), 0.65)

    def test_fingerprint_similarity_is_low_for_unrelated_text(self) -> None:
        original = "Update the CI secret after rotating workspace access."
        unrelated = "Plan support escalation for a blocked customer before the SLA deadline."

        self.assertLess(fingerprint_similarity(original, unrelated), 0.55)


if __name__ == "__main__":
    unittest.main()
