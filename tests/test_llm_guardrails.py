import unittest
from pathlib import Path

from resume_kit.corpus import load_corpus
from resume_kit.jd import analyze_jd
from resume_kit.llm_guardrails import build_llm_prompt
from resume_kit.matcher import match_jd
from resume_kit.profiles import get_profile


FIXTURE = Path(__file__).parent / "fixtures" / "jd_ai_agent.md"


class LLMGuardrailTests(unittest.TestCase):
    def test_prompt_contains_guardrails_and_evidence(self):
        jd = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        result = match_jd(jd, get_profile("ai-agent"), load_corpus())
        prompt = build_llm_prompt(result)
        self.assertIn("不得新增事实", prompt)
        self.assertIn("客户项目只写客户名 + 场景 + 责任范围", prompt)
        self.assertIn("内容采集清洗与多平台分发 Agent 工作流", prompt)
        self.assertIn("Go", prompt)
        self.assertIn("gap", prompt.lower())
