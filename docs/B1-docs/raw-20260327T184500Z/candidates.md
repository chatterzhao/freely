# Candidates - 20260327-1845--manager-consumed-continuity-resume-routing-drift

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260327T184500Z-A: legacy issue
- title: Anchor manager resume to consumed continuity before reopening full patrol
- problem: manager 在 runtime cleanup followthrough 已闭环后，下一轮 resume 仍可能默认回到 generic first-hop patrol，而不是沿刚刚 consumed 的 continuity 继续同一条 owner chain，导致 supervision drift 到低价值全局扫描。
- why_now: 2026-03-27 canonical `develop` 现场已经出现这一形态。它不会触发 restart storm，也不完全符合 semantic-loop suspicion，但会继续烧 token 并让 manager 偏离当前 active issue family。
- acceptance_hint:
  - 明确 manager `resume` 何时必须优先承接 latest consumed continuity
  - 明确哪些 route_kind 允许 resume narrowing，哪些情况必须重新 full patrol
  - 提供脚本级回归测试，证明 fresh delegated continuation / contradiction 不会被错误压制
- priority: P0
- status: absorbed
- adoption_type: supporting_evidence
- milestone: M-20260327T184500Z-A
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260307-1201I-20260327T184500Z-A/issue.md
- decision_reason: 当前缺口仍属于 latest manager continuity consumption / manager resume contract 的 same-family followthrough，不需要再新开独立 lifecycle；这条 pre-brainstorm 仅保留 discovery 边界与吸收理由，正式实现和验证回到 `I-20260322T044500Z`。
- next_action: 在 `I-20260322T044500Z` 的 progress / verification 中补写 consumed-continuity resume drift addendum，并把当前 runtime prompt narrowing 修复和测试收口为 same-family followthrough。
- revisit_trigger: 若后续发现它已经超出 latest manager continuity consumption contract，例如演变成独立 patrol planner / route engine redesign，再重新 materialize。
- session_refs:
  - tool: codex
    session_id: current-thread
    jsonl_path: unavailable://codex-thread-only
    role: author
