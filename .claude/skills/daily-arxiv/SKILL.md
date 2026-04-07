---
name: daily-arxiv
description: 每日从 arXiv 拉取新论文，过滤相关性，生成 digest
---

# /daily-arxiv

> 每日从 arXiv 拉取新论文，过滤相关内容，生成 digest。

## 触发

- cron 每天 08:00（北京时间）自动执行
- 用户手动：`/daily-arxiv`

## 输入

- arXiv RSS feed（配置的 categories）
- `wiki/topics/` 中的研究方向关键词

## 输出

- `wiki/log.md` 中追加 digest 日志
- 高优先级论文直接 ingest（创建 papers 页面）

## 步骤

### STEP 1: 拉取 RSS

1. 运行 `python scripts/fetch_arxiv.py -o /tmp/arxiv_feed.json`
2. 拉取配置的 categories（cs.LG cs.CV cs.CL cs.AI stat.ML）
3. 获取过去 24 小时的论文列表
4. 去重：跳过已在 wiki 中的论文（检查 `index.md` 中的 arxiv URL）

### STEP 2: 相关性过滤

1. 读取 `wiki/topics/` 中的 Overview 段落，提取关键词
2. 读取 `wiki/concepts/` 中的 Definition 段落，提取关键词
3. 对每篇新论文：LLM 判断与用户研究方向的相关性（0-3 分）
   - 3 = 高度相关，核心方向
   - 2 = 中度相关，值得关注
   - 1 = 弱相关，仅供参考
   - 0 = 不相关，跳过

### STEP 3: 分级处理

1. **相关性 = 3**：标记为高优先级
   - 执行完整 ingest 流程（创建 `wiki/papers/{slug}.md`）
   - 在 digest 中突出显示
2. **相关性 = 2**：加入 digest，值得关注
   - 不自动 ingest，用户可手动 `/ingest`
3. **相关性 <= 1**：仅在 digest 中列出（可折叠摘要）

### STEP 4: 生成 digest

1. `APPEND wiki/log.md`：

```
## [YYYY-MM-DD] daily-arxiv | {N}篇相关 / {M}篇总计

### 高优先级（已 ingest）
- [[slug]] — {title}（{one-line summary}）

### 值得关注
- {title} — {arxiv_url} — {one-line summary}

### 其他（弱相关）
<details>
<summary>{K} 篇</summary>
- {title}
</details>
```

### STEP 5: SOTA 更新检测

1. 若某篇高优先级论文的 benchmark 优于 `topics/` 中的 SOTA 记录：
   - 在对应 topic 页面标记需要更新
   - 在 lint-report 中报告

## 约束

- 只 ingest 相关性 >= 3 的论文，其余留给用户判断
- `raw/` 只读
- digest 保持简洁，详情查看具体 papers 页面
- 每天最多 ingest 5 篇（避免 wiki 过载），其余排队
