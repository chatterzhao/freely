# Candidates - 20260321-1435--legacy-promoted-candidate-normalization

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260321-1435-A: legacy issue
- title: Normalize legacy promoted candidates that never materialized
- problem: 一批 legacy candidate 仍写着 `status: promoted`，但 `promoted_issue_path` 仍是 `pending://issue-materialization`，制造了假的 issue 生命周期。
- why_now: 当前 sweep 已进入最终 review / promote-ready 阶段，继续保留这类假 promotion 会污染主管监督和 worktree governance。
- acceptance_hint:
  - 不伪造新的 issue 绑定
  - 已被主线吸收的改为 `superseded`
  - 尚未达到 materialization gate 的回到 `needs_research/proposed`
  - 不改变已真实 materialize 的 candidate / issue / milestone 链路
- priority: P0
- status: dropped
- decision_reason: 这轮不新开独立 issue；直接作为 candidate lifecycle honesty 修复落到当前 sweep，并由已有 `candidate-acceptance-review-governance` 与 `milestone-planning-and-state-maintenance` 真源吸收。
- promoted_issue_path: `docs/B2-docs/ibm/candidate-acceptance-review-governance/issues/candidate-acceptance-review-governance.md`
- milestone: `M-20260306-workspace-routing-foundation`
- superseded_by:
  - `docs/B2-docs/ibm/candidate-acceptance-review-governance/issues/candidate-acceptance-review-governance.md`
  - `docs/B2-docs/ibm/milestone-planning-and-state-maintenance/issues/milestone-planning-and-state-maintenance.md`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
