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
- 本轮继续吸收 fresh-session verification 新暴露出的收口缺口：
  - `test-freely-rate-limit-defers-to-watchdog` 的整秒计时断言存在秒边界抖动，已改成 monotonic 毫秒阈值
  - `ensure-manager` 与 earliest-reset 回归已补 manager bootstrap handoff artifact 断言，锁住 `trigger/account/reason/next_action` 契约
  - 手工或自动账号切换 sweep 期间，watchdog/ensure-manager 之前仍可能并发触发 `whoami/list/switch/codex exec`；当前已补 shared switch lock，让 watchdog 在 sweep 结束前延迟 probe/bootstrap，避免误把切号中间态当成新的限流/授权恢复信号
  - 当前 continuation 又补了一轮锁边界：
    - `whoami/list` 读路径也受 shared switch lock 保护，不再只靠 `switch`/bootstrap 本身等待
    - watchdog `codex exec` probe 现在会持有 shared lock 直到 probe 结束，避免 manual sweep 在 wait-return 后立刻插入
    - focused tests 已覆盖 `ensure-manager` defer 期间不触发 `whoami/list`，以及 probe 自身的 defer + serialization

## Verification

- `git status --short --branch`
- `git rev-list --left-right --count develop...HEAD`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-earliest-reset-wait-revive`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager`
- `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog`
- `bash docs/system/workspace/scripts/tests/test-watchdog-control-plane-skills`
- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-serialization`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-defers-during-account-switch`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-defers-during-account-switch`

### Latest rerun

- 2026-03-24 02:25:39 PDT fresh session rerun:
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-earliest-reset-wait-revive` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog` pass
  - `bash docs/system/workspace/scripts/tests/test-watchdog-control-plane-skills` pass
  - `./bin/governance-check` pass with legacy pre-brainstorm naming warnings only
- 2026-03-24 current continuation rerun:
  - 首轮 `test-freely-rate-limit-defers-to-watchdog` 曾再次命中一次 `4s` 秒边界误报，确认问题出在测试计时口径而非 runtime 回退到本地睡眠
  - 修复后重复验证：
    - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-earliest-reset-wait-revive` pass，且同时验证 wait/reprobe、stale pid cleanup、manager bootstrap handoff
    - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager` pass，且同时验证可用账号切换与 manager bootstrap handoff
    - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog` 连跑 5 次全部 pass，使用 monotonic 毫秒阈值避免秒边界抖动
    - `./bin/governance-check` pass with legacy pre-brainstorm naming warnings only

## Next Action

- 当前批次已处于 manager merge review 前的 verification closeout。
- 若上述聚焦验证在补丁后继续通过，下一步由 manager 决定是否 promote 当前 branch；worker 不直接 merge 到 `develop`。

## Revisit Trigger

- 任一 watchdog wait/reprobe 或 stale `ensure-manager.pid` 回归失败
- manager review 发现当前 doc/code/test 证据仍不一致
- `develop` 真实环境在 replay 后暴露新的 outer-watchdog/productization 缺口
