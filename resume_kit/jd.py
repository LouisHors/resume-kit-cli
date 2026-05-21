import re

from .models import JDAnalysis


KEYWORDS = [
    "AI Agent",
    "Agentic RAG",
    "Agent",
    "RAG",
    "MCP",
    "工具调用",
    "Go",
    "AI coding",
    "NAS",
    "向量检索",
    "全文搜索",
    "iOS",
    "RTC",
    "SDK",
    "解决方案",
    "客户",
    "交付",
]


def analyze_jd(text):
    title = _extract_title(text)
    responsibilities = _extract_numbered_after(
        text,
        headers=["岗位职责", "职责"],
        stop_headers=["岗位要求", "任职要求", "必须", "加分项", "优先"],
    )
    must = _extract_numbered_after(
        text,
        headers=["必须"],
        stop_headers=["加分项", "优先"],
    )
    if not must:
        must = _extract_numbered_after(
            text,
            headers=["岗位要求", "任职要求"],
            stop_headers=["加分项", "优先"],
        )
    nice = _extract_numbered_after(
        text,
        headers=["加分项", "优先"],
        stop_headers=[],
    )
    keywords = [kw for kw in KEYWORDS if kw.lower() in text.lower()]
    return JDAnalysis(
        title=title,
        responsibilities=responsibilities,
        must_requirements=must,
        nice_to_have=nice,
        keywords=keywords,
        inferred_profile=_infer_profile(text),
        risk_flags=_risk_flags(text),
    )


def _extract_title(text):
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
        if stripped:
            return stripped
    return "未命名岗位"


def _extract_numbered_after(text, headers, stop_headers):
    lines = text.splitlines()
    capture = False
    items = []
    for line in lines:
        stripped = line.strip().strip("*：:")
        if any(stripped.startswith(header) for header in headers):
            capture = True
            continue
        if capture and any(stripped.startswith(header) for header in stop_headers):
            break
        if capture:
            match = re.match(r"^\d+[.)、]\s*(.+)$", stripped)
            if match:
                items.append(match.group(1).strip())
    return items


def _infer_profile(text):
    lower = text.lower()
    if "agent" in lower or "rag" in lower or "mcp" in lower:
        return "ai-agent"
    if "ios" in lower or "swift" in lower or "objective-c" in lower:
        return "ios"
    return "solution-expert"


def _risk_flags(text):
    flags = []
    if re.search(r"\bGo\b|Go 语言|golang", text, re.I):
        flags.append("go-language-hard-requirement")
    if "NAS" in text or "存储" in text:
        flags.append("nas-domain-gap")
    if "向量" in text or "embedding" in text.lower():
        flags.append("vector-search-depth-gap")
    return flags
