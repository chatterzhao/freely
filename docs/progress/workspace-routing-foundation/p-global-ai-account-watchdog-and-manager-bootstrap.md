# Progress: global-ai-account-watchdog-and-manager-bootstrap

- issue_id: `I-20260318-1630`
- title: Global AI account watchdog and manager bootstrap
- phase_state: `in_verification`
- runtime_state: `closed_for_this_batch`
- branch: `feature/watchdog-family-replay-20260325`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260325-feature-watchdog-family-replay`
- issue_path: `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://current-manual-codex-thread-id-not-exposed", role: "continuation-worker"}

## Summary

- 2026-03-25 新 pre-brainstorm `C-20260325-0921-A` 已完成首跳判断，并作为 supporting evidence 被本 issue 吸收：
  - 当前恢复 contract 的主问题不再只是“slot-sweep-first 是否建立”，而是 probe 窗口是否真正独占、是否仍残留 cooldown 逻辑、以及 all-unavailable 时是否还会错误拉起 AI
  - 当前判断：`cooldown` 应彻底退出恢复逻辑；slot sweep / reprobe 期间必须阻塞 AI launch；all-unavailable 时 watchdog 保持活着，但 manager / worker 保持 down，直到 inventory 变化或低频 probe 找到 usable slot
  - 这意味着本 issue 当前不进入 merge judgement，而是先回到 doc-loop + dev-loop 完成 strict probe-gating rewrite
- 2026-03-25 当前 worktree 正在做这一轮 stricter rewrite：
  - 已先更新 pre-brainstorm、issue、pre-tests、tasks、progress、milestones，把 no-launch probe-gating 和 wake-only recovery 固定为 acceptance contract
  - 已完成 `availability-watchdog.sh`、`runtime/freely`、`ai-cli` 和 focused regressions 的收口，去掉 cooldown 逻辑残留并补上 all-unavailable / inventory-change wake 验证
- 2026-03-25 live 调查又暴露出一条更底层的 identity 漂移，当前已吸收到同一 issue：
  - `./bin/ai switch` / `whoami` 现场出现 `Current slot = worahe3977@outlook-com-2`，但 `Current account = worahe3976@outlook.com`
  - 逐个解码 `~/.ai-auth/codex-*/auth.json` 后确认，这不是 runtime 读错 active slot，而是 slot 目录本身可以承载与目录名不同的授权邮箱；同一个邮箱/`account_id` 也可出现在多个 slot
  - 结论是 slot 仍然正确，错的是 CLI 把授权邮箱元数据冒充成“当前身份”；当前批次已把 `ai-cli` 的 `whoami`/`switch`/`status`/`save`/`login` contract 改回 slot-first，邮箱仅保留为 `auth_email` 元数据
- 本轮 continuation 已吸收 delegated handoff 中的五点 contract，并确认对应实现已经落在当前分支祖先：
  - all accounts unusable 时选择最早 reset 账号
  - wait 采用 `reset_at + 60s` 等价 buffer 契约，可由 watchdog buffer 环境变量调节
  - wait 期间周期性真实 reprobe，任一已保存账号恢复可用即可提前唤醒
  - `ensure-manager.pid` 只代表 live watchdog，stale pid 会被覆盖并在退出时清理
  - cooldown elapsed 后先 reprobe/reselect，再决定 manager relaunch
- 当前轮次已经补齐 canonical writeback，纠正 issue / milestone / code-review 与实际 continuation 状态之间的漂移。
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
    - `ensure_codex_slot_ready_for_manager` 现在只认 `whoami.slot` 作为 cooldown identity；授权邮箱只允许作为 `auth_email` 元数据存在
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
- `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-whoami-prefers-slot-identity`

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
- 2026-03-25 current slot-identity correction rerun:
  - `bash -n docs/system/workspace/scripts/runtime/ai-cli` pass
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool` pass
  - `bash docs/system/workspace/scripts/tests/test-ai-cli-whoami-prefers-slot-identity` pass
  - `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch` pass

## Next Action

- 当前批次的 strict probe-gating contract replay 与 focused verification 已完成。
- no-launch gate、all-unavailable hold、inventory-change wake evidence 已补齐；当前 worktree 已进入 manager merge judgement / develop replay followthrough 前的 review-ready 状态，但仍保持 `in_verification`，等待 manager 吸收。

## 2026-03-25 Source Lane Retirement Audit

- Re-audited the remaining same-family source/supporting worktrees against this replay owner:
  - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260325-feature-manager-runtime-process-churn-state-reconcile`
  - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260325-feature-interruption-handler-account-recovery`
  - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260325-feature-watchdog-family-integration`
  - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260325-feature-watchdog-strict-slot-probe-gating`
  - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260325-feature-watchdog-slot-sweep-without-cooldown-governance`
- Their remaining local-only deltas are not missing desired capability in the replay owner:
  - `manager-runtime-process-churn-state-reconcile` still carries one local-only continuation commit (`d2ef386`), but this replay owner already preserves its broadened auth-failure detection plus the skip-launch/no-slot-ready regressions in canonical slot-first form
  - `interruption-handler-account-recovery` still points the interruption handler at the older account-ready path instead of the current slot-first contract
  - `watchdog-family-integration` still carries older availability-state / logging behavior that predates the current replay owner
  - `watchdog-strict-slot-probe-gating` still drops the broadened auth-failure detection and the no-launch test coverage now required by this replay owner
  - `watchdog-slot-sweep-without-cooldown-governance` is already an absorbed supporting-evidence lane; its remaining local commit is only retirement writeback, not a new owner path
- This round therefore treats all five branches as superseded local source/supporting lanes whose remaining unique commits should not be replayed onto the canonical owner.

## Revisit Trigger

- 任一 watchdog wait/reprobe 或 stale `ensure-manager.pid` 回归失败
- manager review 发现当前 doc/code/test 证据仍不一致
- `develop` 真实环境在 replay 后暴露新的 outer-watchdog/productization 缺口
- live replay 再次证明 cooldown 仍在主恢复路径上制造错误等待或错误可用性判断
