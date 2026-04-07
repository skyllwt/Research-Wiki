---
title: "Parameter-Efficient Fine-Tuning"
tags: [fine-tuning, efficiency, adaptation]
maturity: stable
key_papers: [lora-low-rank-adaptation, adapter-methods, prefix-tuning, adalora, qlora]
first_introduced: "Adapter layers, Houlsby et al., ICML 2019"
date_updated: 2026-04-07
related_concepts: [full-fine-tuning, prompt-tuning, quantization]
---

## Definition

Parameter-Efficient Fine-Tuning（PEFT）是一类只调整预训练模型极少数参数来完成任务适配的方法。相比全量微调，PEFT 将可训练参数量从数十亿降低至数百万，同时维持接近全量微调的任务效果。

## Intuition

预训练大模型已经"学会了"大量通用能力。任务适配所需的修改是低维的——就像一个掌握多国语言的人，学会一种新方言只需要调整"口音层"，而不需要重新学习语言。PEFT 的各种方法都在寻找这个最小必要的"调整层"。

## Variants

| 方法 | 原理 | 代表工作 | 额外推理延迟 |
|------|------|----------|-------------|
| Adapter | 在 FFN 后插入瓶颈层 | [[adapter-methods]] | 有（串行） |
| LoRA | 权重矩阵低秩分解 | [[lora-low-rank-adaptation]] | **无**（可合并） |
| Prefix Tuning | 在输入前拼接可训练 prefix token | [[prefix-tuning]] | 有（序列变长） |
| Prompt Tuning | 只调 embedding 层的 soft prompt | — | 有 |
| AdaLoRA | 自适应分配 rank 预算 | [[adalora]] | 无 |
| QLoRA | LoRA + 4-bit 量化，降低显存 | [[qlora]] | 略有 |

## Comparison

| 方法 | 参数量 | 推理延迟 | 实现难度 | 效果（相对 FFT） |
|------|--------|----------|----------|-----------------|
| Full FT | 100% | 基准 | 低 | 100% |
| Adapter | ~0.5-3% | +10-15% | 低 | 95-99% |
| LoRA | ~0.01-1% | **0%** | 低 | 95-100% |
| Prefix Tuning | ~0.1% | +5% | 中 | 90-95% |
| QLoRA | ~0.01-1% | <5% | 中 | 93-99% |

## When to use

**适合 PEFT**：
- 显存/存储受限（LoRA 的 AB 矩阵只有几十 MB）
- 多任务场景（每个任务一套 adapter/LoRA，共享主干）
- 对推理延迟敏感（选 LoRA，推理时合并权重）
- 数据量中等（1k-100k 样本）

**不适合 PEFT**：
- 任务与预训练分布差异极大（需要全量微调）
- 数据量极少（< 100 样本，用 in-context learning）
- 需要修改模型的世界知识（LoRA 无法修改冻结权重中的知识）

## Known limitations

- 最优 rank/prefix 长度需要 ablation，缺少通用准则
- 对 OOD（分布外）泛化的提升弱于全量微调
- 多个 adapter 并行时内存管理复杂

## Open problems

- 如何自动选择最优 rank/adapter 位置？（AdaLoRA 探索了这个方向）
- PEFT 与 continual learning 的结合？
- 对于 MoE 架构，PEFT 的最优策略是什么？

## Key papers

### 奠基论文
- [[adapter-methods]] — Houlsby et al. 2019，第一个系统性 adapter 方法
- [[lora-low-rank-adaptation]] — Hu et al. 2022，低秩分解，目前最广泛使用

### 改进与变体
- [[adalora]] — 自适应 rank 分配
- [[qlora]] — LoRA + 4-bit 量化，消费级 GPU 微调 65B 模型

### 综述
- "Scaling Down to Scale Up: A Guide to PEFT" — 系统性综述

## My understanding

LoRA 是目前最值得优先使用的 PEFT 方法，原因是推理零额外延迟且效果最好。

个人困惑：为什么在 q,v 矩阵上使用 LoRA 比 q,k,v,o 都用效果更好？直觉上后者参数更多应该效果更好，但 LoRA 论文的 ablation 显示并非如此。可能是训练稳定性的问题。
