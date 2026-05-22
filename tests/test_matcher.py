import unittest
from pathlib import Path

from resume_kit.corpus import load_corpus
from resume_kit.jd import analyze_jd
from resume_kit.matcher import match_jd
from resume_kit.profiles import get_profile


FIXTURE = Path(__file__).parent / "fixtures" / "jd_ai_agent.md"
VOICE_SUPPORT_JD = """音视频技术支持专家-火山引擎
职位描述
1、负责为客户提供专业技术支持，高效定位、分析并解决复杂技术问题；
2、主动识别与抽象现网共性问题及隐患，协同产品团队推动优化，持续提升产品稳定性与易用性；
3、通过编写知识库文档、组织内部培训和开发运维工具，赋能并提升一线团队的整体技术服务水平。
职位要求
1、计算机或相关专业，具备3年以上云计算或CDN领域的技术支持、运维或研发经验；
2、扎实掌握TCP/IP、HTTP、DNS等网络协议；深入理解CDN调度机制、缓存工作原理；熟悉RTMP、HLS、WebRTC等流媒体协议及音视频编解码基础；
3、熟练使用Linux操作系统，至少掌握Python或Go一种编程语言，具备日志分析及自动化工具开发的实际经验；
4、思维逻辑严密，拥有出色的跨部门沟通协调能力与客户服务意识。
"""


class MatcherTests(unittest.TestCase):
    def test_match_ai_agent_jd_selects_personal_agent_evidence(self):
        jd = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        result = match_jd(jd, get_profile("ai-agent"), load_corpus())
        ids = {item.id for item in result.selected_evidence}
        self.assertIn("personal-content-distribution-agent", ids)

    def test_match_ai_agent_jd_selects_fixed_project_pool_in_priority_order(self):
        jd = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        result = match_jd(jd, get_profile("ai-agent"), load_corpus())
        self.assertEqual(
            [item.project_name for item in result.selected_evidence],
            [
                "Zego RTC 智能排障系统",
                "Horspowers",
                "document-driven-ai-workflow",
                "zego-delivery-tool-kit",
                "ZegoExpressEngine AI 场景代码生成器",
                "内容采集清洗与多平台分发 Agent 工作流",
            ],
        )

    def test_go_requirement_is_gap_not_direct_match(self):
        jd = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        result = match_jd(jd, get_profile("ai-agent"), load_corpus())
        self.assertTrue(any(gap["id"] == "go-language-hard-requirement" for gap in result.gaps))

    def test_solution_expert_projects_are_grouped_by_solution_type(self):
        jd = analyze_jd(VOICE_SUPPORT_JD)
        result = match_jd(jd, get_profile("solution-expert"), load_corpus())
        project_names = [item.project_name for item in result.selected_evidence]

        self.assertIn("某在线实时 KTV / 合唱 / 单唱项目", project_names)
        self.assertIn("某客户接口规范适配与 SDK 再封装项目", project_names)
        self.assertIn("某实时音视频客户方案交付项目", project_names)
        self.assertIn("某 RTC 音频体验优化与问题排查项目", project_names)
        self.assertNotIn("第三方美颜 SDK 集成方案", project_names)
        for customer_specific_title in [
            "好未来 RTC 中台接口适配",
            "Yalla LiveRoom SDK 二次封装",
            "字节跳动 LiveRoomWrapper iOS",
        ]:
            self.assertNotIn(customer_specific_title, project_names)

        ktv = next(item for item in result.selected_evidence if "在线实时 KTV" in item.project_name)

        delivery = next(item for item in result.selected_evidence if "实时音视频客户方案交付" in item.project_name)
        delivery_text = "\n".join(delivery.highlight_results)
        self.assertIn("传音", delivery_text); self.assertNotIn("具体项目", delivery_text)
        self.assertNotIn("表达时", delivery_text)
