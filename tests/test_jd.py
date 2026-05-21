import unittest
from pathlib import Path

from resume_kit.jd import analyze_jd


FIXTURE = Path(__file__).parent / "fixtures" / "jd_ai_agent.md"


class JDTests(unittest.TestCase):
    def test_analyze_jd_extracts_sections(self):
        analysis = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(analysis.title, "AI Agent 开发工程师")
        self.assertTrue(any("NAS 智能 Agent" in item for item in analysis.responsibilities))
        self.assertTrue(any("Go 语言" in item for item in analysis.must_requirements))
        self.assertTrue(any("向量检索" in item for item in analysis.nice_to_have))

    def test_analyze_jd_infers_ai_profile_and_risk_flags(self):
        analysis = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(analysis.inferred_profile, "ai-agent")
        self.assertIn("go-language-hard-requirement", analysis.risk_flags)
        self.assertIn("nas-domain-gap", analysis.risk_flags)
