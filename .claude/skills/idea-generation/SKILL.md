---
name: idea-generation
description: 基于 wiki 知识库构思新的研究 idea
---

# /idea-generation

> 基于 wiki 知识库，构思新的研究 idea。

## 触发

用户手动：`/idea-generation`（可无参数或有用户输入）

## 输入

- `user_input`：研究方向或关键词（可选）

## 输出

- `wiki/outputs/idea-{topic}-{date}.md` — Idea 列表

## 步骤

### STEP 1: 全局扫描

1. 读取 `wiki/index.md` + `wiki/topics/` + `wiki/concepts/`
2. 识别 open problems、research gaps
3. 识别 concepts 之间的交叉点
4. 识别不同论文 Results 中的 contradiction

### STEP 2: 分析与组合

1. **跨方向组合**：Topic A 的方法 + Topic B 的问题
2. **填补空白**：open problems 中尚无解决方案的
3. **矛盾探究**：不同论文对同一问题的矛盾结论 → 推导新假设
4. **SOTA 突破**：当前 SOTA 的已知 limitation → 改进方向

### STEP 3: 生成 idea 列表

每个 idea 包含：

```markdown
### Idea N: {title}

**核心思路**：3-5 句描述

**依据**：
- [[paper-slug]] — {为什么这篇论文支持这个 idea}
- [[concept-slug]] — {为什么这个概念相关}

**可行性评估**：高 / 中 / 低

**新颖性评估**：{基于 wiki 中已知工作的判断}

**潜在风险**：{主要挑战和不确定性}
```

### STEP 4: 归档

1. `CREATE wiki/outputs/idea-{topic}-{date}.md`
2. `APPEND wiki/log.md`：`## [{date}] idea-generation | {N} ideas`

## 约束

- 所有 idea 必须基于 wiki 中已有的知识推导，不凭空编造
- 每个 idea 必须引用至少 2 个 wiki 页面作为依据
- 如果 wiki 中论文不足 5 篇，提示用户先建立更完整的知识库
- 输出归档到 `outputs/`，不直接修改 wiki 页面
