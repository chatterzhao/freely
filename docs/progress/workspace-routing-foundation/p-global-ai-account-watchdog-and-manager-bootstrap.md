# Progress: global-ai-account-watchdog-and-manager-bootstrap

- issue_id: `I-20260318-1630`
- title: Global AI account watchdog and manager bootstrap
- phase_state: `in_verification`
- runtime_state: `in_verification`
- branch: `feature/watchdog-switch-stability-and-probe-freeze-20260326`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260326-feature-watchdog-switch-stability-and-probe-freeze`
- issue_path: `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://current-manual-codex-thread-id-not-exposed", role: "continuation-worker"}

## Summary

- 2026-03-25 新 pre-brainstorm `C-20260325-0525-A` 已完成首跳判断，并作为 supporting evidence 被本 issue 吸收：
  - 当前恢复 contract 的主问题不再是“slot-first cooldown 写回是否对齐”，而是 cooldown 本身是否还应继续充当控制面真相
  - 当前判断：`rate limit`、`deactivated_workspace`、auth failure / invalid auth file、slot probe failure，都应统一进入 failure-driven full slot sweep
  - `all slots unavailable` 时允许保留 earliest-reset 作为 debug / 排序提示，但恢复主路径应基于低频真实 reprobe，而不是继续依赖 cooldown ledger
  - 这意味着本 issue 的下一跳不是直接 merge review，而是先在同 issue family 内重开 doc-loop / dev-loop，完成 contract rewrite
- 2026-03-25 当前 worktree 已完成这一轮 doc-loop + dev-loop + focused verification：
  - `availability-watchdog.sh` 不再以 cooldown/earliest-reset 作为主恢复 gate；`ensure_codex_slot_ready_for_manager()` 现改为 current-slot probe + full saved-slot sweep
  - `probe_all_codex_slots_and_update_cooldown()` 在 sweep 失败时恢复原 auth/active-slot，不再把最后一个失败 slot 留在真实 Codex 工作位；找到 usable slot 时会在返回前把 active slot 推回该 usable slot
  - `ai-cli switch codex` 自动模式现在只会切到真实 probe 成功的 usable slot；`all_unavailable` 仅返回 debug hint，不再把 earliest-reset slot 强行切进真实工作位
  - focused regressions 已重写为 slot-sweep-first contract：
    - `test-freely-ai-account-switch`
    - `test-freely-ensure-manager`
    - `test-freely-ensure-manager-earliest-reset-wait-revive`
  - 这一轮验证已通过，当前保持 `in_verification`，等待后续 code review / manager merge judgement
- 2026-03-26 canonical develop replay 暴露出同族控制面缺口：
  - 最新 delegated continuations 已进入 `.freely/intake/` 的 `delegated` 状态
  - 但 canonical runtime 因 manager `auth_failure` 掉到 `stalled_without_runtime`，现场没有任何存活的 `ensure-manager --watch` / interruption dispatcher 继续消化这些 intake
  - 当前判断：不是新 issue，而是本 issue 的 script-owned recovery contract 仍缺一条 detached control-plane survival gate
- 2026-03-26 当前 continuation 已补上这条控制面恢复：
  - `runtime/freely` 里的 `launch_manager_supervisor()`、`launch_interruption_dispatcher()`、`launch_manager_watchdog()` 已改为 `nohup` detached launch，避免父 supervisor 因 `auth_failure` 退出时把控制面一起带掉
  - 新增 focused regression `test-freely-auth-failure-keeps-control-plane-alive`
  - 继续复跑 `test-freely-manager-watchdog-live-during-active-ai` 与 `test-freely-rate-limit-defers-to-watchdog`，证明 detached launch 没有破坏既有 watchdog 生命周期或 rate-limit 委派路径
- 2026-03-26 紧接的 canonical replay 又暴露出两个 same-family 尾巴：
  - `cmd_start()` 启动 interruption dispatcher 后没有等待 ready，因此 fresh start 允许带着“半个控制面”继续向下执行
  - `live-status` / `activity_state` 不把 `ensure-manager --watch` 算入 control-plane，watchdog-only 现场会被误报成 `stalled_without_runtime`
- 2026-03-26 当前 continuation 已补上这两个 acceptance gap：
  - `cmd_start()` 现在在 `launch_interruption_dispatcher()` 后强制 `ensure_interruption_dispatcher_ready_or_fail()`
  - `live_status_activity_state_for_project()` 与 `cmd_live_status()` 现在都会 surface `role=manager_watchdog`
  - 新增 focused regressions：
    - `test-freely-start-requires-interruption-dispatcher-ready`
    - `test-freely-live-status-watchdog-survival`
  - 现有 `test-freely-live-status` 也已扩展为断言 watchdog surface
- 2026-03-26 当前现场又补出一条 switch observability 缺口：
  - `bin/ai switch codex` 的单 slot probe 现在默认只给 `CODEX_PROBE_TIMEOUT=15` 秒；超时后 watchdog 只回 `timeout`，现场无法区分网络/代理慢、CLI 卡住，还是 `402 deactivated_workspace` 已经返回但被 timeout 截断
  - 当前 continuation 已把 timeout/deactivated-workspace probe output 落到 `.freely/run/codex-probe-artifacts/`，并新增 focused regression `test-freely-codex-probe-timeout-artifact`
  - 同轮 verification 已补 `20260326-slot-probe-timeout-observability-verification.md`，明确本轮只把 timeout observability 与 probe lock contract 作为 merge 证据，不把旧工位里未收干净的 `test-freely-ensure-manager` 漂移误算为本次回归
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
  - 2026-03-24 slot-only cooldown writeback：
    - `ensure_codex_slot_ready_for_manager` 现在只认 `whoami.slot` 作为 cooldown identity，`whoami.account` 仅保留展示用途
    - `select_any_available_codex_slot` 只排除当前精确 slot，不再做同 family exclusion，避免把同邮箱的 `-x` 兄弟 slot 误伤
    - 已验证 `ai-cli` 的 `login`/`switch` 入口遵守显式 suffixed slot contract，不再生成或消费无后缀目录
    - 新的 focused regression `docs/system/workspace/scripts/tests/test-freely-ensure-manager-slot-alias-cooldown` 覆盖了 slot selector / manager bootstrap 路径以及 slot-only cooldown identity
  - 2026-03-25 develop live investigation 追加了新的生产现场证据：
    - canonical `whoami.slot` 当前为 `worahe3976@outlook-com`
    - canonical `ai list` 共返回 15 个保存 slot
    - canonical `.freely/run/codex-slot-cooldowns.tsv` 中有 6 个保存 slot 缺失 cooldown entry：`worahe3976@outlook-com`、`worahe3976@outlook-com-3`、`worahe3977@outlook-com-1`、`worahe3978@outlook-com-1`、`worahe3978@outlook-com-2`、`worahe3978@outlook-com-4`
    - 同时还残留 7 条不再对应保存 slot 的旧 identity entry，均为无后缀旧命名
    - 因此当前 P0 不是“切号前不等待旧动作结束”，而是 watchdog cooldown truth 与 `.ai-auth` slot reality 漂移，导致 limit 后无法稳定收敛到 `all_slots_cooling_down` / earliest-reset hold
  - 同轮还补了一条测试 tightening：
    - `test-freely-rate-limit-defers-to-watchdog` 与 `test-freely-rate-limit-log-defers-to-watchdog` 现在都直接断言 cooldown ledger 写入的是 suffixed slot key `limited@example-com-1`
    - 这把 `runtime/freely` supervisor 在 rate-limit 退出后的 slot-first 写回契约也锁住了，不再只依赖 `ensure-manager` focused regression 间接覆盖
  - 当前 continuation 继续补齐了两个 review 暴露出的缺口：
    - `ensure_manager_once()` 的 idle-manager unavailable 检查现也改成走 slot-first cooldown identity，不再用 `codex_current_account`
    - 当 `whoami.slot` 临时缺失时，cooldown identity 会回退到 `~/.codex/active-slot`，避免 rate-limit 记录直接丢失

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
- `./bin/ai --quiet --format json whoami codex`
- `./bin/ai --quiet --format json list`
- compare canonical `.freely/run/codex-slot-cooldowns.tsv` entries against saved slot inventory
- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `bash docs/system/workspace/scripts/tests/test-freely-auth-failure-keeps-control-plane-alive`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-watchdog-live-during-active-ai`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
- `bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-timeout-artifact`
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
- 2026-03-25 canonical develop live check:
  - `wait_for_codex_slot_switch_idle()` 与 shared switch lock 仍在真源里，说明“切号前等待旧切号/旧 probe 结束” contract 还在
  - 但 live cooldown 账本与保存 slot 清单发生漂移，slot-first continuation 仍未完全反映到 canonical state truth
  - 当前判断：同族 continuation 需要继续围绕 slot inventory / cooldown ledger reconcile 收口，而不是新开独立 process-lifecycle candidate
  - 同轮 focused regression 重跑：
    - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog` pass，且显式断言 slot key cooldown writeback
    - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-log-defers-to-watchdog` pass，且显式断言 textual usage-limit fallback 也写入 slot key
    - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-slot-alias-cooldown` pass
    - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-idle-unavailable-slot-restart` pass，锁住 idle supervisor unavailable branch 的 slot-first restart 判定
    - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-cooldown-falls-back-to-active-slot` pass，锁住 `whoami.slot` 缺失时的 active-slot fallback
- 2026-03-25 06:05 PDT current slot-sweep-first continuation rerun:
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch` pass，且显式验证：
    - 有 usable slot 时才切换
    - `all_unavailable` 时不再切到 earliest-reset slot
    - probe 失败后会恢复原 auth，而不是把无效 slot 留在真实 Codex 工作位
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager` pass，且显式验证 manager bootstrap 之前会先 full sweep 并 promote 真实 usable slot
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-earliest-reset-wait-revive` pass，且显式验证 all-slots-unavailable 后走低频真实 reprobe，而不是 cooldown-driven sleep-until-reset
  - `./bin/governance-check` pass，只有 10 条 legacy pre-brainstorm naming warning
- 2026-03-26 auth-failure control-plane continuation rerun:
  - `bash -n docs/system/workspace/scripts/runtime/freely` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-auth-failure-keeps-control-plane-alive` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-watchdog-live-during-active-ai` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog` pass
  - `./bin/governance-check` pass，只有 10 条 legacy pre-brainstorm naming warning
- 2026-03-26 live-status / dispatcher-ready continuation rerun:
  - `bash -n docs/system/workspace/scripts/runtime/freely` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-auth-failure-keeps-control-plane-alive` pass
- 2026-03-26 slot probe timeout observability continuation rerun:
  - `bash -n docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-timeout-artifact` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-defers-during-account-switch` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch` pass
  - `./bin/governance-check` pass with 10 legacy pre-brainstorm naming warnings only

## Next Action

- 当前批次又补上了 `auth_failure` 后 detached control-plane 存活契约；下一步进入同 issue family 的 commit / merge judgement，并在 develop replay 中确认 canonical runtime 不再掉到 `stalled_without_runtime`。

## Revisit Trigger

- 任一 watchdog wait/reprobe 或 stale `ensure-manager.pid` 回归失败
- manager review 发现当前 doc/code/test 证据仍不一致
- `develop` 真实环境在 replay 后暴露新的 outer-watchdog/productization 缺口
- live replay 再次证明 cooldown 仍在主恢复路径上制造错误等待或错误可用性判断
