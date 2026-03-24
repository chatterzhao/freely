# Progress: global-ai-account-watchdog-and-manager-bootstrap

- issue_id: `I-20260318-1630`
- title: Global AI account watchdog and manager bootstrap
- phase_state: `in_verification`
- runtime_state: `closed_for_this_batch`
- branch: `feature/global-watchdog-earliest-reset-sleep-revive-20260323`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260323-feature-global-watchdog-earliest-reset-sleep-revive`
- issue_path: `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://current-manual-codex-thread-id-not-exposed", role: "continuation-worker"}

## Summary

- 本轮 continuation 已吸收 delegated handoff 中的五点 contract，并确认对应实现已经落在当前分支祖先：
  - all accounts unusable 时选择最早 reset 账号
  - wait 采用 `reset_at + 60s` 等价 buffer 契约，可由 watchdog buffer 环境变量调节
  - wait 期间周期性真实 reprobe，任一已保存账号恢复可用即可提前唤醒
  - `ensure-manager.pid` 只代表 live watchdog，stale pid 会被覆盖并在退出时清理
  - cooldown elapsed 后先 reprobe/reselect，再决定 manager relaunch
- 当前轮次主要补 canonical writeback，纠正 issue / milestone / code-review 与实际 continuation 状态之间的漂移。
- 2026-03-24 fresh session 因上一轮 `context_compacted` 交接被重新拉起后，先按 continuity guard 重跑聚焦验证，再继续保持当前批次 `in_verification` / manager merge review 待处理结论。

## Verification

- `git status --short --branch`
- `git rev-list --left-right --count develop...HEAD`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-earliest-reset-wait-revive`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager`
- `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog`
- `bash docs/system/workspace/scripts/tests/test-watchdog-control-plane-skills`
- `./bin/governance-check`

### Latest rerun

- 2026-03-24 02:25:39 PDT fresh session rerun:
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-earliest-reset-wait-revive` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog` pass
  - `bash docs/system/workspace/scripts/tests/test-watchdog-control-plane-skills` pass
  - `./bin/governance-check` pass with legacy pre-brainstorm naming warnings only

## Next Action

- 当前批次已处于 manager merge review 前的 verification closeout。
- 若上述聚焦验证继续通过，下一步由 manager 决定是否 promote 当前 branch；worker 不直接 merge 到 `develop`。

## Revisit Trigger

- 任一 watchdog wait/reprobe 或 stale `ensure-manager.pid` 回归失败
- manager review 发现当前 doc/code/test 证据仍不一致
- `develop` 真实环境在 replay 后暴露新的 outer-watchdog/productization 缺口
