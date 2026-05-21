import unittest
from pathlib import Path

from resume_kit.corpus import load_corpus
from resume_kit.jd import analyze_jd
from resume_kit.matcher import match_jd
from resume_kit.profiles import get_profile


FIXTURE = Path(__file__).parent / "fixtures" / "jd_ai_agent.md"


class MatcherTests(unittest.TestCase):
    def test_match_ai_agent_jd_selects_personal_agent_evidence(self):
        jd = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        result = match_jd(jd, get_profile("ai-agent"), load_corpus())
        ids = {item.id for item in result.selected_evidence}
        self.assertIn("personal-content-distribution-agent", ids)

    def test_go_requirement_is_gap_not_direct_match(self):
        jd = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        result = match_jd(jd, get_profile("ai-agent"), load_corpus())
        self.assertTrue(any(gap["id"] == "go-language-hard-requirement" for gap in result.gaps))
