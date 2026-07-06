# Issue: watchdog-restart-storm-and-process-churn-governance

- issue_id: `I-20260324-0405`
- title: Watchdog restart-storm and process-churn governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `watchdog-restart-storm-and-process-churn-governance`
- issue-name: `watchdog-restart-storm-and-process-churn-governance`
- verification_artifact_dir: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260324-0405/code-reviews
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260324T041500Z/candidates.md#c-20260324-0405-a`
- source_brainstorm: `docs/B1-docs/raw-20260324T041500Z/brainstorms.md`
- source_candidates: `docs/B1-docs/raw-20260324T041500Z/candidates.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/ibm/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `docs/B2-docs/ibm/manager-watchdog-trigger-and-drift-reconcile-governance/issues/manager-watchdog-trigger-and-drift-reconcile-governance.md`
  - `docs/B2-docs/runtime/watchdog-live-status-surface-and-manager-supervision/issues/watchdog-live-status-surface-and-manager-supervision.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

当前 active truth 已明确：

- watchdog 可以观察 restart storm / process churn
- watchdog 只暴露 signal
- dead-loop / thrash 是否成立，必须由主管在 `auto-loop` 裁决

但 runtime 代码仍只覆盖 stall-based recovery，没有：

- 短窗口 restart/relaunch 计数
- process churn 峰值 signal
- signal 写回 `session-state.env`
- signal 命中后的 manager escalation 路径
- `live-status` / `fleet-status` 对这类 signal 的稳定暴露

这会让系统继续把 dead-loop 伪装成“努力恢复中”。

## Scope

1. 在 runtime/watchdog 中引入 restart storm / process churn 的短窗口 signal。
2. 把原始 signal 写入 `session-state.env`，而不是塞进 `workcell-state.env`。
3. 让 `live-status` / `fleet-status` 暴露 signal 作为派生观察面。
4. 明确 signal 命中后 watchdog 停止盲重启，进入低频观察并触发 manager escalation。
5. 明确 manager continuity 只携带 signal ref 与治理裁决，不重复原始计数。
6. 明确 signal 与现有 stall recovery 的并存规则与默认阈值。

## Acceptance

- runtime 有结构化的 restart storm / process churn signal，最小包含：
  - `RESTART_STORM_WINDOW_SECS`
  - `RESTART_STORM_COUNT`
  - `PROCESS_CHURN_PEAK`
  - `LAST_RESTART_STORM_SIGNAL_AT`
  - `LAST_RESTART_STORM_SIGNAL_REASON`
  - `LAST_RESTART_STORM_ESCALATED_AT`
  - `LAST_RESTART_STORM_ESCALATION_TARGET`
- 原始 signal 只写 `session-state.env`，`workcell-state.env` 不镜像该类计数。
- stall 与 restart storm 不混判：
  - stall 处理 live-but-not-advancing AI
  - restart storm 处理短窗口 exit/relaunch churn
- signal 命中后 watchdog 不继续 blind relaunch，而是进入低频观察并等待 manager judgement。
- manager continuity 只写 signal ref 与 `ownership / restart_point / next_action`，不重复原始计数。
- `live-status` / `fleet-status` 能稳定暴露该 signal，便于主管巡检与人工插话。

## Ready For Dev

当前 IBM 已冻结：

1. signal 真相面：`session-state.env`
2. `workcell-state.env` 不镜像 churn 计数
3. watchdog 命中 signal 后进入低频观察
4. manager continuity 只携带 signal ref 与 followthrough judgement
5. stall 与 restart storm 的判定面分离
6. 默认阈值：
   - `RESTART_STORM_WINDOW_SECS=30`
   - `RESTART_STORM_COUNT=4`
   - `PROCESS_CHURN_PEAK=3`

## Implementation References

- `docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/brainstorms/b-watchdog-restart-storm-and-process-churn-governance.md`
- `docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/prd.md`
- `docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260324-0405/verification/pre-tests.md`
- `docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/tasks.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-restart-storm-defers-blind-relaunch`
- `docs/system/workspace/scripts/tests/test-freely-restart-storm-status-surface`
- `docs/progress/workspace-routing-foundation/p-watchdog-restart-storm-and-process-churn-governance.md`
- `docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/code-reviews/20260324-watchdog-restart-storm-and-process-churn-verification.md`

## Verification Summary

- runtime 现在会在短窗口内记录 restart storm / process churn，原始 signal 只写入 `session-state.env`。
- `workcell-state.env` 继续只承载当前 workcell 生命周期，不镜像 restart storm / process churn 计数。
- signal 命中后，watchdog 不再盲目快速重拉 AI，而是写出 `manager_bootstrap_handoff` 并进入低频观察窗口，等待 manager `auto-loop` 裁决。
- `live-status` / `fleet-status` 已能稳定暴露 restart storm 摘要，便于主管巡检和人工插话。
- 本次 issue 的 IBM `pre-tests.md` 已逐项满足；issue 完成，但 worktree 仍需后续 merge / cleanup / retirement 链闭合后才可删除。
