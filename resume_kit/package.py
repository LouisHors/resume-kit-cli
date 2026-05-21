import json
from dataclasses import asdict
from pathlib import Path

from .corpus import load_corpus
from .jd import analyze_jd
from .llm_guardrails import build_llm_prompt
from .matcher import match_jd
from .profiles import get_profile
from .renderers import render_evidence_map, render_gap, render_resume


def create_package(jd_path, profile_name, out_dir, force=False):
    jd_path = Path(jd_path)
    out_dir = Path(out_dir)
    jd = analyze_jd(jd_path.read_text(encoding="utf-8"))
    result = match_jd(jd, get_profile(profile_name), load_corpus())
    outputs = {
        "resume.md": render_resume(result),
        "gap.md": render_gap(result),
        "llm-prompt.md": build_llm_prompt(result),
        "match.json": json.dumps(asdict(result), ensure_ascii=False, indent=2) + "\n",
        "evidence-map.md": render_evidence_map(result),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name, content in outputs.items():
        path = out_dir / name
        if path.exists() and not force:
            raise FileExistsError(str(path))
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written
