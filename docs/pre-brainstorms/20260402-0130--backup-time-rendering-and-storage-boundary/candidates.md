# Candidates - 20260402-0130--backup-time-rendering-and-storage-boundary

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260402-0130-A
- title: Time Boundary for Backup Naming, Storage, and Display
- problem: 仓库内“备份时间”与“事件时间”的 naming truth、storage truth、display truth 未显式分层，导致用户显示面与恢复/治理面混用 UTC 与本地时间，且容易误把显示层本地化扩散到备份命名与机器真相。
- why_now: 当前 worktree 已经在 probe UI、`freely ai` 与 watchdog 输出里收口时间显示；如果不先冻结边界，这类 patch 会继续以局部修复的方式扩散，而不是沿一条稳定规则落地。
- acceptance_hint:
  - 明确备份命名继续使用 UTC / 稳定排序时间
  - 明确机器真相继续使用 epoch / ISO8601 / RFC3339
  - 明确所有用户显示时间默认按当前系统时区渲染，并显式带时区标签
  - 为新增 surface 提供统一 formatter / helper，而不是散落在各处重复处理
- priority: P0
- status: absorbed
- adoption_type: supporting_evidence
- milestone: M-20260308-frontend-probe-dogfooding-loop
- promoted_issue_path: docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md
- decision_reason: 当前发现首先由 frontend probe 用户显示面暴露，但同轮实现已经顺带收口了 `freely ai` 与 watchdog 的 human-readable 时间渲染。该 pre-brainstorm 只保留边界结论与行业参考，当前实现面不再单开平行 lifecycle。
- next_action: 若后续需要把这条边界提升为 repo-wide governance / capability，要为 runtime + frontend + future TUI 共用 formatter/materialization 开 dedicated owner issue；在那之前，新增显示时间 surface 继续遵守本 research 结论。
- revisit_trigger: 若后续出现需要按“用户自选时区”而不是“宿主系统时区”显示的产品面，或 backup schedule 进入业务时区调度能力，则需要重新 materialize。
- session_refs:
  - tool: codex
    session_id: current-thread
    jsonl_path: unavailable://codex-thread-only
    role: author
