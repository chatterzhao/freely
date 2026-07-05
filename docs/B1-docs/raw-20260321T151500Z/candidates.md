# Candidates - 20260321-1515--remote-branch-retirement-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260321T151500Z-A: legacy issue
- title: Remote branch retirement check for worktree governance
- problem: 当前 worktree 治理已经能做本地 worktree / 本地 branch 收口，但还没有把远程 feature branch 的删除或保留判断纳入 cleanup followthrough，导致治理闭环只完成一半。
- why_now: 本轮 fleet closure 已经暴露出这个缺口。若不把 remote branch disposition 正式收进 skill 和 runtime，后续每轮 promote 后都要手工补删远程分支。
- acceptance_hint:
  - 不新增平行大 skill，而是扩 `worktree-maintenance-governance` 和 `branch-management`
  - `cleanup-followthrough` 能处理 remote branch exists / merged / delete-failed / retained-with-reason
  - script test 覆盖 remote branch deleted 与 retained reason
  - 主管的治理真源显式要求 remote branch disposition
- priority: P0
- status: promoted
- decision_reason: 这是 worktree 治理闭环中的明确缺口，已经被真实 dogfooding 暴露，而且可通过小范围 skill + runtime + test 增量闭合。
- promoted_issue_path: `docs/B2-docs/ibm/remote-branch-retirement-governance/issues/remote-branch-retirement-governance.md`
- legacy_id_mapping: I-20260321T151500Z  # 历史遗留的 issue id
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
