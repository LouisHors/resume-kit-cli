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

    evidence = [
        EvidenceItem(
            id="personal-content-distribution-agent",
            source_path=source_by_key["fact_baseline"].path,
            source_section="内容采集清洗与多平台分发 Agent 工作流补充说明",
            profile_tags=["ai-agent"],
            skill_tags=[
                "agent-workflow",
                "mcp",
                "tool-calling",
                "human-in-the-loop",
                "multi-agent",
                "content-pipeline",
                "sqlite",
                "cron",
            ],
            project_name="内容采集清洗与多平台分发 Agent 工作流",
            ownership="personal",
            disclosure_level="public-personal",
            summary="从 OpenClaw 技能演进到多 Agent 内容生产线，覆盖小红书和微信公众号自动化。",
            resume_phrasing=[
                "设计并实践信息抓取、内容清洗与多平台分发 Agent 工作流，串联 RSS / GitHub Trending、LLM 清洗、SQLite / Markdown / Obsidian 状态沉淀、Slack 人工审核，以及小红书 MCP / 微信公众号草稿箱发布链路。",
                "试运营一个月内单篇内容最高浏览量 14w+，多篇内容浏览量 3w+ / 4w+。",
            ],
            raw_excerpt=_excerpt(fact_text, "内容采集清洗与多平台分发 Agent 工作流"),
        ),
        EvidenceItem(
            id="horspowers-skill-system",
            source_path=source_by_key["ai_handbook"].path,
            source_section="Horspowers / 技能系统",
            profile_tags=["ai-agent"],
            skill_tags=[
                "agent-workflow",
                "spec-coding",
                "harness-coding",
                "tool-calling",
                "workflow",
            ],
            project_name="Horspowers",
            ownership="work",
            disclosure_level="public-work-summary",
            summary="围绕 AI coding、技能系统和文档驱动工程化沉淀工作流约束。",
            resume_phrasing=[
                "沉淀 AI coding 技能系统与文档驱动工作流，把需求澄清、计划拆解、执行校验和分支收尾固化为可复用的工程流程。",
            ],
            raw_excerpt=_excerpt(handbook_text, "Horspowers / 技能系统"),
        ),
    ]
    return Corpus(sources=sources, evidence=evidence)


def _excerpt(text, needle, radius=500):
    index = text.find(needle)
    if index < 0:
        return ""
    start = max(0, index - radius)
    end = min(len(text), index + len(needle) + radius)
    return text[start:end].strip()
