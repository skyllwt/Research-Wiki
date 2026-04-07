<div align="center">

# 📖 Research Wiki

**AI-Powered Personal Knowledge Base for CS/AI Researchers**

*Inspired by Andrej Karpathy's [LLM-Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) concept — a structured, AI-maintained knowledge base for research.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-yellow.svg)](https://www.python.org/)
[![Claude Code](https://img.shields.io/badge/Powered%20by-Claude%20Code-d97706.svg)](https://docs.anthropic.com/en/docs/claude-code)

[English](#english) | [中文](#中文)

</div>

---

## English

### What is Research Wiki?

An AI agent that **automatically builds and maintains a structured research wiki** from your papers — powered by [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Drop `.tex` or `.pdf` files into a folder, run one command, and get a fully cross-referenced knowledge base with paper summaries, concept maps, researcher profiles, and more.

```
  raw/papers/          Claude Code Agent           wiki/
 ┌───────────┐        ┌──────────────┐         ┌──────────────────┐
 │ paper.tex │───────▶│  /ingest     │────────▶│ papers/          │
 │ paper.pdf │        │  /initial-wiki│        │ concepts/        │
 │ notes.md  │───────▶│  /update     │────────▶│ topics/          │
 └───────────┘        └──────────────┘         │ people/          │
                        │                      │ Summary/         │
  arXiv RSS ───────────▶│                      └──────────────────┘
  (daily auto)          │
                   ┌────┴─────┐
                   │ Outputs  │
                   ├──────────┤
                   │ Related  │
                   │ Work     │
                   │ Ideas    │
                   └──────────┘
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Zero-friction setup** | Drop `.tex` / `.pdf` into `raw/papers/`, run one command — wiki is built automatically |
| **Daily arXiv updates** | GitHub Actions cron fetches new papers from cs.LG, cs.CV, cs.CL, cs.AI, stat.ML daily |
| **Knowledge → Output** | Generate publication-ready **Related Work** paragraphs and novel **research ideas** from your wiki |
| **5 page types** | Papers, Concepts, Topics, People, Summaries — with structured YAML frontmatter |
| **7 Claude Code Skills** | Slash commands (`/ingest`, `/lint`, `/write-related-work`, etc.) that run autonomously |
| **Obsidian-compatible** | All links use `[[wikilink]]` format — open `wiki/` in Obsidian for visual graph browsing |

### Quick Start

```bash
# 1. Clone
git clone https://github.com/skyllwt/Research-Wiki.git
cd Research-Wiki

# 2. Install dependencies (pick one)
# Option A: uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Option B: conda
conda create -n research-wiki python=3.10 -y
conda activate research-wiki
pip install -r requirements.txt

# 3. Configure
cp config/settings.local.json.example .claude/settings.local.json
cp config/.env.example .env
# Edit .env → add your S2_API_KEY (optional)

# 4. Build your wiki
claude
# Then type:
# /initial-wiki efficient fine-tuning for LLMs
```

### Skills (Slash Commands)

| Command | What it does |
|---------|-------------|
| `/initial-wiki <topic>` | Bootstrap a full wiki from `raw/` |
| `/ingest <path-or-url>` | Parse a paper and create wiki pages with cross-references |
| `/update <request>` | Add/remove sources or update wiki content |
| `/daily-arxiv` | Fetch & filter new arXiv papers (runs daily via CI) |
| `/write-related-work` | Generate a Related Work section from your wiki |
| `/idea-generation` | Surface novel research ideas from cross-topic connections |
| `/lint` | Scan wiki for broken links, missing cross-refs, health issues |

### Automation

**GitHub Actions** runs daily at UTC 00:00 (08:00 Beijing time):

1. Add `ANTHROPIC_API_KEY` to repo **Settings → Secrets**
2. The workflow in `.github/workflows/daily-arxiv.yml` fetches new arXiv papers, runs `/daily-arxiv`, and auto-commits results

Manual lint check:
```bash
python scripts/lint.py --wiki-dir wiki/
```

---

## 中文

### 这是什么？

一个由 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 驱动的 **AI 研究知识库**。把论文放进文件夹，运行一条命令，就能自动构建一个带交叉引用的结构化 wiki —— 包括论文摘要、概念地图、研究者档案、领域综述等。

灵感来源于 Andrej Karpathy 的 [LLM-Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 概念。

### 主要特性

- **零摩擦建库** — 放入 `.tex` / `.pdf`，一个命令自动生成 wiki
- **每日 arXiv 更新** — GitHub Actions 自动拉取 cs.LG / cs.CV / cs.CL / cs.AI / stat.ML 新论文
- **知识变输出** — 基于 wiki 自动生成可发表的 **Related Work** 段落和 **研究 idea**
- **5 种页面类型** — 论文、概念、方向、人物、综述，全部使用结构化 YAML frontmatter
- **7 个 Skill** — `/ingest`、`/lint`、`/write-related-work` 等斜杠命令全自动执行
- **Obsidian 兼容** — 所有链接使用 `[[wikilink]]` 格式，可在 Obsidian 中可视化浏览

### 快速开始

```bash
git clone https://github.com/skyllwt/Research-Wiki.git && cd Research-Wiki

# 安装依赖（二选一）
# uv（推荐）
uv venv && source .venv/bin/activate && uv pip install -r requirements.txt
# 或 conda
conda create -n research-wiki python=3.10 -y && conda activate research-wiki && pip install -r requirements.txt

# 配置
cp config/settings.local.json.example .claude/settings.local.json
cp config/.env.example .env   # 编辑填入 S2_API_KEY（可选）

# 运行
claude
# 输入：/initial-wiki efficient fine-tuning for LLMs
```

### Skill 命令

| 命令 | 功能 |
|------|------|
| `/initial-wiki <topic>` | 从 raw/ 搭建完整 wiki |
| `/ingest <path-or-url>` | 消化一篇论文，创建页面并建立交叉引用 |
| `/update <request>` | 增删 raw 或更新 wiki 内容 |
| `/daily-arxiv` | 拉取 arXiv 新论文（每日自动运行） |
| `/write-related-work` | 基于 wiki 生成 Related Work 段落 |
| `/idea-generation` | 从交叉方向中构思新 idea |
| `/lint` | 全 wiki 健康检查 |

---

### Project Structure

```
research-wiki/
├── CLAUDE.md              # Runtime schema & rules
├── wiki/                  # The knowledge base (maintained by Claude)
│   ├── papers/            # Structured paper summaries
│   ├── concepts/          # Cross-paper technical concepts
│   ├── topics/            # Research direction maps
│   ├── people/            # Researcher profiles
│   ├── Summary/           # Domain-wide surveys
│   └── outputs/           # Generated Related Work / Ideas
├── raw/                   # Source materials (read-only)
│   ├── papers/            # .tex / .pdf files
│   ├── notes/             # .md notes
│   └── web/               # HTML / Markdown
├── scripts/               # Python helpers (fetch_arxiv, fetch_s2, lint)
├── .claude/skills/        # 7 Claude Code Skill definitions
├── config/                # Configuration templates
└── .github/workflows/     # GitHub Actions (daily arXiv cron)
```

### Wiki Page Types

All pages use Obsidian `[[wikilink]]` format with **mandatory bidirectional cross-references**.

| Type | Directory | Purpose | Example |
|------|-----------|---------|---------|
| Paper | `papers/` | Structured summary | `lora-low-rank-adaptation.md` |
| Concept | `concepts/` | Cross-paper concept | `parameter-efficient-fine-tuning.md` |
| Topic | `topics/` | Research direction map | `efficient-llm-adaptation.md` |
| People | `people/` | Researcher tracker | `tri-dao.md` |
| Summary | `Summary/` | Domain survey | `llm-efficiency.md` |

### Requirements

- Python 3.10+
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (`npm install -g @anthropic-ai/claude-code`)
- `ANTHROPIC_API_KEY` (handled by Claude Code auth)
- `S2_API_KEY` (optional, recommended for 100+ papers)

### License

[MIT](LICENSE)

---

<div align="center">

**Built with [Claude Code](https://docs.anthropic.com/en/docs/claude-code)**

If this project helps you, consider giving it a star!

</div>
