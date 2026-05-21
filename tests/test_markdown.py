import unittest

from resume_kit.markdown import extract_headings, strip_frontmatter


class MarkdownTests(unittest.TestCase):
    def test_strip_frontmatter(self):
        body = strip_frontmatter("---\na: b\n---\n# Title\nBody")
        self.assertEqual(body.strip(), "# Title\nBody")

    def test_extract_headings(self):
        headings = extract_headings("# A\ntext\n## B\nb\n### C\nc")
        self.assertEqual([h["title"] for h in headings], ["A", "B", "C"])
        self.assertEqual(headings[1]["level"], 2)
        self.assertIn("b", headings[1]["body"])
