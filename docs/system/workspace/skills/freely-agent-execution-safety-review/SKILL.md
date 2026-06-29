---
name: freely-agent-execution-safety-review
description: >- 在 Freely workspace 中执行 execution-boundary review，输出 reviewer-backed security decision 与 machine-readable evidence。不退化或逐步批准。

  Use when: 安全敏感变更需要 execution-boundary 独立审查。
  触发词："安全审查"、"execution review"、"boundary check"、"execution boundary"。
---

# skill:freely-agent-execution-safety-review

## 何时使用

- 需要判断当前 execution boundary 是否足够对齐，还是应先做内部安全复核
- 需要把 reviewer / committee 语义从对话习惯变成可复用能力
- 需要在高自治下提供 reviewer-backed continuation guidance，而不是退回逐步人工批准

## 职责

- 对齐 project-local config、launch-time injection、tool flags 和 observed posture。
- 在不把用户拉回逐步审批的前提下，组织 reviewer-backed security guidance。
- 输出可写回 issue / progress / verification 的 advisory evidence。

## 不负责

- 不直接改写 launch blockers、approval posture 或 fallback policy。
- 不把 safeguard recommendation 自动升级成 runtime stop。
- 不替代 product-facing activation consent owner。
- 不自动修复所有安全问题。

## 核心流程

1. 先运行：
   - `./bin/freely security-review-brief --project <project-root>`
2. 读取以下真相：
   - `execution_boundary_audit_status`
   - `execution_boundary_audit_detail`
   - `security_review_mode`
   - `recommended_reviewer_count`
   - `recommended_review_scope`
   - `security_review_decision`
   - `continuation_guidance`
   - `minimal_risk_state`
3. 按 decision ladder 处理：
   - `none`: 当前 agent 可继续
   - `single-reviewer`: 拉起一个 security-focused reviewer
   - `decision-committee`: 拉起两个或更多相互独立的 reviewer，再由主执行者综合
4. 把 brief 关键字段按 `references/evidence-writeback.md` 写回 issue / progress / verification 或 runtime handoff，避免靠会话记忆复述。

## References

- [decision-ladder.md](references/decision-ladder.md)
- [evidence-writeback.md](references/evidence-writeback.md)
