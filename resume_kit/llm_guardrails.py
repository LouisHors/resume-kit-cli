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
