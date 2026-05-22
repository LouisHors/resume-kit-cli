import unittest
from pathlib import Path

from resume_kit.corpus import load_corpus
from resume_kit.jd import analyze_jd
from resume_kit.matcher import match_jd
from resume_kit.profiles import get_profile
from resume_kit.renderers import render_gap, render_publish_resume, render_resume, strip_manual_review_section


FIXTURE = Path(__file__).parent / "fixtures" / "jd_ai_agent.md"


class RendererTests(unittest.TestCase):
    def match_result(self):
        jd = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        return match_jd(jd, get_profile("ai-agent"), load_corpus())

    def test_render_resume_contains_selected_project(self):
        text = render_resume(self.match_result())
        self.assertIn("内容采集清洗与多平台分发 Agent 工作流", text)
        self.assertIn("14w+", text)

    def test_render_resume_uses_structured_project_sections(self):
        text = render_resume(self.match_result())
        self.assertIn("角色：", text)
        self.assertIn("关键词：", text)
        self.assertIn("项目定位：", text)
        self.assertIn("主要工作：", text)
        self.assertIn("可突出成果：", text)

    def test_render_resume_restores_base_resume_structure(self):
        text = render_resume(self.match_result())
        self.assertIn("# 刘豪 - AI Agent / AI Coding 方向简历初稿", text)
        self.assertIn("手机：15338866734", text)
        self.assertIn("## 个人定位", text)
        self.assertIn("## 核心优势", text)
        self.assertIn("## 工作经历", text)
        self.assertIn("## 项目展示", text)
        self.assertIn("## 技术能力", text)
        self.assertIn("## 教育经历", text)
        self.assertIn("深圳市即构科技有限公司 - 高级解决方案专家", text)
        self.assertIn("山东政法学院 - 本科 - 信息工程", text)
        self.assertNotIn("定制说明", text)
        self.assertNotIn("重点匹配项目", text)

    def test_render_resume_does_not_duplicate_prefix_when_title_is_prefixed(self):
        result = self.match_result()
        text = render_resume(result)
        self.assertNotIn("# 刘豪 - 刘豪 -", text)

    def test_render_resume_uses_capability_sentences(self):
        text = render_resume(self.match_result())
        self.assertIn("## 技术能力", text)
        self.assertIn("能够基于", text)
        self.assertNotIn("Codex++", text)
        self.assertNotIn("DSV4", text)
        self.assertNotIn("dsv42codex", text)

    def test_render_publish_resume_omits_manual_review_section(self):
        draft_text = render_resume(self.match_result())
        publish_text = render_publish_resume(self.match_result())
        self.assertIn("## 需要人工复核", draft_text)
        self.assertNotIn("需要人工复核", publish_text)
        self.assertNotIn("确认所有客户与项目表达符合公开边界", publish_text)
        self.assertIn("## 教育经历", publish_text)

    def test_strip_manual_review_section_stops_at_next_peer_heading(self):
        text = "# 简历\n\n## 项目\n\n内容\n\n## 需要人工复核\n\n- 删除我\n\n## 附录\n\n保留我\n"
        stripped = strip_manual_review_section(text)
        self.assertNotIn("需要人工复核", stripped)
        self.assertNotIn("删除我", stripped)
        self.assertIn("## 附录", stripped)
        self.assertIn("保留我", stripped)

    def test_render_gap_contains_go_gap(self):
        text = render_gap(self.match_result())
        self.assertIn("Go", text)
        self.assertIn("gap", text.lower())
