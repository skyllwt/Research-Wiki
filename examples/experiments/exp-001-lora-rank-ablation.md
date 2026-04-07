---
exp_id: exp-001
title: "LoRA rank ablation on small instruction dataset"
status: done
hypothesis: "在 1k 样本指令数据集上，r=4 的效果与 r=16 相差不超过 1% ROUGE-L"
date_started: 2026-03-10
date_done: 2026-03-12
paper_motivation: [lora-low-rank-adaptation]
next_exp: exp-002
concepts_validated: [parameter-efficient-fine-tuning]
---

## Hypothesis

在资源极度受限的场景（1000 条指令数据，单卡 A100），LoRA 的秩 r 从 4 增大到 16 带来的增益会小于 1% ROUGE-L，不值得额外的参数和计算开销。

预期方向：r=4 ≈ r=16，意味着小数据集上低秩已经足够捕捉任务适配信息。

## Setup
- 模型：LLaMA-3-8B（Hugging Face）
- 数据集：Alpaca-1k（从 Alpaca-52k 随机采样 1000 条）
- 超参数：lr=2e-4, epochs=3, batch=4, gradient_accumulation=4
- LoRA target modules：q_proj, v_proj
- α = 2r（标准设置）
- 硬件：A100 40G × 1
- 评估集：Alpaca-eval 200 条（固定随机种子）

## Baseline

全量微调（Full FT）在相同数据下的 ROUGE-L：39.8（来自 [[lora-low-rank-adaptation]] 复现）

## Results

| rank r | ROUGE-L | 损失 | 训练时间 | 峰值显存 |
|--------|---------|------|----------|----------|
| 1      | 31.2    | 1.82 | 11min    | 18.2 GB  |
| 4      | 38.9    | 1.61 | 13min    | 18.6 GB  |
| 8      | 39.0    | 1.60 | 14min    | 19.1 GB  |
| 16     | 39.1    | 1.59 | 16min    | 20.3 GB  |
| 64     | 39.0    | 1.60 | 22min    | 24.7 GB  |

## Analysis

**假设成立**（置信度：高）

r=4 到 r=16 的 ROUGE-L 差异为 0.2%，远低于 1% 阈值。r=4 训练时间比 r=16 少 3 分钟，显存少 1.7GB。

有趣发现：r=64 比 r=16 效果略差，可能是过拟合（1k 数据量对 64 秩来说过少）。这与论文中的发现一致。

r=1 的断崖式下降（31.2 vs 38.9）说明存在一个最小有效 rank 阈值，在本实验设置下约为 r=4。

## Conclusion

**在 1k 样本指令数据集上，r=4 是最优选择**：效果接近 r=16，但训练更快、显存更省。

不建议盲目增大 r，在小数据场景下可能适得其反。

## Next steps

→ [[exp-002]]：在 10k 数据集上重复实验，验证结论是否随数据量变化。
预期：数据量增大后，较大的 r 可能开始带来更明显的收益。
