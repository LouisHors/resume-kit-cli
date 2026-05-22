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
    role: str = ""
    keywords: list[str] = field(default_factory=list)
    project_positioning: str = ""
    main_work: list[str] = field(default_factory=list)
    highlight_results: list[str] = field(default_factory=list)
    capability_phrasing: list[str] = field(default_factory=list)


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
    base_title: str = ""
    base_header_lines: list[str] = field(default_factory=list)
    base_personal_positioning: str = ""
    base_core_strengths: list[str] = field(default_factory=list)
    base_work_experience: list[dict] = field(default_factory=list)
    base_education: list[str] = field(default_factory=list)
