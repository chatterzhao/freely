# Candidates - 20260401-2354--implementation-decision-notes-in-review-artifacts

## Context
- Source brainstorm: `./brainstorms.md`
- Status: active

## Candidates

### C-20260401-2354-A
- candidate_format_version: v2
- title: Implementation decision notes in issue-bound review artifacts
- problem: Freely 已把 candidate / PRD / pre-tests / verification 各层的治理边界基本冻结，但 dev-loop 里的具体实现决策仍缺少统一、可追溯、可 gate 的记录面。现在 reviewer 可能看到代码和测试，却无法直接恢复“为什么这次选这个实现、拒绝了哪些方案、还有哪些边界与残余风险”。
- why_now: 用户已经明确提出要把这层 `proof of thoughtfulness` 做成 Freely 自己的 canonical mechanism，并且要求不要随机落点、不要只靠 skill 提示词。现有 merge gate 已经具备 owner issue 与 review artifact 关联能力，现在正是补这层最小 enforcement 的窗口。
- acceptance_criteria:
  - 冻结 implementation decision note 的 canonical landing surface 为 issue-bound `code-reviews/` / verification artifact，而不是新建平行目录
  - 冻结最小字段：`decision`、`why_this`、`alternatives_considered`、`boundary_non_goals`、`residual_risk`
  - 冻结何时强制：develop-bound implementation-bearing diff 默认必须携带 decision note；research-only / IBM-only / milestone reshuffle 不强制
  - 冻结 gate 的 owner association：从当前 issue 的 `verification_artifact_dir` 出发，而不是扫描全仓 review files
  - 冻结这条能力与 candidate / PRD / pre-tests 的关系：它承接 dev-loop decision，不重写上游 thoughtfulness
- promotion_gate:
  - 已确认 canonical landing surface 应放在 review artifact，而不是 `progress`、`prd.md` 或新目录
  - 已确认这条能力需要 gate 才足够稳，不能只停在 laws / skill prose
  - 已确认 gate 可以复用 `verification_artifact_dir` 与 `governance-merge-gate`，不必另造索引系统
  - 已确认最小字段足够表达 implementer thoughtfulness，而不会把 review artifact 变成 PRD 重写
- open_questions:
  - implementation-bearing path 的首批识别范围是仅 `bin/`、`docs/system/`、`src/`，还是要把更多 capability roots 一并纳入
  - gate 是否只要求 staged review artifact 中存在完整 note，还是未来还要进一步要求与 changed issue slices 一一对应
  - 对 purely verification-only replay closeout，是否允许复用旧 decision note 而不强制新写一份
- acceptance_reviews:
  - reviewer: `codex`
    mode: `initial candidate acceptance review`
    summary: `The missing layer is not candidate/PRD thoughtfulness; it is the owner-bound implementation decision note in dev-loop review artifacts. This is narrow enough to materialize directly as a gate-backed governance owner.`
    verdict: `ready_for_issue_materialization`
- priority: P0
- status: `promoted`
- decision_reason: 边界已经稳定，不值得继续只做研究。最小实现就是把 implementation decision note 固定到 issue-bound review artifact，并由 `governance-merge-gate` 通过 `verification_artifact_dir` 强制存在与最小结构。
- next_action: materialize focused governance issue, update laws / skills / IBM checklist, implement merge-gate enforcement and regression tests, then keep the owner in `in_verification` until develop merge validates the gate in real usage.
- revisit_trigger: 如果 field evidence 证明 implementation-bearing path detection 过宽或过窄，或 review artifact 的最小字段仍不足以恢复关键设计取舍，再以 follow-on 收窄 detection scope 或补充 note schema。
- promoted_issue_id: `I-20260401-2354-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/implementation-decision-notes-in-issue-review-artifacts-governance/issues/implementation-decision-notes-in-issue-review-artifacts-governance.md`
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
    session_id: current-thread
    jsonl_path: unavailable://codex-thread-only
    role: author
