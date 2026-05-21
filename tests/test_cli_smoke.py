import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CliSmokeTests(unittest.TestCase):
    def run_cli(self, *args):
        cmd = [
            sys.executable,
            str(ROOT / "resume_kit" / "cli.py"),
            *args,
        ]
        return subprocess.run(cmd, text=True, capture_output=True, check=False)

    def test_help(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("resume-kit", result.stdout)
        self.assertIn("doctor", result.stdout)

    def test_json_doctor_shape(self):
        result = self.run_cli("doctor", "--json")
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertIn("data", payload)
        self.assertIn("sources", payload["data"])

    def test_resume_export_html_omits_manual_review_section(self):
        with tempfile.TemporaryDirectory() as tempdir:
            tempdir = Path(tempdir)
            source = tempdir / "resume.md"
            target = tempdir / "resume.html"
            source.write_text("# 刘豪 - AI Agent / AI Coding 方向简历初稿\n\n## 教育经历\n\n本科\n\n## 需要人工复核\n\n- 删除我\n", encoding="utf-8")

            result = self.run_cli("resume", "export", str(source), "--html", str(target))

            self.assertEqual(result.returncode, 0, result.stderr)
            html = target.read_text(encoding="utf-8")
            self.assertIn("教育经历", html)
            self.assertNotIn("需要人工复核", html)
            self.assertNotIn("删除我", html)
            self.assertIn("刘豪 - AI Agent / AI Coding 方向简历", html)
            self.assertNotIn("刘豪 - AI Agent / AI Coding 方向简历初稿", html)
