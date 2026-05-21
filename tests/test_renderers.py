import unittest
from pathlib import Path

from resume_kit.corpus import load_corpus
from resume_kit.jd import analyze_jd
from resume_kit.matcher import match_jd
from resume_kit.profiles import get_profile
from resume_kit.renderers import render_gap, render_resume


FIXTURE = Path(__file__).parent / "fixtures" / "jd_ai_agent.md"


class RendererTests(unittest.TestCase):
    def match_result(self):
        jd = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        return match_jd(jd, get_profile("ai-agent"), load_corpus())

    def test_render_resume_contains_selected_project(self):
        text = render_resume(self.match_result())
        self.assertIn("内容采集清洗与多平台分发 Agent 工作流", text)
        self.assertIn("14w+", text)

    def test_render_gap_contains_go_gap(self):
        text = render_gap(self.match_result())
        self.assertIn("Go", text)
        self.assertIn("gap", text.lower())
