---
name: lint
description: 扫描全 wiki 发现健康问题，生成修复建议报告
---

# /lint

> 扫描全 wiki，发现健康问题，生成修复建议。

## 触发

- 每两周自动（或用户手动）
- 用户手动：`/lint`

## 输入

- 全 wiki 目录

## 输出

- lint report（直接报告给用户，或 `wiki/lint-report-{date}.md`）

## 步骤

### STEP 1: 结构完整性

1. 扫描所有 `[[link]]`，验证目标文件存在
2. 找出孤岛页面（无任何入链）
3. 找出必填字段缺失：
   - papers: title, slug, tags, importance
   - concepts: title, tags, maturity, key_papers
   - topics: title, tags
   - people: name, tags
   - Summary: title, scope, key_topics

### STEP 2: Cross Reference 对称性

1. 验证所有正向链接对应的反向链接是否存在
2. 检查：
   - papers → concepts 的 Related 链接，concepts 的 key_papers 是否回链
   - papers → people 的引用，people 的 Key papers 是否回链
   - topics → people 的 key_people，people 的 Research areas 是否覆盖
3. 生成不对称链接列表

### STEP 3: 内容一致性

1. 矛盾表述检测（不同页面对同一事实的描述不一致）
2. SOTA 记录超过 6 个月未更新
3. `importance=5` 但无 concept 页引用
4. concepts 中 `maturity=stable` 但只有 1 篇 key_paper

### STEP 4: 待补充建议

1. concepts 中 key_papers 只有 1 篇的（可能不完整）
2. topics 中 open_problems 为空的
3. people 中 Recent work 超过 6 个月未更新的

### STEP 5: 生成报告

按优先级排序：

- **🔴 需立即修复**：broken links、missing required fields
- **🟡 建议修复**：xref asymmetry、stale SOTA
- **🔵 可选优化**：orphan pages、incomplete concepts

报告格式：

```
## Lint Report — YYYY-MM-DD

**Summary**: N 🔴, M 🟡, K 🔵

### 🔴 需立即修复
1. [file] — {issue description}

### 🟡 建议修复
1. [file] — {issue description}

### 🔵 可选优化
1. [file] — {issue description}
```

## 约束

- **只报告，不自动修复**
- 用户确认后才执行修改
- 可辅助运行 `python scripts/lint.py` 进行结构检查
- 不修改 `raw/` 下的文件
