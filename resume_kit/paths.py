import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
_env = os.environ.get("RESUME_KIT_SOURCE_ROOT")
DEFAULT_SOURCE_ROOT = Path(_env) if _env else None


def source_root():
    if DEFAULT_SOURCE_ROOT is None:
        raise RuntimeError("RESUME_KIT_SOURCE_ROOT is not set")
    return DEFAULT_SOURCE_ROOT


SOURCE_PATHS = {
    "fact_baseline": source_root() / "wiki/guides/resume-fact-baseline.md",
    "repo_map": source_root() / "wiki/guides/repository-output-map-2020-2026.md",
    "code_projects": source_root() / "wiki/guides/code-project-material-map.md",
    "customer_solutions": source_root() / "wiki/guides/customer-solution-material-map.md",
    "technical_articles": source_root() / "wiki/guides/technical-article-material-map.md",
    "ai_handbook": source_root() / "wiki/guides/ai-agent-rag-interview-handbook.md",
    "resume_ai_agent": source_root() / "resumes/liuhao-ai-agent.md",
    "resume_solution_expert": source_root() / "resumes/liuhao-solution-expert.md",
    "resume_ios": source_root() / "resumes/liuhao-ios.md",
}


def source_status():
    return [
        {"key": key, "path": str(path), "exists": path.exists()}
        for key, path in SOURCE_PATHS.items()
    ]
