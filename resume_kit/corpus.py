from .errors import MissingSourceError
from .models import Corpus, EvidenceItem, SourceDoc
from .paths import SOURCE_PATHS


def _read_source(key, path):
    if not path.exists():
        raise MissingSourceError("Required source file does not exist", {"path": str(path)})
    return SourceDoc(key=key, path=str(path), text=path.read_text(encoding="utf-8"))


def load_corpus():
    sources = [_read_source(key, path) for key, path in SOURCE_PATHS.items()]
    source_by_key = {source.key: source for source in sources}
    fact_text = source_by_key["fact_baseline"].text
    handbook_text = source_by_key["ai_handbook"].text
    code_projects_text = source_by_key["code_projects"].text
    resume_text = source_by_key["resume_ai_agent"].text
    solution_text = source_by_key["resume_solution_expert"].text
    ios_text = source_by_key["resume_ios"].text

    evidence = [
        _evidence(
            id="solution-expert-delivery-tool-kit",
            source_path=source_by_key["resume_solution_expert"].path,
            source_section="重点项目经历",
            profile_tags=["solution-expert"],
            skill_tags=["rtc", "solution", "delivery", "customer", "workflow", "tool-calling"],
            project_name="方案交付工具链平台",
            ownership="work",
            disclosure_level="public-work-summary",
            summary="建设面向解决方案交付的工具链，覆盖参数配置、方案检查和 code review 等流程。",
            resume_phrasing=[
                "负责交付工具链整合，将参数配置、方案 checklist、代码 review checklist 和交付文档模板串成可复用工作流。",
            ],
            role="架构设计 / 方案设计 / 工具实现",
            keywords=["工作流 SOP", "参数配置", "方案 checklist", "代码 review checklist", "交付工具链"],
            project_positioning="面向内部的方案交付工具链平台，将参数配置、方案 checklist、代码 review checklist 和交付文档模板沉淀为可复用 SOP。",
            main_work=[
                "分析需求收集、方案编写、参数配置、集成复查等离散动作的流程断点。",
                "将飞书表格映射为结构化数据，打通需求、方案和复查环节。",
                "通过多轮重构把原型验证、功能整合和 UI/UX 优化串成完整平台。",
            ],
            highlight_results=[
                "累计支撑 100+ 人次使用。",
                "减少人为填写错误和学习流程成本。",
            ],
            capability_phrasing=[
                "能够基于交付 checklist 和结构化表单实现流程标准化。",
            ],
            raw_excerpt=_excerpt(solution_text, "zego-delivery-tool-kit"),
        ),
        _evidence(
            id="solution-expert-customer-delivery",
            source_path=source_by_key["resume_solution_expert"].path,
            source_section="重点项目经历",
            profile_tags=["solution-expert"],
            skill_tags=["rtc", "customer", "solution", "delivery", "troubleshooting"],
            project_name="某实时音视频客户方案交付项目",
            ownership="work",
            disclosure_level="public-work-summary",
            summary="面向直播、语聊房、在线教育、视频通话等场景的 RTC 客户方案交付。",
            resume_phrasing=[
                "面向不同行业客户设计 RTC 接入方案，覆盖角色关系、房间模型、推拉流策略、连麦、混流、SEI、异常恢复和上线保障。",
            ],
            role="高级解决方案专家 / 方案设计 / 上线保障",
            keywords=["RTC", "SDK 接入", "客户方案", "上线保障", "直播", "语聊房", "在线教育", "视频通话"],
            project_positioning="面向不同行业客户的实时音视频方案交付项目，将客户业务目标抽象为 SDK 接入链路、联调清单和上线风险控制方案。",
            main_work=[
                "根据客户业务目标拆解音视频链路，包括角色关系、房间模型、推流/拉流策略、连麦逻辑、混流/转推、SEI 同步、媒体播放器、音频前处理和异常恢复。",
                "输出流程图、方案文档、关键代码、Demo 工程和接入检查清单，帮助客户研发团队快速完成 SDK 集成。",
                "参与上线前联调与风险排查，重点关注环境配置、鉴权、房间登录、推拉流、设备权限、网络质量和 SDK 版本兼容。",
            ],
            highlight_results=[
                "面向字节跳动、网易、好未来、SOUL、会玩、富聊、微博、Yalla、传音等客户完成跨场景 RTC 方案交付。",
                "围绕客户上线后的高频问题沉淀排查文档、参数模板和工具化能力，推动交付从单点支持升级为可复用流程。",
            ],
            capability_phrasing=[
                "能够基于客户业务目标拆解 RTC 接入链路，并完成方案文档、Demo、联调和上线保障。",
            ],
            raw_excerpt=_excerpt(solution_text, "实时音视频客户解决方案交付"),
        ),
        _evidence(
            id="solution-expert-customer-interface-wrapper",
            source_path=source_by_key["resume_solution_expert"].path,
            source_section="重点项目经历",
            profile_tags=["solution-expert"],
            skill_tags=["rtc", "customer", "solution", "wrapper", "audio-routing"],
            project_name="某客户接口规范适配与 SDK 再封装项目",
            ownership="work",
            disclosure_level="public-work-summary",
            summary="面向客户既有接口规范的 SDK 再封装与 Demo 支持。",
            resume_phrasing=[
                "为已有接口规范明确的客户设计 RTC Wrapper，将初始化、进房、角色切换、推拉流、回调和错误码等能力收敛到客户侧接口适配层。",
            ],
            role="方案设计 / iOS Wrapper 支持 / 接口联调",
            keywords=["SDK 再封装", "RTC", "Wrapper", "接口规范", "接口适配", "Demo"],
            project_positioning="面向客户既有接口规范与中台接入诉求，提供贴近客户调用习惯的 RTC Wrapper、接口适配说明和验证 Demo。",
            main_work=[
                "分析客户接口规范与底层 RTC SDK 在初始化、进房、角色切换、推流/拉流、回调、环境配置等方面的映射关系。",
                "通过 Wrapper 暴露符合客户既有接口习惯的方法名、回调结构和错误码表达，降低客户研发团队的接入理解成本。",
                "对无法完全对齐的 SDK 行为，在接口注释和方案文档中明确差异、限制和注意事项。",
                "提供连麦、跨频道转发、中台接口适配等场景 Demo，方便客户验证封装层行为与业务链路。",
            ],
            highlight_results=[
                "覆盖直播、语聊、在线教育等多种业务场景的客户接口规范适配与多模式设备参数对齐。",
            ],
            capability_phrasing=[
                "能够基于客户接口规范实现 RTC SDK 再封装、接口适配和联调验证。",
            ],
            raw_excerpt=_excerpt(solution_text, "Yalla LiveRoom SDK 二次封装"),
        ),
        _evidence(
            id="solution-expert-audio-quality-optimization",
            source_path=source_by_key["resume_solution_expert"].path,
            source_section="重点项目经历",
            profile_tags=["solution-expert"],
            skill_tags=["rtc", "customer", "solution", "audio", "troubleshooting"],
            project_name="某 RTC 音频体验优化与问题排查项目",
            ownership="work",
            disclosure_level="public-work-summary",
            summary="面向 RTC 现网音频问题的体验优化、排障分析和方案沉淀。",
            resume_phrasing=[
                "围绕声卡、音量、音质、外放保真、麦上麦下路由等高频音频问题，输出排查报告、优化方案和参数建议。",
            ],
            role="方案设计 / 问题排查 / 体验优化",
            keywords=["音频路由", "声卡适配", "音量调整", "音质优化", "外放保真", "排障报告"],
            project_positioning="面向 RTC 客户现网音频体验问题，将个案排障抽象为可复用的音频链路分析、参数建议和优化方案。",
            main_work=[
                "分析麦克风占用、音频路由、媒体音量/通话音量、外放、耳返、音效和第三方声卡等链路差异。",
                "结合客户现网现象、SDK 日志、设备环境和参数配置，定位音量异常、音质下降、声卡兼容和外放保真等问题。",
                "将处理过程沉淀为问题报告、优化方案和可复用的排查 checklist。",
            ],
            highlight_results=[
                "横切声卡兼容、音量调整和音质提升等音频优化工作，覆盖多个客户场景。",
                "将音频问题排查经验整合到智能排障系统，形成可复用的排障模板和复用材料。",
            ],
            capability_phrasing=[
                "能够基于 SDK 日志、设备环境和音频链路分析定位 RTC 音频体验问题，并沉淀优化方案。",
            ],
            raw_excerpt=_excerpt(source_by_key["customer_solutions"].text, "横切优化代表"),
        ),
        _evidence(
            id="solution-expert-ktv-scheme",
            source_path=source_by_key["resume_solution_expert"].path,
            source_section="重点项目经历",
            profile_tags=["solution-expert"],
            skill_tags=["rtc", "solution", "audio", "KTV", "demo"],
            project_name="某在线实时 KTV / 合唱 / 单唱项目",
            ownership="work",
            disclosure_level="public-work-summary",
            summary="在线 KTV、实时合唱、双人轮唱、单唱等复杂音频娱乐场景方案。",
            resume_phrasing=[
                "围绕在线 KTV、实时合唱、双人轮唱等复杂音频场景，设计基于 ZegoExpressEngine SDK 的 iOS 侧关键能力组合。",
            ],
            role="方案设计 / Demo 支持 / 音频链路设计",
            keywords=["KTV", "实时合唱", "单唱", "伴奏播放器", "SEI", "音频对齐", "自定义音频采集"],
            project_positioning="围绕在线 KTV、实时合唱、双人轮唱和单唱等复杂音频场景，设计完整业务流程、关键 SDK 能力组合和联调方案。",
            main_work=[
                "设计 SDK 初始化、进房、推流/拉流、点歌、播放伴奏、开始演唱、角色切换、停止演唱、退出房间等完整流程。",
                "基于 ZegoMediaPlayer 封装伴奏播放器，处理播放控制、进度回调、状态同步和伴奏混入推流。",
                "结合 SDK 音频数据回调、自定义音频采集和拉流对齐能力，设计人声复用与合唱同步方案。",
            ],
            highlight_results=[
                "覆盖 KTV、海外合唱、游戏化 KTV、单唱/合唱等复杂音频娱乐场景的项目交付。",
            ],
            capability_phrasing=[
                "能够基于伴奏播放器、SEI、音频对齐和自定义采集设计在线 KTV、实时合唱和单唱方案。",
            ],
            raw_excerpt=_excerpt(solution_text, "KTV / 合唱 / 伴奏播放器 iOS 方案"),
        ),
        _evidence(
            id="solution-expert-third-party-beauty",
            source_path=source_by_key["resume_solution_expert"].path,
            source_section="重点项目经历",
            profile_tags=["solution-expert"],
            skill_tags=["rtc", "solution", "video", "beauty", "demo"],
            project_name="某第三方美颜 SDK 集成项目",
            ownership="work",
            disclosure_level="public-work-summary",
            summary="第三方美颜 SDK 接入与 iOS Demo 支持。",
            resume_phrasing=[
                "为客户提供 Zego SDK 与第三方美颜 SDK 组合使用的 iOS Demo 和接入说明，覆盖相芯、商汤、百度、火山等美颜 SDK。",
            ],
            role="iOS Demo 支持 / 音视频链路设计",
            keywords=["自定义视频采集", "视频前处理", "FaceUnity", "商汤", "百度", "火山美颜"],
            project_positioning="面向客户第三方美颜接入需求的 iOS Demo 与链路设计。",
            main_work=[
                "设计两类接入路径：自定义视频采集 + ZegoExpressEngine，以及 ZegoExpressEngine 自定义视频处理回调。",
                "梳理不同美颜 SDK 对 CVPixelBuffer、CMSampleBuffer、OpenGL/Texture 等数据结构的处理方式。",
                "封装第三方美颜与 Zego 推流链路，说明证书、Bundle ID、素材资源、SDK 授权等常见注意事项。",
            ],
            highlight_results=[
                "帮助客户快速验证“采集 -> 美颜处理 -> 推流”的完整链路。",
                "降低美颜接入阶段的格式理解成本。",
            ],
            capability_phrasing=[
                "能够基于视频处理链路实现第三方美颜接入与 Demo 支持。",
            ],
            raw_excerpt=_excerpt(solution_text, "第三方美颜 SDK 集成方案"),
        ),
        
                # --- iOS SDK 开发与维护项目（合并） ---
        _evidence(
            id="ios-sdk-wrapper-dev",
            source_path=source_by_key["fact_baseline"].path,
            source_section="解决方案 / iOS 核心代码产出",
            profile_tags=["ios", "solution-expert"],
            skill_tags=["ios", "objective-c", "sdk", "rtc", "wrapper", "audio-routing"],
            project_name="RTC SDK 二次封装与引擎适配层开发（iOS）",
            ownership="work",
            disclosure_level="public-work-summary",
            summary="面向好未来、Yalla、字节跳动等头部客户，基于 Objective-C 完成 Zego RTC SDK 的 iOS 侧二次封装、引擎适配层开发和 Wrapper 设计，并负责长期维护与 xcframework 打包链路。",
            resume_phrasing=[
                "面向好未来、Yalla、字节跳动等头部客户，基于 Objective-C 完成 Zego RTC SDK 的 iOS 侧二次封装、引擎适配层开发和 Wrapper 设计，并负责长期维护。",
            ],
            role="iOS SDK 开发 / 引擎适配层设计 / 长期维护",
            keywords=["Objective-C", "RTC", "SDK 封装", "Wrapper", "引擎适配层", "xcframework", "音频路由"],
            project_positioning="面向好未来、Yalla、字节跳动等头部客户的 RTC SDK iOS 侧二次封装与引擎适配层开发项目，完成接口对齐、差异屏蔽、错误码统一，并负责 xcframework 打包链路和长期维护。",
            main_work=[
                "基于 Objective-C 实现 RTC 引擎适配层和 SDK Wrapper 封装，覆盖房间管理、推拉流控制、跨频道转发、媒体设备控制、回调分发和异常链路处理。",
                "处理音频会话 hook、volume type、DeviceMode 透传、MediaPlayer 参数映射等差异化能力，以及回调与超时逻辑对齐、错误码统一映射、默认参数收敛等 SDK 差异屏蔽工作。",
                "负责 xcframework 打包链路建设与维护，长期跟进 SDK 版本升级的接口兼容性验证和客户联调问题定位。",
            ],
            highlight_results=[
                "完成好未来培优中台 iOS 侧 RTC 引擎适配层开发与交付。",
                "完成 Yalla iOS 侧 LiveRoom SDK 兼容层开发与交付，覆盖音频路由、设备模式和播放器参数等关键差异化能力。",
                "完成字节跳动 iOS 侧 LiveRoom SDK Wrapper 开发与交付，覆盖房间、推拉流、跨频道转发和错误码等核心能力。",
            ],
            capability_phrasing=[
                "能够基于 Objective-C 完成 RTC SDK 的 iOS 侧二次封装、引擎适配层开发、Wrapper 设计和 xcframework 打包链路维护。",
            ],
            raw_excerpt=_excerpt(fact_text, "好未来 RTC 中台接口适配"),
        ),
_evidence(
            id="zego-delivery-tool-kit",
            source_path=source_by_key["fact_baseline"].path,
            source_section="交付工具链与 AI coding/harness 产物",
            profile_tags=["ai-agent"],
            skill_tags=["agent-workflow", "tool-calling", "workflow", "spec-coding", "harness-coding"],
            project_name="zego-delivery-tool-kit",
            ownership="work",
            disclosure_level="public-work-summary",
            summary="建设交付工具链，覆盖参数配置、方案检查和 code review 等流程。",
            resume_phrasing=[
                "负责交付工具链整合，将参数配置、方案 checklist、代码 review checklist 和交付文档模板串成可复用工作流。",
            ],
            role="架构设计 / 方案设计 / 工具实现",
            keywords=["工作流 SOP", "Vibe Coding", "Spec Coding", "参数配置", "方案 checklist", "代码 review checklist"],
            project_positioning="面向内部的交付工具链平台，将离散的飞书表格流程整合为页面约束的 SOP 化交付流程。",
            main_work=[
                "分析需求收集、方案编写、参数配置、集成复查等离散动作的流程断点。",
                "将飞书表格映射为结构化数据，打通需求、方案和复查环节。",
                "通过多轮重构把原型验证、功能整合和 UI/UX 优化串成完整平台。",
            ],
            highlight_results=[
                "累计支撑 100+ 人次使用。",
                "减少人为填写错误和学习流程成本。",
            ],
            capability_phrasing=[
                "能够基于交付 checklist 和结构化表单实现流程标准化。",
            ],
            raw_excerpt=_excerpt(fact_text, "zego-delivery-tool-kit"),
        ),
        _evidence(
            id="document-driven-ai-workflow",
            source_path=source_by_key["code_projects"].path,
            source_section="AI / Agent / AI coding",
            profile_tags=["ai-agent"],
            skill_tags=["agent-workflow", "context-engineering", "workflow", "spec-coding", "human-in-the-loop"],
            project_name="document-driven-ai-workflow",
            ownership="personal",
            disclosure_level="public-personal",
            summary="从文档驱动实践中抽象出的 AI 协作工作流。",
            resume_phrasing=[
                "设计面向文档的 AI 协作工作流，让需求、设计、计划和验收可以跨会话持续传递。",
            ],
            role="方法论设计 / 工作流抽象 / 工程实践",
            keywords=["Document-driven", "AI 协作", "上下文管理", "跨 session", "任务连续性"],
            project_positioning="把一次性 prompt 升级为可持续协作的文档驱动 AI 工作流，用文档承接需求、设计、计划和任务。",
            main_work=[
                "设计文档结构，让 AI 能从需求澄清、设计决策、实施计划到验收复盘持续恢复上下文。",
                "把任务断裂、上下文丢失和知识传递问题收敛到文档工作流中。",
                "为后续技能化和自动化工作流升级提供稳定抽象。",
            ],
            highlight_results=[
                "形成可复用的文档驱动协作骨架。",
                "成为 Horspowers 技能系统升级的前置沉淀。",
            ],
            capability_phrasing=[
                "能够基于文档驱动开发实现跨会话的任务连续性。",
            ],
            raw_excerpt=_excerpt(code_projects_text, "document-driven-ai-workflow"),
        ),
        _evidence(
            id="horspowers-skill-system",
            source_path=source_by_key["resume_ai_agent"].path,
            source_section="AI Coding 工作流与技能系统实践",
            profile_tags=["ai-agent"],
            skill_tags=["agent-workflow", "spec-coding", "harness-coding", "workflow", "human-in-the-loop", "multi-agent"],
            project_name="Horspowers",
            ownership="work",
            disclosure_level="public-work-summary",
            summary="将文档驱动实践升级为可触发、可验证、可复用的技能/工作流体系。",
            resume_phrasing=[
                "把需求澄清、方案设计、实施计划、测试驱动、代码审查和验证收尾封装成可复用的 AI 技能与工作流。",
            ],
            role="AI 工作流设计 / 技能编排 / 工程实践",
            keywords=["Vibe Coding", "Spec Coding", "Harness Coding", "技能系统", "Subagent", "TDD", "文档驱动开发"],
            project_positioning="把 document-driven-ai-workflow 升级为技能 / 工作流体系，让 AI 开发过程具备触发、约束和验证门禁。",
            main_work=[
                "使用 AGENTS.md、CLAUDE.md 和技能文档为 AI Coding 工具提供稳定上下文和流程约束。",
                "设计 brainstorming -> planning -> execution -> verification -> review 的开发节奏。",
                "在复杂任务中使用 subagent 并行探索、实现和验证。",
            ],
            highlight_results=[
                "形成从想法到可验证代码的 AI Coding 方法论。",
                "让工作流可复用、可审查、可恢复。",
            ],
            capability_phrasing=[
                "能够基于技能系统和验证门禁实现可复用的 AI Coding 工作流。",
            ],
            raw_excerpt=_excerpt(handbook_text, "Horspowers / 技能系统"),
        ),
        _evidence(
            id="zego-rtc-troubleshooting-agent",
            source_path=source_by_key["resume_ai_agent"].path,
            source_section="重点项目经历",
            profile_tags=["ai-agent"],
            skill_tags=["agent-workflow", "mcp", "tool-calling", "rag", "knowledge-base", "troubleshooting"],
            project_name="Zego RTC 智能排障系统",
            ownership="work",
            disclosure_level="public-work-summary",
            summary="面向 Zego Native RTC SDK 的 AI 驱动排障系统。",
            resume_phrasing=[
                "把客户问题描述、参数提取、场景匹配、Themis 查询、日志交叉验证和根因分析封装为 Agent 可执行流程。",
            ],
            role="方案设计 / AI 工作流设计 / 工具实现",
            keywords=["AI Agent", "Codex", "Themis", "Apache Doris", "SDK 日志", "知识图谱", "技能系统", "MCP", "Python"],
            project_positioning="面向 RTC SDK 的垂直领域 Agentic RAG / Tool-augmented troubleshooting system。",
            main_work=[
                "设计排障技能，将客户问题处理过程拆解为可执行步骤。",
                "设计工单学习、日志下载和经验投稿等配套技能，形成闭环。",
                "将错误码、字段 schema、排查决策树和版本注意事项沉淀为知识库。",
                "通过字段白名单、字段别名归一、只读 SQL 和安全校验降低幻觉和错误查询风险。",
            ],
            highlight_results=[
                "把依赖专家经验的排障流程结构化、工具化。",
                "建立适合企业内部场景的 AI Agent harness。",
            ],
            capability_phrasing=[
                "能够基于知识库、工具调用和决策树实现垂直领域排障 Agent。",
            ],
            raw_excerpt=_excerpt(resume_text, "Zego RTC 智能排障系统"),
        ),
        _evidence(
            id="zegoexpressengine-ai-code-generator",
            source_path=source_by_key["resume_ai_agent"].path,
            source_section="重点项目经历",
            profile_tags=["ai-agent"],
            skill_tags=["spec-coding", "tool-calling", "code-generation", "sdk", "demo"],
            project_name="ZegoExpressEngine AI 场景代码生成器",
            ownership="work",
            disclosure_level="public-work-summary",
            summary="面向 ZegoExpressEngine SDK 的 AI 场景代码生成器。",
            resume_phrasing=[
                "把客户场景方案结构化为 SDL / ICL，再生成可运行 iOS Demo，减少方案文档到代码实现的理解偏差。",
            ],
            role="方案设计 / 架构设计",
            keywords=["Spec Coding", "SDL", "ICL", "代码生成", "SDK 契约", "场景编排", "Demo 生成"],
            project_positioning="把方案设计前置为结构化规格，再由 AI 生成受 SDK 契约约束的可运行 Demo。",
            main_work=[
                "设计 SDL 表达角色、数据流和业务意图。",
                "设计 ICL 约束 SDK API 签名、参数、调用顺序和前置条件。",
                "搭建场景选择、规格输出、约束校验和模板组装链路。",
            ],
            highlight_results=[
                "降低 AI 直接生成 SDK 调用代码的随机性。",
                "把解决方案经验抽象为可机器消费的场景模型。",
            ],
            capability_phrasing=[
                "能够基于结构化规格实现场景代码生成与 Demo 交付。",
            ],
            raw_excerpt=_excerpt(resume_text, "ZegoExpressEngine AI 场景代码生成器"),
        ),
        _evidence(
            id="personal-content-distribution-agent",
            source_path=source_by_key["resume_ai_agent"].path,
            source_section="重点项目经历",
            profile_tags=["ai-agent"],
            skill_tags=["agent-workflow", "multi-agent", "mcp", "content-pipeline", "human-in-the-loop"],
            project_name="内容采集清洗与多平台分发 Agent 工作流",
            ownership="personal",
            disclosure_level="public-personal",
            summary="从 OpenClaw 技能演进到多 Agent 内容生产线。",
            resume_phrasing=[
                "设计并实践信息抓取、内容清洗与多平台分发 Agent 工作流，串联 RSS / GitHub Trending、LLM 清洗、SQLite / Markdown / Obsidian 状态沉淀、Slack 人工审核，以及小红书 MCP / 微信公众号草稿箱发布链路。",
                "试运营一个月内单篇内容最高浏览量 14w+，多篇内容浏览量 3w+ / 4w+。",
            ],
            role="个人项目 / Agent 工作流设计 / 自动化工具实现",
            keywords=["OpenClaw", "Multi-agent Workflow", "MCP", "RSS", "SQLite", "Kimi", "Slack", "Obsidian", "小红书", "微信公众号"],
            project_positioning="个人内容自动化项目，从 OpenClaw 技能演进为信息抓取、内容清洗、人工审核和多平台分发的 Agent 工作流。",
            main_work=[
                "设计从多源抓取到生成、清洗、排期、审核、发布的端到端流程。",
                "在小红书链路中使用 SQLite、Kimi、cron 和 Slack 人工审核完成发布闭环。",
                "在微信公众号链路中使用多 Agent 分工、Heartbeat / Cron 和 Markdown 归档完成内容生产。",
            ],
            highlight_results=[
                "完成从单一 OpenClaw 技能到多 Agent 内容生产线的演进。",
                "小红书试运营一个月内，单篇最高浏览量 14w+。",
            ],
            capability_phrasing=[
                "能够基于多 Agent 编排实现内容抓取、清洗、审核与分发闭环。",
            ],
            raw_excerpt=_excerpt(resume_text, "内容采集清洗与多平台分发 Agent 工作流"),
        ),
    ]
    return Corpus(sources=sources, evidence=evidence)


def _evidence(**kwargs):
    return EvidenceItem(**kwargs)


def _excerpt(text, needle, radius=500):
    index = text.find(needle)
    if index < 0:
        return ""
    start = max(0, index - radius)
    end = min(len(text), index + len(needle) + radius)
    return _sanitize_excerpt(text[start:end].strip())


def _sanitize_excerpt(text):
    return (
        text.replace("Codex++", "AI coding 工具")
        .replace("DSV4", "本地适配器")
        .replace("dsv42codex", "本地适配器")
    )
