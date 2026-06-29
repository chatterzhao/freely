# Freely Start After-Failure Recovery Handoff Race

## Why

`freely start` 在真实坏号上并没有稳定完成“失败后自动切到可用工具/号并继续工作”的合同。旧分析过度聚焦 `auth_failure` / `primary_rate_limit_exhausted` 等 failure label，但 2026-04-14 的新真实回放表明，同一坏号既可能被打成 `auth_failure`，也可能被打成 `primary_rate_limit_exhausted`；真正不稳定的是 start 失败后的恢复交接。

## Scope

只收敛这条问题：

- `freely start` 在真实坏号或坏工具上失败后，必须自动把恢复链跑完
- 不要求操作者手工补 `freely ensure-manager`
- 不引入新的后台空转、重复 supervisor、或 `freely stop` 后又被抢回来的竞态

不在本条预研里扩展：

- Codex probe `hi` 成功形状规则本身
- 旧 intake / continuity 噪音治理
- 泛化到所有 unrelated runtime bug

## Desired Contract

成功合同只有一条：

1. `freely start` 启动当前工具/当前号一次
2. 如果运行成功，继续做任务
3. 如果运行失败：
   - 先走当前工具的 slot 内循环
   - 当前工具没有更多 slot，或当前工具本来就没有 slot，可直接进入工具外循环
   - 再按工具优先级排除自己切到下一个工具，继续运行
4. 只有所有工具都不可用时，才允许进入 waiting / 停止
5. `freely stop` 必须能把整条 control-plane 干净停掉，不允许 stop 后又被恢复链反向拉起

## Success Criteria

1. 手工把 Codex 切到真实坏号，例如 `apikey-codex-a1016-1`
2. 执行真实 `freely start --project <project>`
3. 首轮失败后，不需要人工执行 `freely ensure-manager`
4. 系统会自动继续恢复，直到切到可用工具/号并重新运行
5. 同一次恢复过程中，不允许重复重启到刚失败的同一坏号
6. `freely stop --project <project>` 后，不允许再出现被 watchdog / recheck 抢回来的新 supervisor

## New Real Evidence

### 2026-04-14 real replay on `develop`

Environment:

- project: `/Users/zhaoyu/Downloads/code/my-freely/freely`
- current codex slot before start: `apikey-codex-a1016-1`
- current provider: `codex-a1016`

Observed sequence from `runtime-events.log` and real cycle log:

1. `freely start` 拉起 manager supervisor，进入 `ai_launch_begin`
2. 真实 `codex` 运行输出出现连续 `ERROR: Reconnecting...`
3. 随后出现真实 `403 Forbidden: 预扣费额度失败`
4. 这一次 replay 的 `ai_cycle_finished` 被写成：
   - `slot_switch_reason=primary_rate_limit_exhausted`
   - `exit_reason=primary_rate_limit_exhausted`
5. active supervisor 随后写出：
   - `event=supervisor_stopping reason=primary_rate_limit_exhausted`
6. 但在旧 supervisor cleanup 完成前，新的 `project_start_lock_acquired` / `supervisor_started` 又出现了
7. 后续再执行 `freely stop`，仍然观察到 stop 之后被再次拉起的新 supervisor

直接结论：

- 问题不是 failure label 本身
- 问题是 after-failure recovery handoff 没有串成原子交接

### What the code currently does

1. active supervisor 失败后只写：
   - `supervisor_stopping reason=<slot_switch_reason>`
   - 然后 `exit 0`
2. manager recovery 入口仍先依赖：
   - `tool_failure_scope_for_auto_recovery()`
   - `tool_failure_allows_same_tool_slot_recovery()`
   - `tool_failure_allows_cross_tool_auto_recovery()`
3. manager `ensure-manager` 侧在 `current_pid` 仍存在时，会优先沿着“current supervisor 还在 / idle supervisor restart”路径判断
4. `cleanup_supervisor()` 退出时又会：
   - 杀 interruption dispatcher
   - 杀 manager watchdog
   - 然后在 `desired_state=running` 时重新拉 `launch_interruption_dispatcher`
   - 再拉一次 `launch_manager_control_plane_recheck`

这说明当前实现把“失败 supervisor 退出”、“恢复链继续”、“operator stop 生效”混在了一组非原子动作里。

## Single Root Cause

最佳根因只保留这一条：

- **`freely start` 的 after-failure recovery handoff 没有被串成单一、串行、可判定的控制面交接；旧 supervisor、watchdog、one-shot recheck、以及 operator stop 会在同一时间窗里相互竞争，导致恢复链既可能重复启动同一坏号，也可能在 stop 后又被重新拉起。**

换句话说：

- 不是 “`auth_failure` 分类错了”
- 不是 “`primary_rate_limit_exhausted` 分类错了”
- 而是 “failure happened -> who owns recovery next -> when old supervisor is considered fully torn down” 这条 ownership contract 没有 materialize

## Implementation Direction

只允许围绕同一个根因修：

1. 把 after-failure recovery handoff 串行化
2. 明确 old supervisor 在什么条件下才算 fully torn down
3. 在 handoff 未完成前，不允许 watchdog / recheck 抢先按 stale state 拉起新的同工具/同坏号 supervisor
4. 在 operator stop 生效后，不允许任何 recovery owner 再次拉起新 supervisor
5. failure label 只用于观测和 slot/tool selection，不再决定 handoff 是否具备一致性

## Keep / Do Not Regress

这些现有设计是对的，不应乱改：

- 工具外循环 + slot 内循环的总体合同
- worker runtime 本地 same-tool slot recovery 的方向
- 真实日志/真实 `codex exec` 作为坏号 truth 的原则
- `tool_auto_switch_selected` / availability hint 这类恢复观测面

## Verification Plan

最小验证集：

1. 真实 `develop` 级坏号 replay 证据已收集完成
2. dedicated worktree 中补 manager after-failure handoff / stop race 修复
3. 回归 tests 至少覆盖：
   - active supervisor 失败后 control-plane 不会重复抢启同一坏号
   - `freely stop` 不会在 cleanup/recheck race 下被反向拉起
   - same-tool slot exhaustion 后能继续进入 cross-tool fallback
4. 真实环境再次执行：
   - 坏号 `a1016`
   - `freely start`
   - 观察其自动切到可用工具/号
   - `freely stop`
   - 确认彻底停净

## 2026-04-14 Implementation Result

本次实现只改同一条根因，不碰既有 tool/slot 选择顺序：

1. `cleanup_supervisor()` 先读取共享 runtime 真相，而不是只信当前进程内的 stale `DESIRED_RUNTIME_STATE_VALUE`
2. 若已经有 replacement supervisor 存活，旧 supervisor cleanup 直接退出，不再覆盖共享 state，也不再去杀/重拉共享 control-plane
3. manager 失败后的续跑执行者，从 one-shot `launch_manager_control_plane_recheck()` 改成持续 `launch_manager_watchdog()`

对应真源：

- `project_cleanup_runtime_intent()`
- `cleanup_supervisor()`

## 2026-04-14 Verification Result

已通过的回归：

1. `test-freely-start-watchdog-recovers-when-fallback-tool-appears-late`
   - 证明 `freely start` 在当前工具先失败、fallback 工具稍后才变可用时，watchdog 会持续接力直到恢复成功
2. `test-freely-ensure-manager-waits-for-supervisor-teardown-before-fallback`
3. `test-freely-auth-failure-keeps-control-plane-alive`
4. `test-freely-ensure-manager-codex-slot-first-then-cross-tool`
5. `test-freely-ensure-manager-single-slot-failure-falls-through-to-cross-tool`
6. `test-freely-runtime-handoff-local-stop`

真实环境 replay 结论分两层：

1. `a1016` 坏号真实 `freely start` 仍能复现首轮失败，且 failure label 仍可能落成 `auth_failure`
2. root `develop` 的 daemon/startup 面另外还有既存 blocker，会让 live-status 停在 `stalled_without_runtime`

所以这次 fix 已经验证修到：

- after-failure handoff race
- cleanup 使用 stale state 覆盖共享真相
- one-shot recheck 无法持续接力恢复

但 **root `develop` 的 daemon startup blocker 不是同一个 bug**，需要单独收敛，不能误记成“切号恢复仍未修好”。
