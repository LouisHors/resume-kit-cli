# resume-kit

`resume-kit` is a local, rule-first CLI for turning a JD and trusted local resume material into a targeted Markdown resume package.

The first version is offline and deterministic. It reads source material from a configured local source root, selects evidence, marks gaps, and builds a constrained LLM prompt for later polishing.

## Commands

```bash
resume-kit --help
resume-kit doctor --json
resume-kit sources list --json
resume-kit profile show ai-agent --json
resume-kit jd analyze tests/fixtures/jd_ai_agent.md --json
resume-kit match tests/fixtures/jd_ai_agent.md --profile ai-agent --json
resume-kit resume generate tests/fixtures/jd_ai_agent.md --profile ai-agent --out output/resume.md
resume-kit resume export output/resume.md --html output/resume.html --pdf output/resume.pdf --force
resume-kit gap analyze tests/fixtures/jd_ai_agent.md --profile ai-agent --out output/gap.md
resume-kit prompt build tests/fixtures/jd_ai_agent.md --profile ai-agent --out output/llm-prompt.md
resume-kit package tests/fixtures/jd_ai_agent.md --profile ai-agent --out output/package --force
```

`resume export` removes the draft-only `需要人工复核` section before writing HTML or PDF outputs.

## JSON Contract

Successful `--json` commands return:

```json
{
  "ok": true,
  "data": {},
  "warnings": []
}
```

Errors return:

```json
{
  "ok": false,
  "error": {
    "code": "missing_source",
    "message": "Required source file does not exist",
    "detail": {}
  }
}
```

## Install

```bash
make install-local
```

This installs `resume-kit` into `~/.local/bin`.
