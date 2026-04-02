---
name: agent-execution-safety-review
description: 使用 Freely 的 execution-boundary audit 与 security-review brief，在不退化成用户逐步批准的前提下决定是否继续、单 reviewer 复核，或拉起内部 decision committee。
---

# skill:agent-execution-safety-review

## 何时使用

- 需要判断当前 execution boundary 是否足够对齐，还是应先做内部安全复核
- 需要把 reviewer / committee 语义从对话习惯变成可复用能力
- 需要在高自治下提供 reviewer-backed continuation guidance，而不是退回逐步人工批准

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
4. 把 brief 关键字段写回 issue / progress / verification 或 runtime handoff，避免靠会话记忆复述

## 非目标

- 不接管 product-facing activation consent
- 不把用户拉回逐步批准主路
- 不自动修复所有安全问题

## References

- [decision-ladder.md](references/decision-ladder.md)
- [evidence-writeback.md](references/evidence-writeback.md)
