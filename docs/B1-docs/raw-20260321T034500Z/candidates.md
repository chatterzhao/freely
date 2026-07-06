# Candidates - 20260321-0345--manager-reactivation-and-fleet-patrol

## Context
- Source brainstorm: ./brainstorms.md
- Status: promoted

## Candidates

### C-20260321T034500Z-A: legacy issue
- title: Manager reactivation and fleet patrol governance
- problem: Freely 当前已经能通过 supervisor/watchdog 拉起主管，也能提供 `live-status` / `fleet-status` 等观察面，但还缺一条明确的主管 patrol 能力，确保主管定期重新激活后主动检查“哪些 phase / issue / worktree 当前没有 worker 推进、哪些已经完成却没收口”，并据此委派 worker、请求 runtime recovery、推动 merge 或 cleanup。
- why_now: 现在 worktree 治理已经清楚表明，停滞不只来自进程死亡，也来自“生命周期某个点位没人管”。如果不把主管 patrol 明确化，Freely 很容易只做到保活，而做不到持续监督和主动补派。
- acceptance_hint:
  - 明确主管 patrol 的输入顺序：`live-status -> fleet-status -> milestone/issue/progress/recovery`
  - 明确 stalled / orphaned phase 的最小判定
  - 明确发现后如何输出 `ownership + restart_point + next_action`
  - 明确 issue 完成但 worktree 未收口也属于 patrol 发现范围
  - 最终产物应落为主管监督协议增强，而不是一次性聊天建议
- priority: P0
- status: promoted
- decision_reason: 这是 Freely 从“manager process alive”走向“manager genuinely supervising the fleet”的关键一步；不先研究清楚，后续自动监督仍会停在 runtime 层。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260307-1201I-20260321T034500Z-A/issue.md
- legacy_id_mapping: I-20260321T034500Z  # 历史遗留的 issue id
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
