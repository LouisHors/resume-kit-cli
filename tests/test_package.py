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
            resume_text = (Path(tempdir) / "resume.md").read_text(encoding="utf-8")
            match_text = (Path(tempdir) / "match.json").read_text(encoding="utf-8")
            prompt_text = (Path(tempdir) / "llm-prompt.md").read_text(encoding="utf-8")
            self.assertIn("手机：15338866734", resume_text)
            self.assertIn("## 个人定位", resume_text)
            self.assertIn("## 核心优势", resume_text)
            self.assertIn("## 工作经历", resume_text)
            self.assertIn("## 项目展示", resume_text)
            self.assertIn("## 技术能力", resume_text)
            self.assertIn("## 教育经历", resume_text)
            self.assertIn("14w+", resume_text)
            self.assertIn("document-driven-ai-workflow", resume_text)
            self.assertIn("角色：", resume_text)
            for forbidden in ["Codex++", "DSV4", "dsv42codex"]:
                self.assertNotIn(forbidden, resume_text)
                self.assertNotIn(forbidden, match_text)
                self.assertNotIn(forbidden, prompt_text)
