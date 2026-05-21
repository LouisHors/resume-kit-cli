# Resume Kit CLI 设计文档

> **Execution note:** After this design is approved, use `horspowers:writing-plans` to convert it into an implementation plan, then `horspowers:executing-plans` or `horspowers:subagent-driven-development` to build it task-by-task.

**日期**: 2026-05-21

## 目标

设计一个本地 CLI `resume-kit`，让 AI 在受控规则下基于 JD 和个人素材生成定制简历、差异分析和可追溯的 prompt/context。

## 设计背景

这个工具的核心不是“自动写简历”，而是把你已经沉淀好的事实基线、项目素材、技术文章和三份基础简历变成一个可重复调用的生成系统。

真实目标有三个：

- 遇到一个 JD 时，能快速判断匹配度
- 能生成一份可投递的 Markdown 简历草稿
- 能明确说出哪些能力是证据充分、哪些能力只是迁移、哪些能力还需要补齐

## 设计方案

### 方案 A: 纯规则引擎

只用本地 Markdown 素材和固定模板生成输出。

优点：

- 可控
- 不会乱编
- 容易测试

缺点：

- 语言不够自然
- 对不同 JD 的措辞适配较差

### 方案 B: 纯 LLM 生成

直接把 JD 和素材喂给 LLM，让模型自己产出简历与差异分析。

优点：

- 生成速度快
- 文本润色自然

缺点：

- 容易越界
- 容易把个人项目包装成工作项目
- 容易把 gap 说成能力
- 难以稳定复现

### 方案 C: 规则优先 + LLM 受控辅助

先由规则引擎完成 JD 解析、证据筛选、gap 标记和输出骨架，再把受控 prompt/context 交给 LLM 只做语言润色或版式整理。

优点：

- 事实安全
- 结果可追溯
- 方便后续继续接 LLM
- 适合本地 CLI 和 Markdown 工作流

缺点：

- 需要先写好规则和素材结构
- 第一版文本不一定最漂亮

### 最终选择

选择 **方案 C**。

这是最适合你当前阶段的方案：先把事实边界和素材选择规则固化，再让 LLM 只做辅助，不让它决定事实。

## 技术细节

### 1. 命令分层

CLI 分成五层命令：

- `doctor`：检查本地素材是否齐全
- `sources`：查看素材源状态
- `profile`：查看简历 profile
- `jd analyze`：解析 JD
- `match` / `resume generate` / `gap analyze` / `prompt build` / `package`：生成产物

### 2. 数据流

```text
JD 文本
  -> JD 解析
  -> 规则匹配 profile
  -> 从素材池抽取 evidence
  -> 生成 resume.md
  -> 生成 gap.md
  -> 生成 llm-prompt.md
  -> 输出 package
```

### 3. 约束系统

约束分三层：

1. **事实约束**  
   来自 `resume-fact-baseline.md`，约束哪些能写、哪些不能写。

2. **选择约束**  
   由 profile 和 JD 匹配规则决定哪些 evidence 可进入候选集。

3. **表达约束**  
   由 prompt/context 规定 LLM 只能润色候选内容，不得新增事实。

### 4. 证据模型

证据不按“仓库”存，而按“可用于简历表达的最小单元”存。

每条证据至少包含：

- 来源路径
- 来源章节
- 项目名
- 归属
- 披露等级
- skill tag
- resume phrase
- raw excerpt

这样做的原因是：

- 简历不是资料仓库
- 简历需要可追溯
- 一个项目常常只需要其中一两句最强证据

### 5. JD 解析模型

JD 解析只做三件事：

- 提取职责、必须项、加分项
- 识别岗位画像
- 标记风险项

不做的事：

- 不联网
- 不打分招聘方
- 不自动判断是否适合投递

### 6. LLM 使用方式

LLM 只在受控 prompt 中使用，承担以下职责：

- 润色简历表达
- 调整段落顺序
- 让 Markdown 更自然

LLM 不能承担以下职责：

- 产生新事实
- 补不存在的客户
- 补不存在的成果
- 改写事实边界

### 7. 输出内容

`package` 输出五个文件：

- `resume.md`
- `gap.md`
- `llm-prompt.md`
- `match.json`
- `evidence-map.md`

这五个文件分别承担：

- 可投递草稿
- 差异说明
- LLM 输入
- 机器可读结果
- 证据追溯

## 影响范围

这个设计会影响：

- 新仓库的目录结构
- CLI 命令体系
- 单元测试组织方式
- 文档体系
- 未来 LLM 接入方式

不会影响：

- wiki 仓库本身的资料沉淀
- 原始简历文件的内容安全边界
- 客户方案文档的隐私边界

## 实施建议

1. 先做离线 CLI 骨架和 JSON 契约。
2. 再做素材加载和 profile 规则。
3. 再做 JD 解析与 matcher。
4. 再做 resume / gap / prompt 渲染。
5. 最后再做 install、package 和 smoke test。

## 结果评估

设计完成后的判断标准是：

- 能否在不联网的情况下生成一份可追溯的简历草稿
- 能否明确指出 JD 的 gap
- 能否让 LLM 只做语言润色，不越界
- 能否让另一个 AI 只看 context + design + plan 就开始实现

## 相关文档

- [Context](../context/2026-05-21-resume-kit-ai-context.md)
- [Plan](./2026-05-21-resume-kit-cli.md)

*最后更新: 2026-05-21*
