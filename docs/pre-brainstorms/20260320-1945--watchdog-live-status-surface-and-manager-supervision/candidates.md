# Candidates - 20260320-1945--watchdog-live-status-surface-and-manager-supervision

## Context
- Source brainstorm: ./brainstorms.md
- Status: candidate

## Candidates

### C-20260320-1945-A
- title: Watchdog live status surface and manager supervision contract
- problem: Freely 当前只有 `baseline-status / fleet-status / prompt / continuity / jsonl / ps` 这些碎片化证据，没有统一 current-state surface。结果就是后台进程仍在跑时，主管和用户仍无法快速判断“谁在跑、在做什么、是否停在 handoff”。
- why_now: 这是 Freely 用自己开发自己时已经真实暴露的控制面缺口；若不先做最小 live status，后续多 AI / 多 worktree / subagent 并行时，全局监督会继续退化成人工 grep。
- acceptance_hint:
  - 新增 `freely live-status --project <path>` 当前态视图
  - 只展示活跃 pid，不展示已退出 pid
  - 至少输出 `supervisor / interruption dispatcher / ai`、提示词截取、continuity 摘要与 `jsonl/cycle_log` 深挖入口
  - `manager-agent` 与 `multi-worktree-supervision` 明确把它当作主管每轮监督入口
  - 首跳 prompt 明确要求主管轮次优先读取该接口
- priority: P0
- status: promoted
- decision_reason: 当前边界已经够清楚，不需要继续停留在纯预研；应直接 materialize 成 issue 并实现最小 CLI 面。
- promoted_issue_path: `docs/epics/workspace-routing-foundation/watchdog-live-status-surface-and-manager-supervision/issues/watchdog-live-status-surface-and-manager-supervision.md`
- next_action: materialize issue，并落最小 CLI + doc + test；后续是否扩成更细的 stall detection 再另开 issue
- revisit_trigger: 若后续需要 JSON 输出、长期 watch 模式、或更强 stall detection / event stream，再从同一预研线继续扩
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
