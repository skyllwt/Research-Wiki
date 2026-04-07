# Research Wiki

> CS/AI 研究者的个人知识库，由 Claude Code 驱动。

把论文放进 `raw/papers/`，运行 Claude Code，wiki 自动生成。

## 特性

- **零摩擦建库**：放入 .tex / .pdf，一个命令自动建 wiki
- **持续自动更新**：每天自动拉取 arXiv 新论文
- **知识变输出**：基于 wiki 生成 Related Work / Idea 列表
- **开箱即用**：5 种页面类型 + 7 个 Skill，预设 CS/AI Schema

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/yourname/research-wiki.git
cd research-wiki/repo
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

```bash
cp .env.example .env
# 编辑 .env，填入你的 ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 4. 放入论文

```bash
# 将你的论文放到 raw/papers/ 目录
cp /path/to/your-paper.tex raw/papers/
cp /path/to/another-paper.pdf raw/papers/
```

### 5. 运行

```bash
# 启动 Claude Code
claude

# 然后输入：
# /initial-wiki efficient fine-tuning for LLMs
```

## 使用方式

### Skills

| 命令 | 功能 |
|------|------|
| `/initial-wiki <topic>` | 从 raw/ 搭建完整 wiki |
| `/ingest <path-or-url>` | 消化一篇论文 |
| `/update <request>` | 增删 raw 或更新 wiki |
| `/daily-arxiv` | 拉取 arXiv 新论文 |
| `/write-related-work` | 生成 Related Work 段落 |
| `/idea-generation` | 构思新 idea |
| `/lint` | 健康检查 |

### 目录结构

```
repo/
├── CLAUDE.md          ← 运行时入口
├── wiki/              ← 知识库（LLM 维护）
│   ├── papers/        ← 论文摘要
│   ├── concepts/      ← 技术概念
│   ├── topics/        ← 研究方向
│   ├── people/        ← 研究者
│   ├── Summary/       ← 领域综述
│   └── outputs/       ← 生成物
├── raw/               ← 原始资料（只读）
│   ├── papers/        ← .tex / .pdf
│   ├── notes/         ← .md 笔记
│   └── web/           ← 网页内容
├── scripts/           ← 辅助脚本
├── skills/            ← Skill 定义
└── templates/         ← 页面模板
```

## 自动化

### GitHub Actions（每日 arXiv 更新）

1. 在仓库 Settings → Secrets 中添加 `ANTHROPIC_API_KEY`
2. `.github/workflows/daily-arxiv.yml` 每天 UTC 00:00（北京时间 08:00）自动运行

### 手动运行 lint

```bash
python scripts/lint.py --wiki-dir wiki/
```

## 页面类型

| 类型 | 用途 | 示例 |
|------|------|------|
| **papers/** | 论文结构化摘要 | `lora-low-rank-adaptation.md` |
| **concepts/** | 跨论文技术概念 | `parameter-efficient-fine-tuning.md` |
| **topics/** | 研究方向地图 | `efficient-llm-adaptation.md` |
| **people/** | 研究者追踪 | `tri-dao.md` |
| **Summary/** | 领域全景综述 | `llm-efficiency.md` |

## 链接系统

所有内部链接使用 Obsidian wikilink 格式：

```markdown
[[lora-low-rank-adaptation]]  ← 链接到论文
[[flash-attention]]           ← 链接到概念
```

写正向链接时自动同步反向链接，`/lint` 定期检查对称性。

可在 [Obsidian](https://obsidian.md/) 中打开 wiki/ 目录可视化浏览。

## 依赖

- Python 3.10+
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (`npm install -g @anthropic-ai/claude-code`)
- `ANTHROPIC_API_KEY`

## License

MIT
