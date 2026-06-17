from __future__ import annotations

import unittest

from cairn.passages import split_passages


class PassageTests(unittest.TestCase):
    def test_split_passages_uses_heading_and_line_ranges(self) -> None:
        text = (
            "---\n"
            "type: Runbook\n"
            "title: Deploy 403\n"
            "description: Fix deploy.\n"
            "tags: [deploy]\n"
            "timestamp: 2026-06-17T10:00:00Z\n"
            "---\n\n"
            "# Context\n\n"
            "Deploy fails with HTTP 403.\n\n"
            "# Resolution\n\n"
            "Rotate the CI token.\n"
        )

        passages = split_passages("knowledge/deploy-403.md", text)

        self.assertEqual(len(passages), 2)
        self.assertEqual(passages[0].path, "knowledge/deploy-403.md")
        self.assertEqual(passages[0].heading, "Context")
        self.assertEqual(passages[0].start_line, 9)
        self.assertEqual(passages[0].end_line, 12)
        self.assertIn("HTTP 403", passages[0].text)
        self.assertEqual(passages[1].heading, "Resolution")
        self.assertEqual(passages[1].start_line, 13)
        self.assertIn("Rotate the CI token.", passages[1].text)


if __name__ == "__main__":
    unittest.main()
