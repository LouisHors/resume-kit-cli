import tempfile
import unittest
from pathlib import Path

from resume_kit.package import create_package


FIXTURE = Path(__file__).parent / "fixtures" / "jd_ai_agent.md"


class PackageTests(unittest.TestCase):
    def test_create_package_outputs_expected_files(self):
        with tempfile.TemporaryDirectory() as tempdir:
            paths = create_package(FIXTURE, "ai-agent", Path(tempdir), force=False)
            names = {path.name for path in paths}
            self.assertEqual(names, {
                "resume.md",
                "gap.md",
                "llm-prompt.md",
                "match.json",
                "evidence-map.md",
            })
            self.assertIn("14w+", (Path(tempdir) / "resume.md").read_text(encoding="utf-8"))
