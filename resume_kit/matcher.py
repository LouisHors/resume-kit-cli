from .models import MatchResult


RISK_GAP_MESSAGES = {
    "go-language-hard-requirement": "JD 明确要求熟练 Go。当前素材更强的是 Python / Node.js / iOS / TypeScript，应在 gap 文档中说明短期补齐计划，不写成已熟练。",
    "nas-domain-gap": "JD 涉及 NAS / 存储业务。当前素材没有直接 NAS 经验，可用 RTC 排障、多源日志、权限和知识库检索经验做迁移表达。",
    "vector-search-depth-gap": "JD 涉及向量检索 / RAG Pipeline 深度。当前素材有知识库和搜索实践，但 embedding、rerank、评测指标需要补齐表达。",
}


def match_jd(jd, profile, corpus):
    selected = []
    direct = []
    transferable = []

    for item in corpus.evidence:
        score = _score_item(jd, profile, item)
        if score >= 3:
            selected.append(item)
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
    return MatchResult(
        profile=profile.name,
        jd=jd,
        direct_matches=direct,
        transferable_matches=transferable,
        gaps=gaps,
        selected_evidence=selected,
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
