# research-wiki · CLAUDE.md

> **你在做什么**：这是一个 spec-first 项目工作区。当前阶段是**设计阶段**，还没有实际代码。你和用户在这里共同迭代、修改、收敛设计稿。等设计稿确定后，再进入实现阶段。

---

## 当前阶段与任务

**阶段**：设计稿迭代（Phase 1）  
**你的角色**：设计协作者 + 文档执行者  
**不要做的事**：不要写实现代码，不要创建 `wiki/` 目录下的真实内容

每次对话开始，先读 `spec/` 目录的当前状态，理解哪些已决策、哪些仍在讨论。

---

## spec/ 目录地图

| 目录 | 内容 | 状态标记位置 |
|------|------|-------------|
| `00-origin/` | Karpathy 原始 blog，只读参考 | — |
| `01-vision/` | 项目定位、目标用户、与 RAG 的差异化 | 文件顶部 status |
| `02-architecture/` | 系统模块、数据流、模块间关系 | 文件顶部 status |
| `03-wiki-schema/` | 六类页面定义、字段、链接关系、YAML schema | 文件顶部 status |
| `04-workflows/` | 5 条 workflow 的伪代码级定义 | 文件顶部 status |
| `05-tech-stack/` | 工具选型、依赖、实现细节 | 文件顶部 status |
| `06-decisions/` | ADR 决策记录，每个重要决定一个文件 | 文件名前缀编号 |

**status 取值**：`draft` / `in-review` / `settled` / `needs-revision`

---

## 如何参与设计迭代

当用户说"修改 X"或"我觉得 Y 应该这样"时：

1. 读取相关 spec 文件的当前内容
2. 在文件内**直接修改**，不要创建新文件
3. 更新文件顶部的 `status` 和 `last-updated`
4. 如果这次修改涉及重要决策，在 `06-decisions/` 新增一个 ADR
5. 告诉用户改了什么、为什么这样改、还有哪些未决问题

当用户问"现在设计是什么样的"时：
- 读取相关文件，用自然语言总结，不要只是复制粘贴文件内容

---

## 文件命名规范

- spec 文件：`{topic}.md`，放在对应目录
- ADR 文件：`ADR-{NNN}-{short-title}.md`，放在 `06-decisions/`
- 模板文件：`template-{page-type}.md`，放在 `templates/`
- 示例文件：放在 `examples/{papers|concepts|experiments}/`

---

## 项目背景（30 秒版本）

这个项目把 Karpathy 的 LLM Wiki 思想应用到 CS/AI 科研场景。核心差异：

- **Karpathy**：通用知识积累，pattern 抽象
- **本项目**：CS/AI 科研专用，有论文/实验/方向/概念四种核心知识单元，有 arXiv 追踪、Related Work 生成等科研专属 workflow

完整背景见 `spec/00-origin/karpathy-blog.md` 和 `spec/01-vision/vision.md`。

---

## 进入实现阶段的条件

所有 `spec/` 文件的 status 都达到 `settled`，且用户明确说"开始实现"。
