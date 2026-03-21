# Candidates - 20260320-1745--dirty-worktree-governance-redesign

## Context
- Source brainstorm: ./brainstorms.md
- Status: candidate

## Candidates

### C-20260320-1745-A
- title: Dirty worktree gate redesign for multi-worktree autonomy
- problem: 当前 `dirty fleet` 被当成全局二元门禁，导致 unrelated dirty / busy worktree 也会阻断本可安全执行的 `audit / merge_prep / cleanup-followthrough`。在多 AI / 多 worktree / subagent 并行场景下，这会把“系统正在工作”误判成“系统异常”。
- why_now: Freely 已开始用自己开发自己，插话 runtime 已真实暴露出这类误伤；如果不拆分 dirty gate，未来并行度一提高，cleanup 与 worktree 维护会频繁卡死。
- acceptance_hint:
  - 将 dirty gate 重构成 `target_clean / fleet_busy / fleet_dirty_unrelated`
  - merge / promote / release 继续保持强门禁
  - `audit / merge_prep / retirement_handoff / cleanup-followthrough` 改成 finer-grained handling
  - cleanup runtime 至少能在 unrelated dirty tree 存在时继续清理安全 target，并保留 busy/dirty target 的 retained evidence
  - 若引入 bypass，只能是 `allow-dirty-unrelated / skip-busy-worktree / scope` 这类细粒度能力
- priority: P0
- status: candidate
- decision_reason: 这是 Freely 进入多工位自治后的真实治理缺口，不是抽象优化。当前应先把问题空间和最小修复边界收口，再决定是否 materialize 成更大的治理 issue。
- promoted_issue_path: pending://issue-materialization
- next_action: 保持 pre-brainstorm candidate；若本轮最小 runtime 修复稳定，再 materialize 正式 issue
- revisit_trigger: 再次出现 unrelated dirty tree 阻断 cleanup / audit / merge-prep，或需要为 `wt-status-all` / cleanup 增加显式绕过语义时
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
