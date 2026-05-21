---
date: 2026-05-21
type: context
tags: [resume-kit, ai, cli, context, handoff]
updated: 2026-05-21
---

# Resume Kit AI Context

这是一份给未来 AI 直接开工用的上下文文档。

目标很简单：把 `resume-kit` 这个 CLI 项目迁移到新的独立仓库后，AI 只要先读本页、设计文档和实施计划，就能开始实现，不必重新翻 wiki。

---

## 1. 项目一句话

`resume-kit` 是一个本地 CLI，用规则优先、LLM 受控辅助的方式，根据 JD 和个人素材生成定制简历、JD 差异分析、证据映射和 prompt/context。

---

## 2. 为什么要做这个工具

你当前已经沉淀了足够多的三类资料：

- 事实基线：哪些能写、哪些不能写、客户怎么披露、个人/工作产出怎么分开
- 素材地图：代码仓库、客户方案、技术文章、AI 手册
- 基础简历：AI Agent、解决方案专家、iOS 三份初稿

手工改简历的痛点是：

- 每个 JD 都要重新筛材料
- 很容易把客户边界写过界
- 很容易把个人项目写得过满
- 很容易忽略 JD 的硬性短板

因此这个 CLI 的第一目标不是“会写漂亮话”，而是：

1. 快速把 JD 解析出来
2. 从本地证据池里选对材料
3. 生成一份可信、可追溯、可再编辑的简历草稿
4. 生成一份明确的差异分析

---

## 3. 绝对约束

这些规则来自 wiki 的事实基线，后续实现不得违反：

- 客户名可以公开，方案细节不公开。
- 客户项目只写“客户名 + 某场景 + 我的责任范围”。
- 工作产出和个人产出必须分开。
- 不写客户内部业务逻辑、参数细节、内部指标、上线数据、私有实现细节。
- 不生成未被本地素材支持的量化指标。
- JD 硬性要求中不匹配的内容必须写进 gap 文档，不硬塞进简历。

---

## 4. 这次要承托的三份简历

### AI Agent / AI Coding

优先项目：

- `Horspowers`
- `排障工具`
- `zegoros`
- `zego-delivery-tool-kit`
- `内容采集清洗与多平台分发 Agent 工作流`

重点表达：

- Vibe Coding
- Spec Coding
- Harness Coding
- Agent workflow
- MCP / tool calling
- Human-in-the-loop
- 多 Agent 协作

### 解决方案专家

优先项目：

- 客户方案素材
- `zego-delivery-tool-kit`
- 好未来 RTC 中台接口适配
- Yalla LiveRoom SDK 二次封装
- 字节跳动 LiveRoomWrapper iOS

重点表达：

- 客户场景交付
- Demo / Wrapper 交付
- 参数配置与方案清单
- SDK 接入与联调
- 上线保障

### iOS

优先项目：

- 好未来 RTC 中台接口适配
- Yalla LiveRoom SDK 二次封装
- 字节跳动 LiveRoomWrapper iOS
- 音频、CallKit、路由、性能分析、跨平台适配相关技术文章

重点表达：

- iOS App 开发
- Objective-C / Swift
- RTC SDK 封装
- 音频与路由
- 客户侧联调

---

## 5. 新项目的推荐结构

新仓库建议只保留下面四类内容：

```text
resume-kit/
  docs/
    context/
    plans/
  src/
  tests/
  README.md
  Makefile
```

其中：

- `docs/context/`：长期背景、口径、资料来源、边界
- `docs/plans/`：实施计划、阶段任务、验收标准
- `src/`：CLI 实现
- `tests/`：单元测试与端到端 fixture

---

## 6. 未来 AI 进入项目时的第一步

新仓库里的 AI 应该先按这个顺序读：

1. `docs/context/2026-05-21-resume-kit-ai-context.md`
2. `docs/plans/2026-05-21-resume-kit-design.md`
3. `docs/plans/2026-05-21-resume-kit-cli.md`

如果只剩一个文件，也至少要先看 context，再看 design 或 plan。

---

## 7. 关键输入文件

实现前应该先确认这些文件可读：

- `wiki/guides/resume-fact-baseline.md`
- `wiki/guides/code-project-material-map.md`
- `wiki/guides/customer-solution-material-map.md`
- `wiki/guides/technical-article-material-map.md`
- `wiki/guides/ai-agent-rag-interview-handbook.md`
- `resumes/liuhao-ai-agent.md`
- `resumes/liuhao-solution-expert.md`
- `resumes/liuhao-ios.md`

如果这些文件仍在 wiki 仓库里，新项目可以先通过相对路径引用，或者把它们同步成新仓库的只读素材。

---

## 8. AI 实现时的行为要求

- 先读文档，再写代码。
- 先做离线规则，再考虑 LLM。
- 先确保不乱编事实，再考虑语言美化。
- 先保留 Markdown 输出，再考虑别的格式。
- 先把 gap 说清楚，再考虑投递效果。

---

*最后更新: 2026-05-21*
