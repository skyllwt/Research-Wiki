---
name: initial-wiki
description: 从 raw/ 目录搭建完整的 Research Wiki，包括论文、概念、方向、人物页面
argument-hint: [topic]
---

# /initial-wiki

> 从零搭建一个 Research Wiki。

## 触发

用户手动运行 `/initial-wiki`，或在 `raw/papers/` 放好文件后输入 topic。

## 输入

- `topic`：研究方向关键词（如 "efficient fine-tuning for LLMs"）
- `raw/papers/` 中的 .tex / .pdf 文件
- 可选：`raw/notes/`、`raw/web/` 中的笔记和网页

## 输出

完整的 wiki 骨架：`wiki/CLAUDE.md`、`index.md`、`log.md`，以及 papers、concepts、topics、people、Summary 目录下的页面。

## 步骤

### STEP 1: 收集 Raw Sources

**先确认工作目录**：`cd` 到 wiki 项目根目录（包含 `wiki/`、`raw/`、`scripts/` 的目录），所有后续路径都相对于此目录。

1. 扫描 `raw/papers/` 目录，识别所有文件：
   - 若为压缩包（`.tar.gz` / `.zip`）：在同目录下创建论文文件夹，解压到文件夹中，然后扫描文件夹内的 `.tex` 文件
   - 若 `.tex` 存在：优先使用（tex source > PDF）
   - 若只有 `.pdf`：使用 PyMuPDF 提取文本
   - 若解析失败：尝试 fallback（tex → PDF 解析，PDF → vision API 读取公式）
2. 扫描 `raw/notes/`、`raw/web/` 中的用户笔记和网页
3. 通过 arXiv 按 topic 搜索相关论文 → 运行 `scripts/fetch_arxiv.py`
   - 对搜索结果中相关度高的论文（最多 10 篇）：**下载 tex source 到 `raw/papers/`**
   - 下载方式：`curl -L "https://arxiv.org/e-print/{arxiv_id}" -o raw/papers/{slug}.tar.gz`，然后解压到 `raw/papers/{slug}/`
   - 若 tex 下载失败：下载 PDF `curl -L "https://arxiv.org/pdf/{arxiv_id}" -o raw/papers/{slug}.pdf`
4. 通过 Semantic Scholar 按 topic 搜索高引论文 → 运行 `scripts/fetch_s2.py search`
   - 对 wiki 中尚未收录的高引论文：同样下载到 `raw/papers/`
5. 所有来源汇总为 `raw_source_list`

### STEP 2: 领域分析

1. LLM 阅读 `raw_source_list`，提取核心主题
2. 识别 3-8 个子方向（concepts）
3. 识别 2-5 个核心研究问题（topics）
4. 识别关键人物（people）

### STEP 3: 搭建 wiki 骨架

1. `CREATE wiki/CLAUDE.md` — 运行时 schema（从模板复制或手写）
2. `CREATE wiki/index.md` — 填入初始条目
3. `CREATE wiki/log.md` — 首条日志
4. `CREATE wiki/Summary/{area}.md` — 领域全景综述
5. 对 `raw/papers/` 中每篇论文：执行 ingest 逻辑，生成 `wiki/papers/{slug}.md`
6. `CREATE wiki/concepts/` 中的核心概念页
7. `CREATE wiki/topics/` 中的方向页
8. `CREATE wiki/people/` 中的关键人物页
9. 对 `index.md` 和 `log.md` 进行完整填充

### STEP 4: 报告

- 列出创建的页面数
- 列出核心概念和方向
- 建议下一步：手动 ingest 更多论文 / 阅读 `wiki/Summary/` 查看全景

## 约束

- `raw/` 只读，不得修改
- 所有链接使用 `[[slug]]` wikilink 格式
- 写正向链接时同步写反向链接
- 页面模板遵循 `CLAUDE.md` 中的定义
