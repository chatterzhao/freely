---
name: freely-candidate-acceptance-review
description: >- 对 pre-brainstorm candidate 做独立 acceptance review。重点审 acceptance_criteria、
  promotion_gate、open_questions 与 acceptance_reviews 的完整性和可验证性。

  Use when: candidate 准备 promotion、影响边界大、或 milestone 关键节点。
  触发词："acceptance review"、"候选评审"、"promotion review"、"candidate 审查"。
---

# skill:freely-candidate-acceptance-review

## 目标

这不是重做整个 brainstorm。

只审 candidate 是否已经足够稳定，可以从 pre-brainstorm 继续 promotion。

## 重点检查

- `acceptance_criteria` 是否表达了 pre-brainstorm 完成条件
- `promotion_gate` 是否表达了进入 `freely-doc-B2_IBM-execution` skill 前必须满足的边界
- `open_questions` 是否仍暴露关键未决问题
- `acceptance_reviews` 是否已有独立 review 记录

## reviewer 模式

优先以下独立 reviewer：

- `subagent`
- `fresh_process`
- `peer_worker`

不要只让同一作者自审后就直接 promotion。

## 何时至少一次 review

- candidate 准备从研究态进入 promotion 决策
- candidate 的边界会影响后续 worker 行为
- candidate 会改变 loop placement / owner / canonical artifact

## 何时优先多个独立 review

- 涉及跨工位 / 跨分支 / execution base / depends_on
- 涉及 runtime / manager / control-plane 治理边界
- signal 或 candidate 本身复杂、组合性强、容易带入实现偏见

## 输出

至少写回 candidate 的 `acceptance_reviews`，包含：

- `reviewer`
- `mode`
- `summary`
- `verdict`

verdict 推荐：

- `pass`
- `needs_more_research`
- `block_promotion`
