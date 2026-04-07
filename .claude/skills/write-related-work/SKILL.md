---
name: write-related-work
description: 基于 wiki 已有知识生成可直接用于论文的 Related Work 段落
---

# /write-related-work

> 基于 wiki 已有知识，生成可直接用于论文的 Related Work 段落。

## 触发

用户手动：`/write-related-work`（可无参数或有用户输入）

## 输入

- `research_question`：研究问题或关键词（可选，无参数时基于全 wiki 生成）

## 输出

- `wiki/outputs/related-work-{topic}-{date}.md` — Related Work 段落

## 步骤

### STEP 1: 定位相关知识

1. 读取 `wiki/index.md`
2. 根据 `research_question` 匹配相关 topics 和 tags
3. 生成候选页面列表，按 importance 降序排列

### STEP 2: 精读相关页面

1. 精读候选 papers：重点读 Problem、Key idea、Results、My take
2. 精读相关 concepts：重点读 Definition、Variants、Comparison
3. 精读相关 topics：重点读 Timeline、Open problems

### STEP 3: 构建论述结构

1. 将论文分组：背景工作 / 直接相关工作 / 对比方法
2. 确定叙述顺序：
   - 按时间线（从早期到最新）
   - 或从宏观到具体（大方向 → 子方向 → 具体方法）

### STEP 4: 生成段落

1. 输出格式：学术论文风格（中文或英文，取决于用户要求）
2. 每个引用使用 `[[slug]]` 格式（方便后续替换为 `\cite{}`）
3. 段落结构：
   - 开头：该方向的大背景和重要性
   - 中间：按分组展开，每组 1-2 段
   - 结尾：与本文工作的定位关系

### STEP 5: 归档

1. `CREATE wiki/outputs/related-work-{topic}-{date}.md`
2. `APPEND wiki/log.md`：`## [{date}] write-related-work | {topic}`

## 约束

- 只引用 wiki 中已有的论文，不凭空编造引用
- 引用格式统一使用 `[[slug]]`
- 如果 wiki 中相关论文不足 3 篇，提示用户先 ingest 更多论文
- 输出归档到 `outputs/`，不直接修改 wiki 页面
