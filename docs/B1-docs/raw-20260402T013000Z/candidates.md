# Candidates - 20260402-0130--backup-time-rendering-and-storage-boundary

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260402T013000Z-A: legacy issue
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
- milestone: M-20260402T013000Z-A
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260402T013000Z-A/issue.md
- decision_reason: 当前 pre-brainstorm 保留的是跨 surface 的边界结论与行业参考。frontend Probe 显示层由 `I-20260308T124400Z-03` 吸收；runtime/status/CLI/watchdog 的 human-readable 显示层现已由 `I-20260402T030800Z-A` materialize。该 research 不再单独维持平行 owner，但继续作为两条收口链的共同依据。
- next_action: 新增显示时间 surface 继续遵守本 research 结论；若需要共享 formatter/materialization，优先吸收到 runtime-side owner 而不是再把 boundary 留在 absorbed-only 状态。
- revisit_trigger: 若后续出现需要按“用户自选时区”而不是“宿主系统时区”显示的产品面，或 backup schedule 进入业务时区调度能力，则需要从该 research 再次 materialize 新 owner。
- session_refs:
  - tool: codex
    session_id: current-thread
    jsonl_path: unavailable://codex-thread-only
    role: author
