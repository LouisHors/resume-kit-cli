# Resume Kit CLI 实施计划

> **Execution note:** After this plan is approved, use `horspowers:executing-plans` or `horspowers:subagent-driven-development` to implement it task-by-task in the current host.

**日期**: 2026-05-21

## 目标

实现一个本地 CLI `resume-kit`，基于 JD 和已沉淀的个人素材，生成定制简历 Markdown、JD 匹配差异文档、证据追溯文件和受规则约束的 LLM prompt/context。

## 相关文档

- Context: [2026-05-21-resume-kit-ai-context.md](../context/2026-05-21-resume-kit-ai-context.md)
- Design: [2026-05-21-resume-kit-design.md](./2026-05-21-resume-kit-design.md)

## 架构方案

第一版采用“规则优先 + LLM 辅助”的离线架构：CLI 先用确定性规则解析 JD、读取本地素材、筛选证据、生成简历骨架和差异分析，再生成一份严格约束的 LLM prompt/context 供 Codex 或其他 LLM 做语言润色。LLM 不直接决定事实，不允许新增证据外的经历、客户细节或量化指标。

CLI 放在当前 wiki 仓库的 `/Users/zego/my-code-wiki/tools/resume_kit/`，通过 `make install-local` 安装为 `~/.local/bin/resume-kit`，可从任意目录运行。

## 技术栈

- Python 3 标准库：`argparse`、`json`、`re`、`pathlib`、`dataclasses`、`unittest`
- Markdown 文本解析：第一版使用轻量 frontmatter / heading / table 解析，不引入外部依赖
- 安装方式：生成 `~/.local/bin/resume-kit` wrapper，不依赖 pip editable install
- 测试方式：`python3 -m unittest discover tools/resume_kit/tests -v`

---

## 设计约束

### 第一版范围

第一版实现这些命令：

```bash
resume-kit --help
resume-kit doctor --json
resume-kit sources list --json
resume-kit profile show ai-agent --json
resume-kit jd analyze jd.md --json
resume-kit match jd.md --profile ai-agent --json
resume-kit resume generate jd.md --profile ai-agent --out output/resume.md
resume-kit gap analyze jd.md --profile ai-agent --out output/gap.md
resume-kit prompt build jd.md --profile ai-agent --out output/llm-prompt.md
resume-kit package jd.md --profile ai-agent --out output/
```

支持的 profile：

- `ai-agent`
- `solution-expert`
- `ios`

第一版不做：

- 不自动投递简历
- 不生成 PDF / Word
- 不抓招聘网站
- 不自动深挖 GitHub / GitLab
- 不调用真实 LLM API
- 不覆盖 `resumes/` 下的三份基础简历
- 不把缺口包装成已掌握能力

### 事实与披露约束

所有生成逻辑必须遵守 `/Users/zego/my-code-wiki/wiki/guides/resume-fact-baseline.md`：

- 客户名可以公开，方案细节不公开。
- 客户项目只写“客户名 + 某场景 + 我的责任范围”。
- 工作产出和个人产出必须分开。
- 不写客户内部业务逻辑、参数细节、内部指标、上线数据、私有实现细节。
- 不生成未被本地素材支持的量化指标。
- JD 硬性要求中不匹配的内容写入 gap 文档，不硬塞进简历。

### LLM 约束策略

CLI 不让 LLM 自由发挥，而是生成受控 prompt。prompt 必须包含：

1. **任务边界**：只允许润色和重组候选素材，不允许新增事实。
2. **候选素材**：由规则引擎筛出的 evidence list。
3. **事实红线**：来自 `resume-fact-baseline.md` 的可公开 / 不应公开规则。
4. **缺口处理**：JD 要求但素材不足的能力必须进入 gap 文档，不得伪装为已具备。
5. **输出格式**：简历 Markdown、差异文档 Markdown、证据映射 JSON 的结构约束。

---

## 数据源

第一版固定读取这些文件：

```text
/Users/zego/my-code-wiki/wiki/guides/resume-fact-baseline.md
/Users/zego/my-code-wiki/wiki/guides/code-project-material-map.md
/Users/zego/my-code-wiki/wiki/guides/customer-solution-material-map.md
/Users/zego/my-code-wiki/wiki/guides/technical-article-material-map.md
/Users/zego/my-code-wiki/wiki/guides/ai-agent-rag-interview-handbook.md
/Users/zego/my-code-wiki/resumes/liuhao-ai-agent.md
/Users/zego/my-code-wiki/resumes/liuhao-solution-expert.md
/Users/zego/my-code-wiki/resumes/liuhao-ios.md
```

素材抽象为 `EvidenceItem`：

```python
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
```

JD 抽象为 `JDAnalysis`：

```python
@dataclass(frozen=True)
class JDAnalysis:
    title: str
    responsibilities: list[str]
    must_requirements: list[str]
    nice_to_have: list[str]
    keywords: list[str]
    inferred_profile: str
    risk_flags: list[str]
```

匹配结果抽象为 `MatchResult`：

```python
@dataclass(frozen=True)
class MatchResult:
    profile: str
    jd: JDAnalysis
    direct_matches: list[dict]
    transferable_matches: list[dict]
    gaps: list[dict]
    selected_evidence: list[EvidenceItem]
```

---

## 输出契约

### JSON 成功输出

所有 `--json` 成功输出使用统一 envelope：

```json
{
  "ok": true,
  "data": {},
  "warnings": []
}
```

### JSON 错误输出

所有 `--json` 错误输出使用统一 envelope：

```json
{
  "ok": false,
  "error": {
    "code": "missing_source",
    "message": "Required source file does not exist",
    "detail": {
      "path": "/Users/zego/my-code-wiki/wiki/guides/resume-fact-baseline.md"
    }
  }
}
```

### package 输出目录

`resume-kit package jd.md --profile ai-agent --out output/` 生成：

```text
output/
  resume.md
  gap.md
  llm-prompt.md
  match.json
  evidence-map.md
```

---

## Task 1: CLI 项目骨架

**Files:**

- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/__init__.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/__main__.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/cli.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/Makefile`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/README.md`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/tests/__init__.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_cli_smoke.py`

**Step 1: Write the smoke test**

Create `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_cli_smoke.py`:

```python
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


class CliSmokeTests(unittest.TestCase):
    def run_cli(self, *args):
        cmd = [
            sys.executable,
            str(ROOT / "tools" / "resume_kit" / "resume_kit" / "cli.py"),
            *args,
        ]
        return subprocess.run(cmd, text=True, capture_output=True, check=False)

    def test_help(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("resume-kit", result.stdout)
        self.assertIn("doctor", result.stdout)

    def test_json_doctor_shape(self):
        result = self.run_cli("doctor", "--json")
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertIn("data", payload)
        self.assertIn("sources", payload["data"])
```

**Step 2: Run test to verify it fails**

Run:

```bash
python3 -m unittest tools.resume_kit.tests.test_cli_smoke -v
```

Expected: FAIL because `tools/resume_kit/resume_kit/cli.py` does not exist.

**Step 3: Create minimal CLI**

Create `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/cli.py` with:

```python
#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def envelope(data, warnings=None):
    return {"ok": True, "data": data, "warnings": warnings or []}


def print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_doctor(args):
    source_paths = [
        REPO_ROOT / "wiki" / "guides" / "resume-fact-baseline.md",
        REPO_ROOT / "wiki" / "guides" / "code-project-material-map.md",
        REPO_ROOT / "wiki" / "guides" / "customer-solution-material-map.md",
        REPO_ROOT / "wiki" / "guides" / "technical-article-material-map.md",
        REPO_ROOT / "wiki" / "guides" / "ai-agent-rag-interview-handbook.md",
        REPO_ROOT / "resumes" / "liuhao-ai-agent.md",
        REPO_ROOT / "resumes" / "liuhao-solution-expert.md",
        REPO_ROOT / "resumes" / "liuhao-ios.md",
    ]
    data = {
        "repo_root": str(REPO_ROOT),
        "sources": [
            {"path": str(path), "exists": path.exists()} for path in source_paths
        ],
    }
    if args.json:
        print_json(envelope(data))
    else:
        for item in data["sources"]:
            mark = "ok" if item["exists"] else "missing"
            print(f"{mark}: {item['path']}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="resume-kit")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="verify local sources and install state")
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(func=cmd_doctor)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
```

Create `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/__main__.py`:

```python
from .cli import main

raise SystemExit(main())
```

Create empty `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/__init__.py`.

Create empty `/Users/zego/my-code-wiki/tools/resume_kit/tests/__init__.py`.

Create `/Users/zego/my-code-wiki/tools/resume_kit/Makefile`:

```makefile
PYTHON ?= python3
PREFIX ?= $(HOME)/.local/bin
REPO_ROOT := $(shell cd ../.. && pwd)

.PHONY: test install-local

test:
	$(PYTHON) -m unittest discover tests -v

install-local:
	mkdir -p "$(PREFIX)"
	printf '#!/usr/bin/env bash\nexec $(PYTHON) "$(REPO_ROOT)/tools/resume_kit/resume_kit/cli.py" "$$@"\n' > "$(PREFIX)/resume-kit"
	chmod +x "$(PREFIX)/resume-kit"
	@echo "Installed $(PREFIX)/resume-kit"
```

Create `/Users/zego/my-code-wiki/tools/resume_kit/README.md` with command list, JSON envelope policy, install command, and source paths.

**Step 4: Run test to verify it passes**

Run:

```bash
python3 -m unittest tools.resume_kit.tests.test_cli_smoke -v
```

Expected: PASS.

**Step 5: Commit**

```bash
git add tools/resume_kit
git commit -m "feat: scaffold resume-kit cli"
```

---

## Task 2: 统一路径、错误和 JSON 输出

**Files:**

- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/paths.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/jsonio.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/errors.py`
- Modify: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/cli.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_jsonio.py`

**Step 1: Write the failing tests**

Create `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_jsonio.py`:

```python
import json
import unittest

from resume_kit.jsonio import error_envelope, success_envelope


class JsonEnvelopeTests(unittest.TestCase):
    def test_success_envelope(self):
        payload = success_envelope({"value": 1})
        self.assertEqual(payload["ok"], True)
        self.assertEqual(payload["data"]["value"], 1)
        self.assertEqual(payload["warnings"], [])

    def test_error_envelope_has_code_message_and_detail(self):
        payload = error_envelope("missing_source", "Missing source", {"path": "x"})
        self.assertEqual(payload["ok"], False)
        self.assertEqual(payload["error"]["code"], "missing_source")
        self.assertEqual(payload["error"]["message"], "Missing source")
        self.assertEqual(payload["error"]["detail"]["path"], "x")
        json.dumps(payload, ensure_ascii=False)
```

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest tests.test_jsonio -v
```

Expected: FAIL because `resume_kit.jsonio` does not exist.

**Step 3: Implement support modules**

Create `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/jsonio.py`:

```python
import json
import sys


def success_envelope(data, warnings=None):
    return {"ok": True, "data": data, "warnings": warnings or []}


def error_envelope(code, message, detail=None):
    return {
        "ok": False,
        "error": {
            "code": code,
            "message": message,
            "detail": detail or {},
        },
    }


def emit_json(payload, stream=None):
    target = stream or sys.stdout
    target.write(json.dumps(payload, ensure_ascii=False, indent=2))
    target.write("\n")
```

Create `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/errors.py`:

```python
class ResumeKitError(Exception):
    code = "resume_kit_error"

    def __init__(self, message, detail=None):
        super().__init__(message)
        self.message = message
        self.detail = detail or {}


class MissingSourceError(ResumeKitError):
    code = "missing_source"
```

Create `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/paths.py`:

```python
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]

SOURCE_PATHS = {
    "fact_baseline": REPO_ROOT / "wiki/guides/resume-fact-baseline.md",
    "code_projects": REPO_ROOT / "wiki/guides/code-project-material-map.md",
    "customer_solutions": REPO_ROOT / "wiki/guides/customer-solution-material-map.md",
    "technical_articles": REPO_ROOT / "wiki/guides/technical-article-material-map.md",
    "ai_handbook": REPO_ROOT / "wiki/guides/ai-agent-rag-interview-handbook.md",
    "resume_ai_agent": REPO_ROOT / "resumes/liuhao-ai-agent.md",
    "resume_solution_expert": REPO_ROOT / "resumes/liuhao-solution-expert.md",
    "resume_ios": REPO_ROOT / "resumes/liuhao-ios.md",
}
```

Modify `cli.py` to import `SOURCE_PATHS`, `success_envelope`, `emit_json`, `ResumeKitError`, and `error_envelope`. Wrap `main()` in a try/except so `--json` commands return the error envelope and plain commands print a concise error to stderr.

**Step 4: Run tests**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest discover tests -v
```

Expected: PASS.

**Step 5: Commit**

```bash
git add tools/resume_kit
git commit -m "feat: add resume-kit json and path helpers"
```

---

## Task 3: Markdown 与素材加载

**Files:**

- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/markdown.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/models.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/corpus.py`
- Modify: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/cli.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_markdown.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_corpus.py`

**Step 1: Write markdown parser tests**

Create `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_markdown.py`:

```python
import unittest

from resume_kit.markdown import extract_headings, strip_frontmatter


class MarkdownTests(unittest.TestCase):
    def test_strip_frontmatter(self):
        body = strip_frontmatter("---\na: b\n---\n# Title\nBody")
        self.assertEqual(body.strip(), "# Title\nBody")

    def test_extract_headings(self):
        headings = extract_headings("# A\ntext\n## B\nb\n### C\nc")
        self.assertEqual([h["title"] for h in headings], ["A", "B", "C"])
        self.assertEqual(headings[1]["level"], 2)
        self.assertIn("b", headings[1]["body"])
```

**Step 2: Write corpus tests**

Create `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_corpus.py`:

```python
import unittest

from resume_kit.corpus import load_corpus


class CorpusTests(unittest.TestCase):
    def test_load_corpus_has_required_sources(self):
        corpus = load_corpus()
        keys = {source.key for source in corpus.sources}
        self.assertIn("fact_baseline", keys)
        self.assertIn("resume_ai_agent", keys)

    def test_extract_evidence_contains_agent_project(self):
        corpus = load_corpus()
        ids = {item.id for item in corpus.evidence}
        self.assertIn("personal-content-distribution-agent", ids)
```

**Step 3: Run tests to verify failure**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest tests.test_markdown tests.test_corpus -v
```

Expected: FAIL because modules do not exist.

**Step 4: Implement data models**

Create `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/models.py`:

```python
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
```

**Step 5: Implement markdown helpers**

Create `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/markdown.py`:

```python
import re


def strip_frontmatter(text):
    if not text.startswith("---"):
        return text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return text
    return parts[2].lstrip()


def extract_headings(text):
    lines = text.splitlines()
    headings = []
    current = None
    body = []
    for line in lines:
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            if current is not None:
                current["body"] = "\n".join(body).strip()
                headings.append(current)
            current = {"level": len(match.group(1)), "title": match.group(2).strip(), "body": ""}
            body = []
        else:
            body.append(line)
    if current is not None:
        current["body"] = "\n".join(body).strip()
        headings.append(current)
    return headings
```

**Step 6: Implement corpus loader**

Create `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/corpus.py`:

```python
from .models import Corpus, EvidenceItem, SourceDoc
from .paths import SOURCE_PATHS


def _read_source(key, path):
    return SourceDoc(key=key, path=str(path), text=path.read_text(encoding="utf-8"))


def load_corpus():
    sources = [_read_source(key, path) for key, path in SOURCE_PATHS.items()]
    source_by_key = {source.key: source for source in sources}
    evidence = []
    fact_text = source_by_key["fact_baseline"].text

    evidence.append(EvidenceItem(
        id="personal-content-distribution-agent",
        source_path=source_by_key["fact_baseline"].path,
        source_section="3.2 个人产出",
        profile_tags=["ai-agent"],
        skill_tags=[
            "agent-workflow",
            "mcp",
            "human-in-the-loop",
            "multi-agent",
            "content-pipeline",
            "sqlite",
            "cron",
        ],
        project_name="内容采集清洗与多平台分发 Agent 工作流",
        ownership="personal",
        disclosure_level="public-personal",
        summary="从 OpenClaw 技能演进到多 Agent 内容生产线，覆盖小红书和微信公众号自动化。",
        resume_phrasing=[
            "设计并实践信息抓取、内容清洗与多平台分发 Agent 工作流，串联 RSS / GitHub Trending、LLM 清洗、SQLite / Markdown / Obsidian 状态沉淀、Slack 人工审核，以及小红书 MCP / 微信公众号草稿箱发布链路。",
            "试运营一个月内单篇内容最高浏览量 14w+，多篇内容浏览量 3w+ / 4w+。",
        ],
        raw_excerpt=_excerpt(fact_text, "内容采集清洗与多平台分发 Agent 工作流"),
    ))

    return Corpus(sources=sources, evidence=evidence)


def _excerpt(text, needle, radius=500):
    index = text.find(needle)
    if index < 0:
        return ""
    start = max(0, index - radius)
    end = min(len(text), index + len(needle) + radius)
    return text[start:end].strip()
```

**Step 7: Add `sources list` command**

Modify `cli.py`:

- Add `sources` subparser with `list`.
- `resume-kit sources list --json` returns all source keys, paths, and existence state.

**Step 8: Run tests**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest discover tests -v
```

Expected: PASS.

**Step 9: Commit**

```bash
git add tools/resume_kit
git commit -m "feat: load resume evidence corpus"
```

---

## Task 4: Profile 与素材优先级规则

**Files:**

- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/profiles.py`
- Modify: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/cli.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_profiles.py`

**Step 1: Write failing tests**

Create `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_profiles.py`:

```python
import unittest

from resume_kit.profiles import get_profile, list_profiles


class ProfileTests(unittest.TestCase):
    def test_profiles_exist(self):
        names = [profile.name for profile in list_profiles()]
        self.assertEqual(names, ["ai-agent", "solution-expert", "ios"])

    def test_ai_agent_prioritizes_agent_materials(self):
        profile = get_profile("ai-agent")
        self.assertIn("agent-workflow", profile.priority_skill_tags)
        self.assertIn("Horspowers", profile.preferred_projects)
        self.assertIn("内容采集清洗与多平台分发 Agent 工作流", profile.preferred_projects)
```

**Step 2: Run tests to verify failure**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest tests.test_profiles -v
```

Expected: FAIL because `profiles.py` does not exist.

**Step 3: Implement profiles**

Create `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/profiles.py`:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    name: str
    display_name: str
    base_resume_key: str
    priority_skill_tags: list[str]
    preferred_projects: list[str]
    forbidden_styles: list[str]


PROFILES = {
    "ai-agent": Profile(
        name="ai-agent",
        display_name="AI Agent / AI Coding",
        base_resume_key="resume_ai_agent",
        priority_skill_tags=[
            "agent-workflow",
            "mcp",
            "rag",
            "tool-calling",
            "spec-coding",
            "harness-coding",
            "human-in-the-loop",
            "multi-agent",
        ],
        preferred_projects=[
            "Horspowers",
            "排障工具",
            "zegoros",
            "zego-delivery-tool-kit",
            "内容采集清洗与多平台分发 Agent 工作流",
            "Amazon 选品工具",
        ],
        forbidden_styles=["包装个人项目为公司项目", "虚构 Go 熟练经验"],
    ),
    "solution-expert": Profile(
        name="solution-expert",
        display_name="解决方案专家",
        base_resume_key="resume_solution_expert",
        priority_skill_tags=["rtc", "solution", "delivery", "customer", "troubleshooting"],
        preferred_projects=[
            "客户方案素材",
            "zego-delivery-tool-kit",
            "好未来 RTC 中台接口适配",
            "Yalla LiveRoom SDK 二次封装",
            "字节跳动 LiveRoomWrapper iOS",
        ],
        forbidden_styles=["披露方案细节", "披露客户内部参数"],
    ),
    "ios": Profile(
        name="ios",
        display_name="iOS 开发",
        base_resume_key="resume_ios",
        priority_skill_tags=["ios", "objective-c", "swift", "rtc", "audio", "sdk"],
        preferred_projects=[
            "好未来 RTC 中台接口适配",
            "Yalla LiveRoom SDK 二次封装",
            "字节跳动 LiveRoomWrapper iOS",
            "CallKit",
            "AVAudioSession",
        ],
        forbidden_styles=["把方案专家经历写成纯 App 开发"],
    ),
}


def list_profiles():
    return [PROFILES[name] for name in ["ai-agent", "solution-expert", "ios"]]


def get_profile(name):
    try:
        return PROFILES[name]
    except KeyError as exc:
        raise ValueError(f"Unknown profile: {name}") from exc
```

**Step 4: Add `profile show` command**

Modify `cli.py`:

- Add `profile show <name> --json`.
- Return profile fields.
- Plain output prints display name, base resume, preferred projects.

**Step 5: Run tests**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest discover tests -v
```

Expected: PASS.

**Step 6: Commit**

```bash
git add tools/resume_kit
git commit -m "feat: add resume-kit profiles"
```

---

## Task 5: JD 解析器

**Files:**

- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/jd.py`
- Modify: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/models.py`
- Modify: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/cli.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/tests/fixtures/jd_ai_agent.md`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_jd.py`

**Step 1: Create fixture**

Create `/Users/zego/my-code-wiki/tools/resume_kit/tests/fixtures/jd_ai_agent.md`:

```markdown
# AI Agent 开发工程师

岗位职责
1. 负责 NAS 智能 Agent 系统的设计、开发与优化
2. 负责 Agent 的部署、调优、评测与问题排查
3. 负责提示词工程、工具调用流程、交互流程与 Agent 技能设计
4. 负责 RAG / Agentic RAG 及知识库接入与优化

岗位要求
必须：
1. 具备一年及以上大语言模型应用开发经验，有实际的 AI Agent 或 RAG 项目实践经验
2. 掌握 AI Agent 开发、RAG 优化、MCP 及工具开发等技术原理及落地经验
3. 熟练掌握 Go 语言，能熟练使用主流 AI coding 工具

加分项：
1. 有向量检索、全文搜索、RAG Pipeline 的实战经验
2. 有 Agent 编排模式设计经验，包括多 Agent 协作、任务动态分解与调度
```

**Step 2: Write failing tests**

Create `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_jd.py`:

```python
import unittest
from pathlib import Path

from resume_kit.jd import analyze_jd


FIXTURE = Path(__file__).parent / "fixtures" / "jd_ai_agent.md"


class JDTests(unittest.TestCase):
    def test_analyze_jd_extracts_sections(self):
        analysis = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(analysis.title, "AI Agent 开发工程师")
        self.assertTrue(any("NAS 智能 Agent" in item for item in analysis.responsibilities))
        self.assertTrue(any("Go 语言" in item for item in analysis.must_requirements))
        self.assertTrue(any("向量检索" in item for item in analysis.nice_to_have))

    def test_analyze_jd_infers_ai_profile_and_risk_flags(self):
        analysis = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(analysis.inferred_profile, "ai-agent")
        self.assertIn("go-language-hard-requirement", analysis.risk_flags)
        self.assertIn("nas-domain-gap", analysis.risk_flags)
```

**Step 3: Run tests to verify failure**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest tests.test_jd -v
```

Expected: FAIL because `jd.py` does not exist.

**Step 4: Add `JDAnalysis` model**

Modify `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/models.py`:

```python
@dataclass(frozen=True)
class JDAnalysis:
    title: str
    responsibilities: list[str]
    must_requirements: list[str]
    nice_to_have: list[str]
    keywords: list[str]
    inferred_profile: str
    risk_flags: list[str]
```

**Step 5: Implement parser**

Create `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/jd.py`:

```python
import re

from .models import JDAnalysis


KEYWORDS = [
    "AI Agent", "Agent", "RAG", "Agentic RAG", "MCP", "工具调用",
    "Go", "AI coding", "NAS", "向量检索", "全文搜索", "iOS",
    "RTC", "SDK", "解决方案", "客户", "交付",
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
    inferred = _infer_profile(text)
    risks = _risk_flags(text)
    return JDAnalysis(
        title=title,
        responsibilities=responsibilities,
        must_requirements=must,
        nice_to_have=nice,
        keywords=keywords,
        inferred_profile=inferred,
        risk_flags=risks,
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
        if any(header in stripped for header in headers):
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
```

**Step 6: Add `jd analyze` command**

Modify `cli.py`:

- Add `jd analyze <path> --json`.
- Plain output prints title, inferred profile, keywords, risk flags.

**Step 7: Run tests**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest discover tests -v
```

Expected: PASS.

**Step 8: Commit**

```bash
git add tools/resume_kit
git commit -m "feat: analyze job descriptions"
```

---

## Task 6: 规则匹配引擎

**Files:**

- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/matcher.py`
- Modify: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/models.py`
- Modify: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/cli.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_matcher.py`

**Step 1: Write failing tests**

Create `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_matcher.py`:

```python
import unittest
from pathlib import Path

from resume_kit.corpus import load_corpus
from resume_kit.jd import analyze_jd
from resume_kit.matcher import match_jd
from resume_kit.profiles import get_profile


FIXTURE = Path(__file__).parent / "fixtures" / "jd_ai_agent.md"


class MatcherTests(unittest.TestCase):
    def test_match_ai_agent_jd_selects_personal_agent_evidence(self):
        jd = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        result = match_jd(jd, get_profile("ai-agent"), load_corpus())
        ids = {item.id for item in result.selected_evidence}
        self.assertIn("personal-content-distribution-agent", ids)

    def test_go_requirement_is_gap_not_direct_match(self):
        jd = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        result = match_jd(jd, get_profile("ai-agent"), load_corpus())
        self.assertTrue(any(gap["id"] == "go-language-hard-requirement" for gap in result.gaps))
```

**Step 2: Run tests to verify failure**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest tests.test_matcher -v
```

Expected: FAIL because `matcher.py` does not exist.

**Step 3: Add `MatchResult` model**

Modify `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/models.py`:

```python
@dataclass(frozen=True)
class MatchResult:
    profile: str
    jd: JDAnalysis
    direct_matches: list[dict]
    transferable_matches: list[dict]
    gaps: list[dict]
    selected_evidence: list[EvidenceItem]
```

**Step 4: Implement matcher**

Create `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/matcher.py`:

```python
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
    text = " ".join(jd.keywords + jd.responsibilities + jd.must_requirements + jd.nice_to_have).lower()
    for tag in item.skill_tags:
        if tag.replace("-", " ") in text or tag in text:
            score += 1
    if item.project_name in profile.preferred_projects:
        score += 2
    return score
```

**Step 5: Add `match` command**

Modify `cli.py`:

- Add `match <jd_path> --profile <name> --json`.
- Serialize `MatchResult` with `dataclasses.asdict`.

**Step 6: Run tests**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest discover tests -v
```

Expected: PASS.

**Step 7: Commit**

```bash
git add tools/resume_kit
git commit -m "feat: match jd against resume evidence"
```

---

## Task 7: 简历与差异文档渲染

**Files:**

- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/renderers.py`
- Modify: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/cli.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_renderers.py`

**Step 1: Write failing tests**

Create `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_renderers.py`:

```python
import unittest
from pathlib import Path

from resume_kit.corpus import load_corpus
from resume_kit.jd import analyze_jd
from resume_kit.matcher import match_jd
from resume_kit.profiles import get_profile
from resume_kit.renderers import render_gap, render_resume


FIXTURE = Path(__file__).parent / "fixtures" / "jd_ai_agent.md"


class RendererTests(unittest.TestCase):
    def match_result(self):
        jd = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        return match_jd(jd, get_profile("ai-agent"), load_corpus())

    def test_render_resume_contains_selected_project(self):
        text = render_resume(self.match_result())
        self.assertIn("内容采集清洗与多平台分发 Agent 工作流", text)
        self.assertIn("14w+", text)

    def test_render_gap_contains_go_gap(self):
        text = render_gap(self.match_result())
        self.assertIn("Go", text)
        self.assertIn("gap", text.lower())
```

**Step 2: Run tests to verify failure**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest tests.test_renderers -v
```

Expected: FAIL because `renderers.py` does not exist.

**Step 3: Implement renderers**

Create `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/renderers.py`:

```python
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
        lines.append(f"- 披露等级：{item.disclosure_level}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
```

**Step 4: Add output commands**

Modify `cli.py`:

- Add `resume generate <jd_path> --profile <name> --out <path>`.
- Add `gap analyze <jd_path> --profile <name> --out <path>`.
- Ensure parent output directory is created.
- Refuse to overwrite existing files unless `--force` is provided.

**Step 5: Run tests**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest discover tests -v
```

Expected: PASS.

**Step 6: Commit**

```bash
git add tools/resume_kit
git commit -m "feat: render targeted resume and gap report"
```

---

## Task 8: LLM prompt/context 生成

**Files:**

- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/llm_guardrails.py`
- Modify: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/renderers.py`
- Modify: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/cli.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_llm_guardrails.py`

**Step 1: Write failing test**

Create `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_llm_guardrails.py`:

```python
import unittest
from pathlib import Path

from resume_kit.corpus import load_corpus
from resume_kit.jd import analyze_jd
from resume_kit.llm_guardrails import build_llm_prompt
from resume_kit.matcher import match_jd
from resume_kit.profiles import get_profile


FIXTURE = Path(__file__).parent / "fixtures" / "jd_ai_agent.md"


class LLMGuardrailTests(unittest.TestCase):
    def test_prompt_contains_guardrails_and_evidence(self):
        jd = analyze_jd(FIXTURE.read_text(encoding="utf-8"))
        result = match_jd(jd, get_profile("ai-agent"), load_corpus())
        prompt = build_llm_prompt(result)
        self.assertIn("不得新增事实", prompt)
        self.assertIn("客户项目只写客户名 + 场景 + 责任范围", prompt)
        self.assertIn("内容采集清洗与多平台分发 Agent 工作流", prompt)
        self.assertIn("Go", prompt)
        self.assertIn("gap", prompt.lower())
```

**Step 2: Run test to verify failure**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest tests.test_llm_guardrails -v
```

Expected: FAIL because `llm_guardrails.py` does not exist.

**Step 3: Implement prompt builder**

Create `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/llm_guardrails.py`:

```python
import json
from dataclasses import asdict


def build_llm_prompt(result):
    evidence_payload = [asdict(item) for item in result.selected_evidence]
    gap_payload = result.gaps
    return f"""# 受约束简历生成任务

你是简历改写助手，只能基于下方证据和规则生成内容。

## 不可违反的规则

- 不得新增事实、项目、客户、数据或指标。
- 不得把个人项目包装成公司项目。
- 不得把 gap 写成已掌握能力。
- 客户项目只写客户名 + 场景 + 责任范围。
- 不得公开客户内部业务逻辑、参数细节、内部指标、上线数据、私有实现细节。
- 如果 JD 要求与证据不足，必须写入差异分析，不得硬塞进简历。

## JD 信息

标题：{result.jd.title}

职责：
{_bullets(result.jd.responsibilities)}

必须要求：
{_bullets(result.jd.must_requirements)}

加分项：
{_bullets(result.jd.nice_to_have)}

## 已筛选证据

```json
{json.dumps(evidence_payload, ensure_ascii=False, indent=2)}
```

## Gap / 风险点

```json
{json.dumps(gap_payload, ensure_ascii=False, indent=2)}
```

## 输出要求

请输出两个 Markdown 文档：

1. `resume.md`：面向该 JD 的定制简历草稿。
2. `gap.md`：JD 匹配差异分析，包含已匹配、可迁移、短板、补齐建议。
"""


def _bullets(items):
    if not items:
        return "- 无"
    return "\n".join(f"- {item}" for item in items)
```

**Step 4: Add `prompt build` command**

Modify `cli.py`:

- Add `prompt build <jd_path> --profile <name> --out <path>`.
- Output prompt markdown only.

**Step 5: Run tests**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest discover tests -v
```

Expected: PASS.

**Step 6: Commit**

```bash
git add tools/resume_kit
git commit -m "feat: build constrained resume llm prompt"
```

---

## Task 9: 一键 package 输出

**Files:**

- Create: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/package.py`
- Modify: `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/cli.py`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_package.py`

**Step 1: Write failing test**

Create `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_package.py`:

```python
import tempfile
import unittest
from pathlib import Path

from resume_kit.package import create_package


FIXTURE = Path(__file__).parent / "fixtures" / "jd_ai_agent.md"


class PackageTests(unittest.TestCase):
    def test_create_package_outputs_expected_files(self):
        with tempfile.TemporaryDirectory() as tempdir:
            paths = create_package(FIXTURE, "ai-agent", Path(tempdir), force=False)
            names = {path.name for path in paths}
            self.assertEqual(names, {
                "resume.md",
                "gap.md",
                "llm-prompt.md",
                "match.json",
                "evidence-map.md",
            })
            self.assertIn("14w+", (Path(tempdir) / "resume.md").read_text(encoding="utf-8"))
```

**Step 2: Run test to verify failure**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest tests.test_package -v
```

Expected: FAIL because `package.py` does not exist.

**Step 3: Implement package generator**

Create `/Users/zego/my-code-wiki/tools/resume_kit/resume_kit/package.py`:

```python
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
```

**Step 4: Add `package` command**

Modify `cli.py`:

- Add `package <jd_path> --profile <name> --out <dir> [--force]`.
- Plain output prints generated file paths.
- JSON output returns generated file paths.

**Step 5: Run tests**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest discover tests -v
```

Expected: PASS.

**Step 6: Commit**

```bash
git add tools/resume_kit
git commit -m "feat: package resume outputs for jd"
```

---

## Task 10: 安装与跨目录 smoke test

**Files:**

- Modify: `/Users/zego/my-code-wiki/tools/resume_kit/README.md`
- Modify: `/Users/zego/my-code-wiki/tools/resume_kit/Makefile`
- Create: `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_install_contract.py`

**Step 1: Add install contract test**

Create `/Users/zego/my-code-wiki/tools/resume_kit/tests/test_install_contract.py`:

```python
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


class InstallContractTests(unittest.TestCase):
    def test_makefile_exists(self):
        self.assertTrue(Path("Makefile").exists())

    def test_readme_documents_package_command(self):
        text = Path("README.md").read_text(encoding="utf-8")
        self.assertIn("resume-kit package", text)
        self.assertIn("resume-kit doctor --json", text)
```

**Step 2: Run tests**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest discover tests -v
```

Expected: PASS.

**Step 3: Install locally**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
make install-local
```

Expected: prints `Installed /Users/zego/.local/bin/resume-kit`.

**Step 4: Smoke test from another directory**

Run:

```bash
cd /tmp
command -v resume-kit
resume-kit --help
resume-kit doctor --json
```

Expected:

- `command -v resume-kit` prints `/Users/zego/.local/bin/resume-kit`
- `resume-kit --help` includes `doctor`, `jd`, `match`, `resume`, `gap`, `prompt`, `package`
- `resume-kit doctor --json` returns `"ok": true` and all source files exist

**Step 5: Commit**

```bash
git add tools/resume_kit
git commit -m "docs: document resume-kit install and usage"
```

---

## Task 11: 端到端验收

**Files:**

- No new files required
- Generated output path for manual verification: `/Users/zego/my-code-wiki/output/resume-kit-fixture/`
- Sync target: `/Users/zego/Documents/Document/docs/plans/2026-05-21-resume-kit-cli.md`

**Step 1: Run all tests**

Run:

```bash
cd /Users/zego/my-code-wiki/tools/resume_kit
PYTHONPATH=. python3 -m unittest discover tests -v
```

Expected: all tests PASS.

**Step 2: Run package against fixture JD**

Run:

```bash
cd /Users/zego/my-code-wiki
resume-kit package tools/resume_kit/tests/fixtures/jd_ai_agent.md --profile ai-agent --out output/resume-kit-fixture --force
```

Expected generated files:

```text
/Users/zego/my-code-wiki/output/resume-kit-fixture/resume.md
/Users/zego/my-code-wiki/output/resume-kit-fixture/gap.md
/Users/zego/my-code-wiki/output/resume-kit-fixture/llm-prompt.md
/Users/zego/my-code-wiki/output/resume-kit-fixture/match.json
/Users/zego/my-code-wiki/output/resume-kit-fixture/evidence-map.md
```

**Step 3: Verify policy-sensitive content**

Run:

```bash
rg -n "14w\\+|3w\\+|4w\\+|Go|NAS|不得新增事实|客户项目只写客户名" output/resume-kit-fixture
```

Expected:

- `resume.md` includes `14w+` only through the content distribution Agent evidence.
- `gap.md` includes Go and NAS as gap / transferable risk, not direct mastery.
- `llm-prompt.md` includes `不得新增事实` and `客户项目只写客户名 + 场景 + 责任范围`.

**Step 4: Verify no source overwrite**

Run:

```bash
git diff -- resumes wiki/guides
```

Expected: no diff caused by `resume-kit package`.

**Step 5: Commit final implementation state**

```bash
git add tools/resume_kit output/resume-kit-fixture
git commit -m "test: add resume-kit end-to-end fixture"
```

**Step 6: Sync plan and README to Documents**

Run:

```bash
mkdir -p /Users/zego/Documents/Document/docs/plans
cp /Users/zego/my-code-wiki/docs/plans/2026-05-21-resume-kit-cli.md /Users/zego/Documents/Document/docs/plans/2026-05-21-resume-kit-cli.md
```

Expected: the implementation plan is available from the iCloud-synced Documents mirror.

---

## 后续增强，不进入第一版

- 接入 GitHub / GitLab 深挖，补充 EvidenceItem 自动生成。
- 把素材库从 Markdown 解析升级为 YAML/JSON index。
- 接入可配置 LLM provider，但必须保留当前 prompt guardrail。
- 增加 `.docx` / PDF 导出。
- 增加 Web UI。
- 增加招聘网站 JD URL 抓取。

---

## 计划自审

### Completeness

所有第一版命令、文件路径、测试命令、安装命令、输出契约和验收条件均已定义。

### Scope Control

第一版只实现本地 CLI、规则匹配、Markdown 输出和 prompt 生成，不做网络抓取、LLM API、PDF/Word、自动投递或 GitHub/GitLab 深挖。

### Executability

每个任务都包含明确文件路径、测试步骤、最小实现方向、验证命令和提交点。

### Risk Notes

- 第一版的 Markdown 解析是轻量规则，不追求完整 Markdown AST。
- 第一版 EvidenceItem 先手写关键证据，后续再做自动抽取。
- LLM 只作为后续润色环节的受控输入，不作为事实来源。
