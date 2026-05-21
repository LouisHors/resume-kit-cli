def strip_manual_review_section(text):
    lines = text.splitlines()
    output = []
    skip_level = None
    removed = False

    for line in lines:
        if line.startswith("#"):
            marker, _, title = line.partition(" ")
            if marker and set(marker) == {"#"} and title.strip() == "需要人工复核":
                skip_level = len(marker)
                removed = True
                continue
            if skip_level is not None and marker and set(marker) == {"#"} and len(marker) <= skip_level:
                skip_level = None

        if skip_level is None:
            output.append(line)

    if not removed:
        return text
    return "\n".join(output).rstrip() + "\n"


def formalize_publish_resume_text(text):
    text = strip_manual_review_section(text)
    lines = text.splitlines()
    output = []
    replaced_title = False

    for line in lines:
        if not replaced_title and line.startswith("# "):
            title = line[2:].strip()
            normalized = _normalize_resume_title(title)
            output.append(f"# {normalized}")
            replaced_title = True
            continue
        output.append(line)

    if not output:
        return text
    return "\n".join(output).rstrip() + "\n"


def _normalize_resume_title(title):
    for suffix in ("定制简历草稿", "定制简历初稿", "简历草稿", "简历初稿"):
        if title.endswith(suffix):
            return f"{title[:-len(suffix)]}简历"
    return title


def render_resume(result):
    lines = [
        "# 刘豪 - AI Agent / AI Coding 方向简历初稿",
        "",
        *result.base_header_lines,
        "",
        "## 个人定位",
        "",
        result.base_personal_positioning,
        "",
    ]
    lines.extend([
        "## 核心优势",
        "",
    ])
    for strength in result.base_core_strengths:
        lines.append(f"- {strength}")
    lines.extend([
        "",
        "## 工作经历",
        "",
    ])
    for work in result.base_work_experience:
        lines.append(f"### {work['title']}")
        lines.append("")
        lines.append(work["period"])
        lines.append("")
        for bullet in work["bullets"]:
            lines.append(f"- {bullet}")
        lines.append("")
    lines.extend([
        "## 项目展示",
        "",
    ])
    for item in result.selected_evidence:
        lines.append(f"### {item.project_name}")
        lines.append("")
        lines.append(f"角色：{item.role or item.ownership}")
        lines.append(f"关键词：{'、'.join(item.keywords) if item.keywords else '无'}")
        lines.append(f"项目定位：{item.project_positioning or item.summary}")
        lines.append("主要工作：")
        for work in item.main_work or item.resume_phrasing:
            lines.append(f"- {work}")
        lines.append("可突出成果：")
        for highlight in item.highlight_results or item.resume_phrasing:
            lines.append(f"- {highlight}")
        for sentence in item.capability_phrasing:
            lines.append(f"- {sentence}")
        lines.append("")
    lines.extend([
        "## 技术能力",
        "",
    ])
    capability_lines = []
    seen = set()
    for item in result.selected_evidence:
        for sentence in item.capability_phrasing:
            if sentence not in seen:
                capability_lines.append(sentence)
                seen.add(sentence)
    if not capability_lines:
        capability_lines = [
            "能够基于 AI Agent 工作流实现工具调用、上下文管理和验证闭环。",
        ]
    for sentence in capability_lines:
        lines.append(f"- {sentence}")
    lines.append("")
    lines.extend([
        "## 教育经历",
        "",
    ])
    for line in result.base_education:
        lines.append(line)
    lines.append("")
    lines.extend([
        "## 需要人工复核",
        "",
        "- 根据目标 JD 调整项目顺序和表达强度。",
        "- 确认所有客户与项目表达符合公开边界。",
    ])
    return "\n".join(lines).rstrip() + "\n"


def render_publish_resume(result):
    return formalize_publish_resume_text(render_resume(result))


def render_gap(result):
    lines = [
        f"# {result.jd.title} JD 匹配差异分析",
        "",
        "## 已匹配",
        "",
    ]
    if result.direct_matches:
        for match in result.direct_matches:
            lines.append(f"- {match['project_name']}：{match['reason']}")
    else:
        lines.append("- 暂无直接匹配项。")

    lines.extend(["", "## 可迁移匹配", ""])
    if result.transferable_matches:
        for match in result.transferable_matches:
            lines.append(f"- {match['project_name']}：{match['reason']}")
    else:
        lines.append("- 暂无可迁移匹配项。")

    lines.extend(["", "## Gap / 风险点", ""])
    if result.gaps:
        for gap in result.gaps:
            lines.append(f"- `{gap['id']}`：{gap['message']}")
    else:
        lines.append("- 暂无明显 gap。")
    return "\n".join(lines).rstrip() + "\n"


def render_evidence_map(result):
    lines = ["# 证据映射", ""]
    for item in result.selected_evidence:
        lines.append(f"## {item.id}")
        lines.append("")
        lines.append(f"- 项目：{item.project_name}")
        lines.append(f"- 来源：`{item.source_path}`")
        lines.append(f"- 章节：{item.source_section}")
        lines.append(f"- 归属：{item.ownership}")
        lines.append(f"- 披露等级：{item.disclosure_level}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
