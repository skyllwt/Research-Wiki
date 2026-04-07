---
title: "LoRA: Low-Rank Adaptation of Large Language Models"
slug: lora-low-rank-adaptation
arxiv: "https://arxiv.org/abs/2106.09685"
venue: ICLR 2022
year: 2022
tags: [fine-tuning, efficiency, parameter-efficient, adaptation]
status: done
importance: 5
date_added: 2026-04-07
code_url: "https://github.com/microsoft/LoRA"
cited_by: []
experiments: []
discovered_via: manual
---

## Problem

全量微调（full fine-tuning）大语言模型成本极高：对于 GPT-3（175B），每次任务适配需要存储和部署独立的完整副本，不仅存储开销巨大，而且对下游任务的推理延迟没有改善。需要一种参数高效的微调方法，能在不牺牲效果的前提下大幅降低可训练参数量。

## Key idea

冻结预训练权重矩阵，对每个 Transformer 层注入可训练的低秩矩阵对 (A, B)。
训练时只更新 A 和 B（参数量减少 10,000 倍），推理时将 ΔW = BA 合并回 W₀，**零额外推理延迟**。

核心洞察：预训练模型权重的"内在维度"（intrinsic dimensionality）远低于全参数空间，低秩近似足以捕捉任务适配所需的变化。

## Method

对权重矩阵 W₀ ∈ ℝ^{d×k}，前向传播修改为：

```
h = W₀x + ΔWx = W₀x + BAx
```

其中 B ∈ ℝ^{d×r}，A ∈ ℝ^{r×k}，秩 r ≪ min(d, k)。

初始化：A 用高斯分布，B 初始化为零（确保训练初始时 ΔW = 0，不破坏预训练特征）。

缩放因子 α/r 用于控制 ΔW 的学习率，避免随 r 变化需要重新调整 lr。

实验中 r=4 或 r=8 在大多数任务上已足够，作者在 q,v 矩阵上使用 LoRA（不对所有矩阵使用）。

## Results

在 GPT-3 上与 full fine-tuning 对比（RoBERTa/DeBERTa/GPT-2/GPT-3）：

| 方法 | 可训练参数 | ROUGE-1 (XSum) | 存储 |
|------|-----------|----------------|------|
| Full FT | 175B | 67.1 | 350GB |
| LoRA r=4 | **4.7M** | **67.9** | 35MB |
| LoRA r=64 | 75.5M | 68.2 | 150MB |

效果与 full fine-tuning 相当甚至略优，参数量减少 4 个数量级。

## Limitations

- r 的选择需要 ablation 实验，没有自动化方法
- 对于需要大幅修改预训练知识的任务（如领域迁移）效果有限
- 论文主要在语言模型上验证，视觉模型的最优 r 可能不同
- LoRA 改变了哪些矩阵（q/k/v/o）的最优组合未被充分探索

## Open questions

- 最优 r 与任务难度/数据量的关系？
- LoRA 是否适用于 Mixture-of-Experts 架构？
- rank-adaptive 版本（AdaLoRA）能否成为默认选择？

## My take

⭐⭐⭐⭐⭐ 必读论文。

思路极简（低秩近似），实现极易（几十行代码），效果极强（接近全量微调）。
已成为 PEFT 领域的事实标准，几乎所有后续工作都以 LoRA 为基准。

适用于：资源受限的微调、多任务切换（只需切换 AB 矩阵）、对推理延迟敏感的场景。
不适用于：需要深度修改模型先验知识、数据量极小（< 100 样本）的场景。

## Related

[[parameter-efficient-fine-tuning]]  [[adapter-methods]]  [[prefix-tuning]]  [[adalora]]
