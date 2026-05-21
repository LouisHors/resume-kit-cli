from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_ROOT = Path("/Users/zego/my-code-wiki")


def source_root():
    return DEFAULT_SOURCE_ROOT


SOURCE_PATHS = {
    "fact_baseline": source_root() / "wiki/guides/resume-fact-baseline.md",
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
