from dataclasses import dataclass, field


@dataclass(frozen=True)
class SourceDoc:
    key: str
    path: str
    text: str


@dataclass(frozen=True)
class EvidenceItem:
    id: str
    source_path: str
    source_section: str
    profile_tags: list[str]
    skill_tags: list[str]
    project_name: str
    ownership: str
    disclosure_level: str
    summary: str
    resume_phrasing: list[str]
    raw_excerpt: str


@dataclass(frozen=True)
class Corpus:
    sources: list[SourceDoc] = field(default_factory=list)
    evidence: list[EvidenceItem] = field(default_factory=list)


@dataclass(frozen=True)
class JDAnalysis:
    title: str
    responsibilities: list[str]
    must_requirements: list[str]
    nice_to_have: list[str]
    keywords: list[str]
    inferred_profile: str
    risk_flags: list[str]


@dataclass(frozen=True)
class MatchResult:
    profile: str
    jd: JDAnalysis
    direct_matches: list[dict]
    transferable_matches: list[dict]
    gaps: list[dict]
    selected_evidence: list[EvidenceItem]
