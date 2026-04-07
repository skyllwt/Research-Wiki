---
name: ingest
description: 消化一篇论文，创建 wiki 页面并建立所有交叉引用
argument-hint: [path-or-url]
---

# /ingest

> 消化一篇论文，完整纳入 wiki，建立所有交叉引用。

## 触发

用户手动：`/ingest <本地路径或 arXiv URL>`

## 输入

- `source`：本地 .tex / .pdf 路径，或 arXiv URL（如 `https://arxiv.org/abs/2106.09685`）

## 输出

- `wiki/papers/{slug}.md` — 论文页面
- 更新的交叉引用页面（concepts、topics、people）
- 更新的 `index.md` 和 `log.md`

## 步骤

### STEP 1: 解析来源

**先确认工作目录**：`cd` 到 wiki 项目根目录（包含 `wiki/`、`raw/`、`scripts/` 的目录），所有后续路径都相对于此目录。

1. 检测 source 类型：
   - **arXiv URL**：
     - 尝试获取 tex source（从 ar5iv `https://ar5iv.labs.arxiv.org/html/{id}` 或直接下载 .tex）
     - 若失败：下载 PDF
   - **本地 .tex 文件**：直接读取
   - **本地 .pdf 文件**：PyMuPDF 提取文本
   - **解析失败**：尝试 fallback 策略
2. 提取：标题、摘要、作者、机构、发表日期
3. 提取参考文献列表

### STEP 2: 预处理（实体标注）

1. **提取关键词**：从标题和摘要中抽取 3-8 个核心关键词
2. **标注领域**：判断所属研究领域（NLP / CV / ML Systems / Robotics 等）
3. **标注影响力**：通过 Semantic Scholar 查询引用量
   - 运行 `python scripts/fetch_s2.py paper {arxiv_id}`
   - 引用量 + 顶会身份 + 研究相关性 → importance 评分（1-5）
4. **图表处理**：
   - 提取 figure/table captions
   - 关键图表送 vision API 解读，生成描述摘要
5. **Appendix 摘要**（非全文提取，避免上下文膨胀）

### STEP 3: 生成 papers 页面

1. 按 paper 模板填写所有必填字段
2. slug 生成规则：论文标题关键词，连字符连接，全小写
3. `CREATE wiki/papers/{slug}.md`

### STEP 4: 处理交叉引用（核心步骤）

**Part A — Wiki 内部匹配：**

1. 读取 `wiki/index.md`，提取所有 tags
2. 找出与本文 tags 重叠的已有页面
3. 对每个重叠 concept：
   - 若本文是该概念的核心论文：追加 `[[slug]]` 到 `key_papers`
   - 若本文引入新变体：在 Variants 段落追加
   - 若有矛盾：写 contradiction note
4. 对每个重叠 topic：追加到 `seminal_works` 或 `recent_work`
5. 若新概念首次出现：`CREATE wiki/concepts/{concept}.md`

**Part B — Semantic Scholar 外部引用：**

1. 运行 `python scripts/fetch_s2.py citations {arxiv_id}`
2. 运行 `python scripts/fetch_s2.py references {arxiv_id}`
3. 对 citations 中已在 wiki 中的论文：自动回填 `cited_by`
4. 对 references 中高引但 wiki 中未收录的：建议用户后续 ingest

### STEP 5: 处理作者

1. 提取第一作者和通讯作者
2. 若 `people/{author}.md` 存在：追加本文到 `Key papers`
3. 若不存在且作者 importance >= 4：`CREATE wiki/people/{author}.md`

### STEP 6: 更新导航

1. `EDIT wiki/index.md`：在对应 topic 分类下追加条目
2. `APPEND wiki/log.md`：`## [{date}] ingest | {title}`

### STEP 7: 报告给用户

- 列出：创建的页面、更新的页面
- 列出：发现的矛盾点（若有）
- 列出：S2 发现的高引未收录论文

## 约束

- `raw/` 只读
- 所有链接使用 `[[slug]]` wikilink 格式
- 写正向链接时同步写反向链接
- tex 优先：.tex > .pdf > fallback
- `index.md` 立即更新，`log.md` append-only
