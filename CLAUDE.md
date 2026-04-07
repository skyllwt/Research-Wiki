# Research Wiki — Runtime Schema

> CS/AI Research Wiki. 由 Claude Code 驱动。
> 本文件是 wiki 的运行时入口，定义页面结构、链接规范、workflow 约束。

---

## 目录结构

```
wiki/
├── CLAUDE.md          ← 本文件
├── index.md           ← 内容目录（YAML）
├── log.md             ← 时序日志（append-only）
├── papers/            ← 论文结构化摘要
├── concepts/          ← 技术概念综述
├── topics/            ← 研究方向地图
├── people/            ← 研究者追踪
├── Summary/           ← 领域全景综述
└── outputs/           ← 生成物（Related Work, Idea 列表）

raw/
├── papers/            ← .tex / .pdf（只读）
├── notes/             ← .md 笔记（只读）
└── web/               ← HTML / Markdown（只读）
```

---

## 5 类页面

| 目录 | 文件名 | 职责 |
|------|--------|------|
| `papers/` | `{slug}.md` | 论文结构化摘要 |
| `concepts/` | `{concept-name}.md` | 跨论文技术概念综述 |
| `topics/` | `{topic-name}.md` | 研究方向地图 |
| `people/` | `{firstname-lastname}.md` | 研究者追踪 |
| `Summary/` | `{area-name}.md` | 领域全景综述 |

---

## 链接语法

所有内部链接使用 Obsidian wikilink：

```markdown
[[slug]]                    ← 链接到本 wiki 内任意页面
[[lora-low-rank-adaptation]] ← 链接到 papers/lora-low-rank-adaptation.md
[[flash-attention]]          ← 链接到 concepts/flash-attention.md
```

**命名规范**：全小写，连字符分隔，无空格。

---

## Cross Reference 规则

写正向链接时**必须同步写反向链接**：

| 正向操作 | 必须同步的反向操作 |
|----------|-------------------|
| papers/A 写 `Related: [[concept-B]]` | concepts/B 的 `key_papers` 追加 `A` |
| papers/A 写 `[[researcher-C]]` | people/C 的 `Key papers` 追加 `A` |
| topics/T 写 `key_people: [[person-D]]` | people/D 的 `Research areas` 追加 T |
| concepts/K 写 `key_papers: [[paper-E]]` | papers/E 的 `Related` 追加 `K` |
| concepts/K 写 part_of `[[topic-F]]` | topics/F 的概述段落追加 `K` |

---

## 页面模板

### papers/{slug}.md

```yaml
---
title: ""
slug: ""
arxiv: ""
venue: ""
year:
tags: []
importance: 3           # 1-5
date_added: YYYY-MM-DD
source_type: tex         # tex | pdf
s2_id: ""
keywords: []
domain: ""               # NLP / CV / ML Systems / Robotics
code_url: ""
cited_by: []
---
```

正文：`## Problem` / `## Key idea` / `## Method` / `## Results` / `## Limitations` / `## Open questions` / `## My take` / `## Related`

### concepts/{concept-name}.md

```yaml
---
title: ""
tags: []
maturity: active         # stable | active | emerging | deprecated
key_papers: []
first_introduced: ""
date_updated: YYYY-MM-DD
related_concepts: []
---
```

正文：`## Definition` / `## Intuition` / `## Formal notation` / `## Variants` / `## Comparison` / `## When to use` / `## Known limitations` / `## Open problems` / `## Key papers` / `## My understanding`

### topics/{topic-name}.md

```yaml
---
title: ""
tags: []
my_involvement: none     # none | reading | side-project | main-focus
sota_updated: YYYY-MM-DD
key_venues: []
related_topics: []
key_people: []
---
```

正文：`## Overview` / `## Timeline` / `## Seminal works` / `## SOTA tracker` / `## Open problems` / `## My position` / `## Research gaps` / `## Key people`

### people/{firstname-lastname}.md

```yaml
---
name: ""
affiliation: ""
tags: []
homepage: ""
scholar: ""
date_updated: YYYY-MM-DD
---
```

正文：`## Research areas` / `## Key papers` / `## Recent work` / `## Collaborators` / `## My notes`

### Summary/{area-name}.md

```yaml
---
title: ""
scope: ""
key_topics: []
paper_count:
date_updated: YYYY-MM-DD
---
```

正文：`## Overview` / `## Core areas` / `## Evolution` / `## Current frontiers` / `## Key references` / `## Related`

---

## index.md 格式

```yaml
papers:
  - slug: lora-low-rank-adaptation
    title: "LoRA: Low-Rank Adaptation of Large Language Models"
    tags: [fine-tuning, efficiency]
    importance: 5

concepts:
  - slug: parameter-efficient-fine-tuning
    tags: [fine-tuning, efficiency]
    maturity: stable

topics:
  - slug: efficient-llm-adaptation
    tags: [fine-tuning, efficiency, llm]

people:
  - slug: tri-dao
    affiliation: "Princeton / Together AI"
```

---

## log.md 格式（append-only）

```markdown
## [2026-04-07] ingest | added papers/lora-low-rank-adaptation | updated: concepts/parameter-efficient-fine-tuning
## [2026-04-07] lint | report: 0 🔴, 2 🟡, 1 🔵
## [2026-04-08] daily-arxiv | 3 papers ingested from RSS
```

---

## 约束

- **raw/ 只读**：不得修改 `raw/` 下的文件。
- **双向链接**：写正向链接时同步写反向链接。
- **tex 优先**：.tex > .pdf，fallback 链：tex 失败 → PDF 解析，PDF 失败 → vision API。
- **index.md 每次 ingest 立即更新**，log.md append-only。
- **lint 只报告不修复**：用户确认后才执行修改。
- **slug 生成规则**：论文标题关键词，连字符连接，全小写。
- **importance 评分**：1 = niche, 2 = useful, 3 = field-standard, 4 = influential, 5 = seminal。

---

## Skills

| Skill | 文件 | 触发 |
|-------|------|------|
| `/initial-wiki` | `skills/initial-wiki/SKILL.md` | 手动 |
| `/ingest` | `skills/ingest/SKILL.md` | 手动 |
| `/update` | `skills/update/SKILL.md` | 手动 |
| `/daily-arxiv` | `skills/daily-arxiv/SKILL.md` | cron 08:00 |
| `/write-related-work` | `skills/write-related-work/SKILL.md` | 手动 |
| `/idea-generation` | `skills/idea-generation/SKILL.md` | 手动 |
| `/lint` | `skills/lint/SKILL.md` | 每两周/手动 |
