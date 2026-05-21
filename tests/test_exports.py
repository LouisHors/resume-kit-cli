import tempfile
import unittest
from pathlib import Path

from resume_kit.exports import export_resume_markdown, render_resume_html
from resume_kit.renderers import formalize_publish_resume_text


class ExportTests(unittest.TestCase):
    def test_formalized_title_removes_draft_suffix(self):
        text = "# 刘豪 - AI Agent / AI Coding 方向简历初稿\n\n## 教育经历\n\n山东政法学院\n"
        formalized = formalize_publish_resume_text(text)
        self.assertIn("# 刘豪 - AI Agent / AI Coding 方向简历", formalized)
        self.assertNotIn("初稿", formalized)

    def test_render_resume_html_omits_manual_review_after_strip(self):
        text = "# 简历\n\n## 教育经历\n\n山东政法学院\n\n## 需要人工复核\n\n- 不应导出\n"
        html = render_resume_html(text.replace("## 需要人工复核\n\n- 不应导出\n", ""))
        self.assertIn("<h2>教育经历</h2>", html)
        self.assertNotIn("需要人工复核", html)

    def test_export_html_omits_manual_review_section(self):
        with tempfile.TemporaryDirectory() as tempdir:
            tempdir = Path(tempdir)
            source = tempdir / "resume.md"
            target = tempdir / "resume.html"
            source.write_text(
                "# 刘豪 - AI Agent / AI Coding 方向简历初稿\n\n## 教育经历\n\n山东政法学院\n\n## 需要人工复核\n\n- 不应导出\n",
                encoding="utf-8",
            )

            paths = export_resume_markdown(source, html_path=target)

            self.assertEqual(paths, [target])
            html = target.read_text(encoding="utf-8")
            self.assertIn("<h2>教育经历</h2>", html)
            self.assertIn("山东政法学院", html)
            self.assertNotIn("需要人工复核", html)
            self.assertNotIn("不应导出", html)
            self.assertIn("刘豪 - AI Agent / AI Coding 方向简历", html)
            self.assertNotIn("刘豪 - AI Agent / AI Coding 方向简历初稿", html)
