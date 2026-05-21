def render_resume(result):
    lines = [
        f"# 刘豪 - {result.jd.title} 定制简历草稿",
        "",
        "## 定制说明",
        "",
        f"- 目标岗位：{result.jd.title}",
        f"- 匹配方向：{result.profile}",
        "- 本文由本地素材和规则生成，需人工确认后投递。",
        "",
        "## 重点匹配项目",
        "",
    ]
    for item in result.selected_evidence:
        lines.append(f"### {item.project_name}")
        lines.append("")
        lines.append(f"归属：{item.ownership}")
        lines.append("")
        for phrase in item.resume_phrasing:
            lines.append(f"- {phrase}")
        lines.append("")
    lines.extend([
        "## 需要人工复核",
        "",
        "- 根据目标 JD 调整项目顺序和表达强度。",
        "- 确认所有客户与项目表达符合公开边界。",
    ])
    return "\n".join(lines).rstrip() + "\n"


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
