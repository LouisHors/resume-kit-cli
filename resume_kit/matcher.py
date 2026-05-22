from .models import MatchResult


RISK_GAP_MESSAGES = {
    "go-language-hard-requirement": "JD 明确要求熟练 Go。当前素材更强的是 Python / Node.js / iOS / TypeScript，应在 gap 文档中说明短期补齐计划，不写成已熟练。",
    "nas-domain-gap": "JD 涉及 NAS / 存储业务。当前素材没有直接 NAS 经验，可用 RTC 排障、多源日志、权限和知识库检索经验做迁移表达。",
    "vector-search-depth-gap": "JD 涉及向量检索 / RAG Pipeline 深度。当前素材有知识库和搜索实践，但 embedding、rerank、评测指标需要补齐表达。",
}

PROFILE_BASE_RESUME = {
    "ai-agent": {
        "title": "刘豪 - AI Agent / AI Coding 方向简历初稿",
        "header_lines": [
            "手机：15338866734",
            "邮箱：louishors@outlook.com",
            "城市：深圳",
            "性别：男",
            "工作经验：10 年+",
            "求职意向：AI Agent 开发 / AI Coding 工程师 / AI 工具链工程师",
        ],
        "personal_positioning": (
            "长期从事实时音视频 SDK 技术方案、客户交付和 iOS 开发，近一年重点投入 AI Coding、AI Agent、MCP、技能系统和知识库驱动的智能排障工具建设。"
            "具备从业务问题抽象、技术方案设计、工具链实现到落地交付的完整经验，能够把 LLM 能力接入真实工程流程，提升开发、排障、交付和知识沉淀效率。"
        ),
        "core_strengths": [
            "AI Agent 工程实践：熟悉 Agent 的规划、工具调用、上下文管理、技能系统、知识库检索、验证闭环等核心环节，能够将 AI 能力封装为可复用工作流，而不只是停留在提示词使用层面。",
            "AI Coding 方法论：近一年持续实践 Vibe Coding、Spec Coding、Harness Coding。能够通过快速原型探索方向，通过规格文档约束实现边界，通过 Agent harness、技能、工具和验证脚本提升输出稳定性。",
            "工具链与协议理解：了解 Codex、Claude Code、Cursor 等 AI 编程工具的工作方式，实践过 MCP、插件、技能、AGENTS.md/CLAUDE.md 上下文约束、Hook、自动化检查等机制。",
            "领域知识 + AI 结合：拥有 6 年实时音视频 SDK 解决方案经验，能把 RTC 场景、SDK 日志、Themis/Doris 数据、客户工单经验转化为 AI 可执行的排障知识库和决策树。",
            "全链路交付能力：从需求分析、方案设计、代码实现、测试验证、文档编写到客户上线支持均有长期经验，适合 AI 工具、Agent 平台、开发者工具、智能排障、知识工程等岗位。",
        ],
        "work_experience": [
            {
                "title": "深圳市即构科技有限公司 - 高级解决方案专家",
                "period": "2020.04 - 至今",
                "bullets": [
                    "面向实时音视频客户提供 SDK 接入、场景方案设计、Demo/Wrapper 交付、问题定位和上线保障。",
                    "支持过字节跳动、网易、好未来、SOUL、会玩、富聊、微博、Yalla、传音等客户项目，覆盖直播、语聊房、KTV/合唱、在线教育、视频通话、第三方美颜、SDK 再封装等场景。",
                    "近一年将工作重心转向 AI Coding 与 AI Agent 工具建设，围绕 RTC 排障、知识库、交付工具、开发流程自动化沉淀多个项目。",
                    "通过 Codex、Claude Code、Cursor 等工具，把方案设计、开发计划、代码审查、测试验证、文档沉淀等流程结构化为可复用的 Agent 工作流。",
                ],
            },
            {
                "title": "深圳小泊科技有限公司 - iOS 开发",
                "period": "2018.03 - 2020.03",
                "bullets": [
                    "任职于移动开发部门，负责万科长租业务相关 App 开发，覆盖 C 端租客 App「泊寓」、B 端管理 App「小泊伙伴」以及招商公寓等定制项目。",
                    "负责需求确认、技术评估、功能开发、版本迭代、上架维护，以及部分任务分配和进度管理。",
                    "参与 Swift + RxSwift + MVVM 架构项目，负责基础组件、复杂页面、地图找房、登录、详情页、表格联动等模块。",
                ],
            },
            {
                "title": "广东来艾科技有限公司 - iOS 开发",
                "period": "2016.10 - 2018.03",
                "bullets": [
                    "负责社交电商 App「来艾」iOS 端开发，覆盖即时通讯、钱包支付、好友列表、短视频、网络层封装等模块。",
                    "基于融云 SDK、AVFoundation、FMDB、Ping++、Moya、PromiseKit 等完成核心功能开发与性能优化。",
                    "曾将万级好友联系人排序性能从约 500 个/s 优化到约 5w 个/s；项目在 4w 日活、50w 总用户规模下 crash 率保持在 0.1% 以下。",
                ],
            },
            {
                "title": "山东易构软件技术股份有限公司 - iOS 开发",
                "period": "2015.03 - 2016.08",
                "bullets": [
                    "参与公司项目研发，负责 iOS 功能开发、需求对接和项目维护。",
                ],
            },
        ],
        "education": [
            "山东政法学院 - 本科 - 信息工程",
            "2011 - 2015",
            "大学英语六级",
        ],
    },
    "solution-expert": {
        "title": "刘豪 - 解决方案专家方向简历初稿",
        "header_lines": [
            "手机：15338866734",
            "邮箱：louishors@outlook.com",
            "城市：深圳",
            "性别：男",
            "工作经验：10 年+",
            "求职意向：音视频技术支持专家 / 实时音视频解决方案专家 / SDK 解决方案工程师",
        ],
        "personal_positioning": (
            "6 年实时音视频 SDK 解决方案与客户交付经验，早期具备 4 年以上 iOS 一线开发经验。熟悉直播、语聊房、KTV/合唱、在线教育、视频通话、第三方美颜、客户接口规范适配与 SDK 再封装等 RTC 场景，能够从客户需求分析、方案设计、Demo/Wrapper 交付、问题排查到上线保障完成全链路技术支持。"
            "近一年进一步将 AI Coding、知识库和智能排障工具引入解决方案工作，提升复杂问题分析和交付效率。"
        ),
        "core_strengths": [
            "实时音视频场景经验：长期围绕 Zego Express SDK / LiveRoom SDK 做客户方案设计和落地支持，覆盖推拉流、连麦、混流、SEI、音频前处理、自定义采集/渲染、媒体播放器、合唱同步等能力。",
            "客户交付能力：支持过字节跳动、网易、好未来、SOUL、会玩、富聊、微博、Yalla、传音等客户项目，能够在客户业务、SDK 能力、工程实现之间做方案权衡。",
            "方案设计与 Demo 交付：能将客户需求拆解为流程图、接入步骤、关键代码、参数配置、Demo 工程和问题排查清单，帮助客户降低接入成本。",
            "问题定位与上线保障：熟悉 SDK 日志、错误码、质量数据、Themis/Doris 数据分析和客户工单处理，能够定位拉流失败、卡顿、首帧慢、登录失败、混流失败、音频异常等问题。",
            "技术工具建设能力：沉淀过参数配置工具、方案清单工具、智能排障系统、工单知识学习工具等内部平台/脚本，能将重复交付工作工具化。",
        ],
        "work_experience": [
            {
                "title": "深圳市即构科技有限公司 - 高级解决方案专家",
                "period": "2020.04 - 至今",
                "bullets": [
                    "负责实时音视频 SDK 客户的售前/售中/售后技术方案支持，围绕客户业务场景设计 SDK 接入方案并推动项目上线。",
                    "面向直播、语聊房、KTV/合唱、在线教育、视频通话、游戏语音、第三方美颜、客户接口规范适配等场景输出方案文档、关键代码和 Demo 工程。",
                    "支持客户完成 SDK 集成、参数配置、功能验证、性能调优、问题定位和上线保障。",
                    "支持过字节跳动、网易、好未来、SOUL、会玩、富聊、微博、Yalla、传音等客户项目，能在不同行业场景中快速识别音视频技术风险。",
                    "参与和沉淀内部交付工具，包括参数配置管理、方案清单检查、代码审查模块、智能排障系统和 SDK 场景代码生成器等。",
                    "结合 AI Coding 工具，将专家排障经验、SDK 文档、Themis 数据和客户工单沉淀为可复用的知识库与 Agent 工作流。",
                ],
            },
            {
                "title": "深圳小泊科技有限公司 - iOS 开发",
                "period": "2018.03 - 2020.03",
                "bullets": [
                    "任职于移动开发部门，负责万科长租业务相关 App 开发，覆盖 C 端租客 App「泊寓」、B 端管理 App「小泊伙伴」以及招商公寓等定制项目。",
                    "负责需求确认、技术评估、功能开发、版本迭代、上架维护，以及部分任务分配和进度管理。",
                    "参与 Swift + RxSwift + MVVM 架构项目，负责基础组件、复杂页面、地图找房、登录、详情页、表格联动等模块。",
                ],
            },
            {
                "title": "广东来艾科技有限公司 - iOS 开发",
                "period": "2016.10 - 2018.03",
                "bullets": [
                    "负责社交电商 App「来艾」iOS 端开发，覆盖即时通讯、钱包支付、好友列表、短视频、网络层封装等模块。",
                    "基于融云 SDK、AVFoundation、FMDB、Ping++、Moya、PromiseKit 等完成核心功能开发与性能优化。",
                    "曾将万级好友联系人排序性能从约 500 个/s 优化到约 5w 个/s；项目在 4w 日活、50w 总用户规模下 crash 率保持在 0.1% 以下。",
                ],
            },
            {
                "title": "山东易构软件技术股份有限公司 - iOS 开发",
                "period": "2015.03 - 2016.08",
                "bullets": [
                    "参与公司项目研发，负责 iOS 功能开发、需求对接和项目维护。",
                ],
            },
        ],
        "education": [
            "山东政法学院 - 本科 - 信息工程",
            "2011 - 2015",
            "大学英语六级",
        ],
    },
    "ios": {
        "title": "刘豪 - iOS 开发方向简历初稿",
        "header_lines": [
            "手机：15338866734",
            "邮箱：louishors@outlook.com",
            "城市：深圳",
            "性别：男",
            "工作经验：10 年+",
            "求职意向：高级 iOS 开发工程师 / iOS SDK 工程师 / 移动端技术专家",
        ],
        "personal_positioning": (
            "2016 年起全职从事 iOS 开发，2020 年 4 月后转向实时音视频 SDK 解决方案专家岗位，但仍长期围绕 iOS SDK、Demo、Wrapper、客户接入和复杂音视频场景进行技术工作。具备 App 业务开发、iOS 基础能力、性能优化、SDK 集成、音视频场景、客户交付和工具化沉淀经验，适合 iOS App、iOS SDK、音视频 SDK、开发者工具等方向。"
        ),
        "core_strengths": [
            "iOS 基础扎实：熟悉 Swift、Objective-C、UIKit、AVFoundation、CoreLocation、CoreBluetooth、常见架构模式和第三方 SDK 集成。",
            "业务 App 经验完整：曾负责长租公寓、社交电商、B 端管理工具等多个 App 开发，覆盖首页、搜索、地图、登录、支付、IM、短视频、报修、预订签约、复杂表格等模块。",
            "音视频与 SDK 能力突出：2020 年后长期基于 Zego Express SDK / LiveRoom SDK 做 iOS 方向客户方案、Demo、Wrapper 和排障支持，熟悉推拉流、连麦、KTV、合唱、美颜、自定义采集/处理等场景。",
            "性能与工程化意识：有页面加载性能优化、万级数据排序优化、crash 定位、CI/CD、Jenkins、Bugly、Instruments、Mock、Charles、Postman 等实践经验。",
            "沟通与交付能力：从开发岗位转向解决方案专家后，长期面向客户和内部团队沟通需求、拆解技术方案、评估风险并推动上线。",
        ],
        "work_experience": [
            {
                "title": "深圳市即构科技有限公司 - 高级解决方案专家",
                "period": "2020.04 - 至今",
                "bullets": [
                    "负责实时音视频 SDK 客户的 iOS/移动端接入方案设计、Demo/Wrapper 支持、问题定位和上线保障。",
                    "支持字节跳动、网易、好未来、SOUL、会玩、富聊、微博、Yalla、传音等客户项目，覆盖直播、语聊房、KTV/合唱、在线教育、视频通话、第三方美颜、SDK 再封装等场景。",
                    "基于 Zego Express SDK / LiveRoom SDK 输出 iOS Demo、关键代码、接入文档和调试方案。",
                    "参与客户接口规范适配 Wrapper、第三方美颜 Demo、KTV/合唱 Demo、ZegoMediaPlayer 伴奏播放器、自定义音视频采集/处理等方案设计。",
                    "建设交付工具和智能排障工具，将 SDK 接入经验、日志排查经验和客户问题沉淀为可复用流程。",
                ],
            },
            {
                "title": "深圳小泊科技有限公司 - iOS 开发",
                "period": "2018.03 - 2020.03",
                "bullets": [
                    "任职于移动开发部门，负责万科集团长租业务 App 开发，主要产品包括 C 端「泊寓」和 B 端「小泊伙伴」。",
                    "参与需求确认、需求评审、技术评估、任务拆解、开发进度管理、版本迭代和 App 上架。",
                    "负责 App 功能开发与维护，涉及首页、找房、门店/房间详情、预订签约、报修、物资管理、用户带看 CRM 等模块。",
                    "负责 UI 规范、基础组件、Swift 语法糖工具和部分 Flutter 组件封装。",
                ],
            },
            {
                "title": "广东来艾科技有限公司 - iOS 开发",
                "period": "2016.10 - 2018.03",
                "bullets": [
                    "负责社交电商 App「来艾」iOS 端开发，覆盖即时通讯、短视频、钱包支付、好友列表、网络层封装和性能优化。",
                    "基于融云 SDK 实现 IM 模块，基于 AVFoundation 实现短视频拍摄与播放，基于 FMDB 实现万级好友数据存储、排序和检索。",
                    "基于 Ping++ 接入支付宝、微信、银联等支付能力，支持银行卡绑定、实名认证等钱包基础功能。",
                    "基于 Moya + PromiseKit 建设网络统一管理和异步处理能力。",
                    "通过存取逻辑优化，将万级好友联系人排序性能从约 500 个/s 提升到约 5w 个/s；项目在 4w 日活、50w 总用户规模下 crash 率保持在 0.1% 以下。",
                ],
            },
            {
                "title": "山东易构软件技术股份有限公司 - iOS 开发",
                "period": "2015.03 - 2016.08",
                "bullets": [
                    "参与公司项目研发，负责 iOS 功能开发、需求对接和项目维护。",
                ],
            },
        ],
        "education": [
            "山东政法学院 - 本科 - 信息工程",
            "2011 - 2015",
            "大学英语六级",
        ],
    },
}


def match_jd(jd, profile, corpus):
    direct = []
    transferable = []

    for item in corpus.evidence:
        score = _score_item(jd, profile, item)
        if score >= 3:
            direct.append({
                "evidence_id": item.id,
                "project_name": item.project_name,
                "reason": "profile and JD keywords matched",
                "score": score,
            })
        elif score > 0:
            transferable.append({
                "evidence_id": item.id,
                "project_name": item.project_name,
                "reason": "transferable but not primary",
                "score": score,
            })

    gaps = [
        {"id": flag, "message": RISK_GAP_MESSAGES.get(flag, flag)}
        for flag in jd.risk_flags
    ]
    selected = _select_evidence(profile.name, direct, transferable, corpus)
    base_resume = PROFILE_BASE_RESUME.get(profile.name, PROFILE_BASE_RESUME["ai-agent"])
    return MatchResult(
        profile=profile.name,
        jd=jd,
        direct_matches=direct,
        transferable_matches=transferable,
        gaps=gaps,
        selected_evidence=selected,
        base_title=_resolve_base_title(profile.name, jd, base_resume["title"]),
        base_header_lines=base_resume["header_lines"],
        base_personal_positioning=base_resume["personal_positioning"],
        base_core_strengths=base_resume["core_strengths"],
        base_work_experience=base_resume["work_experience"],
        base_education=base_resume["education"],
    )


def _score_item(jd, profile, item):
    score = 0
    if profile.name in item.profile_tags:
        score += 2
    jd_text = " ".join(
        jd.keywords + jd.responsibilities + jd.must_requirements + jd.nice_to_have
    ).lower()
    for tag in item.skill_tags:
        tag_text = tag.replace("-", " ")
        if tag_text in jd_text or tag in jd_text:
            score += 1
    if item.project_name in profile.preferred_projects:
        score += 2
    return score


def _select_evidence(profile_name, direct, transferable, corpus):
    target_ids = {
        "ai-agent": [
            "zego-rtc-troubleshooting-agent",
            "horspowers-skill-system",
            "document-driven-ai-workflow",
            "zego-delivery-tool-kit",
            "zegoexpressengine-ai-code-generator",
            "personal-content-distribution-agent",
        ],
        "solution-expert": [
            "solution-expert-customer-delivery",
            "solution-expert-ktv-scheme",
            "solution-expert-audio-quality-optimization",
            "solution-expert-customer-interface-wrapper",
            "solution-expert-delivery-tool-kit",
        ],
        "ios": [
            "solution-expert-talrtc-wrapper",
            "solution-expert-yalla-wrapper",
            "solution-expert-byte-wrapper",
            "solution-expert-ktv-scheme",
            "solution-expert-third-party-beauty",
            "solution-expert-delivery-tool-kit",
        ],
    }.get(profile_name, [])
    evidence_by_id = {item.id: item for item in corpus.evidence}
    selected_names = set()
    selected = []
    for evidence_id in target_ids:
        item = evidence_by_id.get(evidence_id)
        if item is not None and item.project_name not in selected_names:
            selected.append(item)
            selected_names.add(item.project_name)

    if profile_name == "solution-expert":
        return selected

    for entry in direct:
        item = evidence_by_id.get(entry["evidence_id"])
        if item is not None and item.project_name not in selected_names:
            selected.append(item)
            selected_names.add(item.project_name)

    for entry in transferable:
        item = evidence_by_id.get(entry["evidence_id"])
        if item is not None and item.project_name not in selected_names:
            selected.append(item)
            selected_names.add(item.project_name)

    return selected


def _resolve_base_title(profile_name, jd, default_title):
    if profile_name == "solution-expert":
        jd_title = jd.title or ""
        if "音视频技术支持专家" in jd_title or ("音视频" in jd_title and "技术支持" in jd_title):
            return "刘豪 - 音视频技术支持专家简历初稿"
        return default_title
    return default_title
