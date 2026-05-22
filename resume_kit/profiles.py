from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    name: str
    display_name: str
    base_resume_key: str
    priority_skill_tags: list[str]
    preferred_projects: list[str]
    forbidden_styles: list[str]


PROFILES = {
    "ai-agent": Profile(
        name="ai-agent",
        display_name="AI Agent / AI Coding",
        base_resume_key="resume_ai_agent",
        priority_skill_tags=[
            "agent-workflow",
            "mcp",
            "rag",
            "tool-calling",
            "spec-coding",
            "harness-coding",
            "human-in-the-loop",
            "multi-agent",
        ],
        preferred_projects=[
            "Zego RTC 智能排障系统",
            "Horspowers",
            "document-driven-ai-workflow",
            "zego-delivery-tool-kit",
            "ZegoExpressEngine AI 场景代码生成器",
            "内容采集清洗与多平台分发 Agent 工作流",
        ],
        forbidden_styles=["包装个人项目为公司项目", "虚构 Go 熟练经验"],
    ),
    "solution-expert": Profile(
        name="solution-expert",
        display_name="解决方案专家",
        base_resume_key="resume_solution_expert",
        priority_skill_tags=["rtc", "solution", "delivery", "customer", "troubleshooting"],
        preferred_projects=[
            "实时音视频客户方案交付",
            "在线实时 KTV / 合唱 / 单唱方案",
            "RTC 音频体验优化与问题排查方案",
            "客户接口规范适配与 SDK 再封装方案",
            "方案交付工具链平台",
        ],
        forbidden_styles=["披露方案细节", "披露客户内部参数"],
    ),
    "ios": Profile(
        name="ios",
        display_name="iOS 开发",
        base_resume_key="resume_ios",
        priority_skill_tags=["ios", "objective-c", "swift", "rtc", "audio", "sdk"],
        preferred_projects=[
            "好未来 RTC 中台接口适配",
            "Yalla LiveRoom SDK 二次封装",
            "字节跳动 LiveRoomWrapper iOS",
            "CallKit",
            "AVAudioSession",
        ],
        forbidden_styles=["把方案专家经历写成纯 App 开发"],
    ),
}


def list_profiles():
    return [PROFILES[name] for name in ["ai-agent", "solution-expert", "ios"]]


def get_profile(name):
    try:
        return PROFILES[name]
    except KeyError as exc:
        raise ValueError(f"Unknown profile: {name}") from exc
