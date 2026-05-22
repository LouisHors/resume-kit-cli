import unittest

from resume_kit.corpus import load_corpus


class CorpusTests(unittest.TestCase):
    def test_load_corpus_has_required_sources(self):
        corpus = load_corpus()
        keys = {source.key for source in corpus.sources}
        self.assertIn("fact_baseline", keys)
        self.assertIn("resume_ai_agent", keys)

    def test_extract_evidence_contains_agent_project(self):
        corpus = load_corpus()
        ids = {item.id for item in corpus.evidence}
        self.assertIn("personal-content-distribution-agent", ids)

    def test_ai_agent_corpus_uses_fixed_six_project_pool(self):
        corpus = load_corpus()
        ai_items = [item for item in corpus.evidence if "ai-agent" in item.profile_tags]
        project_names = [item.project_name for item in ai_items]
        self.assertEqual(project_names, [
            "zego-delivery-tool-kit",
            "document-driven-ai-workflow",
            "Horspowers",
            "Zego RTC 智能排障系统",
            "ZegoExpressEngine AI 场景代码生成器",
            "内容采集清洗与多平台分发 Agent 工作流",
        ])

    def test_ai_agent_corpus_excludes_small_side_projects(self):
        corpus = load_corpus()
        text = "\n".join(
            [
                item.id
                + "\n"
                + item.project_name
                + "\n"
                + item.summary
                + "\n"
                + "\n".join(item.resume_phrasing)
                for item in corpus.evidence
            ]
        )
        for forbidden in ["Codex++", "DSV4", "dsv42codex"]:
            self.assertNotIn(forbidden, text)
