# 预研头脑风暴：start-restart-control-plane-semantics

## 状态更新

- 2026-03-28 当前 pre-brainstorm 已完成它的职责：`C-20260327-2006-A` 已 materialize 为 `I-20260327-2006-A` 与 `I-20260327-2006-B` 两个紧邻 issue。
- 当前 canonical route 不再是 `pre_brainstorm`，而是：
  - `I-20260327-2006-A` -> `in_verification`
  - `I-20260327-2006-B` -> downstream `done_ibm`
- 2026-03-29 23:25 PDT fresh session 首跳再次复核后，当前 worker lane 的 runtime 状态虽然已变成 `last_ai_state=down`、`last_exit_reason=ai_exit_rc_1`，但 branch-local route 仍未变化：`I-20260327-2006-A` 继续等待 manager-owned `completion_verification`，`I-20260327-2006-B` 继续保持 downstream `done_ibm`。
- 2026-03-29 22:47 PDT 再次按 `AGENTS.md -> constitution-guard -> laws-enforcer -> lead-agent -> context-source-skill -> live-status` 复核后，当前 active truth 仍是 `I-20260327-2006-A` 等待 manager-owned `completion_verification`。旧的 delegated IBM relaunch prompts 继续只算 supervision history，不再代表当前 lane route。
- 下文保留的是 promotion 前的研究证据与边界推导，用于追溯为什么最初不能直接跳过 pre-brainstorm / IBM；它不再代表当前 active route。

## 背景

当前 delegated continuation 要求收敛 `freely start` / `freely stop` / `freely restart` 与显式 global/shared control-plane 的边界，但现有 canonical truth 还没有把这组命令语义冻结成独立 lifecycle。

已确认的同族真相：

- `I-20260318-1630` 已完成，并明确只覆盖 global AI account watchdog、manager bootstrap、slot sweep、launch gate 与 detached watchdog survival；不得把它重新打开。
- `docs/system/workspace/scripts/runtime/freely` 已有 project-scoped pid 归属校验：
  - `valid_supervisor_pid_for_project`
  - `valid_ensure_manager_watchdog_pid_for_project`
  - `valid_interruption_dispatcher_pid_for_project`
  - `valid_ai_pid_for_project`
- `cmd_stop()` 当前只停当前 `--project` 归属下的 `ai.pid`、`supervisor.pid`、`interruption-dispatch.pid`、`ensure-manager` watchdog pid；它不会按全局进程名盲杀。
- `cmd_start()` 当前会启动 project-scoped supervisor，并在需要时启动 project-scoped interruption dispatcher 与 manager watchdog；但它没有冻结 `restart` / `start --force` 语义，也没有显式区分“安全的 project-scope force”与“危险的 global reset”。
- availability watchdog 的 shared identity 与持久状态明显不是 project-scoped：
  - `~/.codex/active-slot`
  - `$HOME/.codex/slot-switch.lock`
  - per-project `.freely/run/codex-availability-state.env` / cache 只是在 shared slot reality 基础上的 project consumption surface
- 与现有 `C-20260323-1435-A` 的边界也已足够明确：
  - `interactive-init-bootstrap-and-force-governance` 讨论的是 `freely init` 的 bootstrap / skip / force contract
  - 本条讨论的是 runtime lifecycle/control-plane command family 的 blast radius、owner taxonomy 与 restart semantics
  - 因此两者同属 force 语义家族，但不是同一个 issue owner

## 当前问题

Freely 现在已经有部分实现事实，但语义面仍不完整：

1. `freely start` 当前更像“如果本工位还没在运行，就启动 project runtime/control-plane”，但没有明确 stale pid、idle supervisor、partial control-plane 时是 attach、repair 还是 fail-fast。
2. `freely stop` 当前行为是 project-scoped stop，但没有冻结它是否永远不得触碰 shared watchdog/account artifacts。
3. `freely restart` 尚未成为 canonical surface；用户只能自己组合 stop/start，或者走某些 watchdog-owned recovery path。
4. `freely start --force` 目前没有 canonical contract，但这是控制面里最危险的语义点：如果 force 含义不清，极易从“重建本工位 supervisor/dispatcher”滑成“顺手清 global slot/cache/watchdog state”。
5. project-scoped `stop/restart/force` 必须只影响一个 Freely project runtime instance，不能隐式波及其他 project。
6. 若 future surface 暴露 global `stop/restart`，其语义必须明确是“all Freely project runtimes”，而不是“当前 project 外加若干 shared helper”。
7. global restart 不能只是 global kill + blind relaunch；它必须先保留 restore manifest，记住 restart 前哪些 project 处于 running/desired=running，再按该集合恢复。

## 为什么现在不能直接进 IBM

还缺少足够稳定的 issue 边界：

- 现有证据证明“project-scoped process ownership”已经部分实现，但这只是底层 identity 事实，不等于高层 CLI semantics 已冻结。
- `I-20260318-1630` 明确要求 global watchdog 继续拥有 slot/account recovery；这条问题不能再把 global control-plane 重吸回同 issue。
- 仓库里还没有现成的 canonical `freely restart` / `start --force` owner issue 可直接 continuation。
- 当前 runtime 真源只暴露 `cmd_start()` / `cmd_stop()`，并没有独立冻结 `cmd_restart()` 或 `cmd_start --force` 语义；这说明高层命令面仍未完成 materialization。
- handoff 指向的 `.freely/run/interruption-resolutions/20260327-201112-start-restart-control-plane-followthrough.md` 在当前 worktree 不存在；这进一步说明当前更适合先保留 discovery 边界，而不是假设已有稳定 issue materialization。

## 当前证据刷新

本轮按 `constitution-guard -> laws-enforcer -> lead-agent -> context-source-skill -> doc-pre-brainstorm-execution` 复核后，新增的稳定事实是：

1. runtime 真源没有用户态 `cmd_restart()`，也没有 `freely start --force` 参数面；`--force` 目前只存在于 `freely init`。
2. `cmd_stop()` 已经具备 project-scoped kill 边界：它只处理当前 project `.freely/run/` 下的 `ai.pid`、`ensure-manager.pid`、`interruption-dispatch.pid`、`supervisor.pid`，且 watchdog / dispatcher / supervisor 都会先通过 `valid_*_pid_for_project()` 校验。
3. project identity 的 canonical anchor 已相当明确：`pidfile + ps command line 中的 --project/-C + cwd fallback`，而不是按 `codex` / `node` / `bash` 等全局进程名猜测。
4. 当前仍不存在任何 global restart manifest 或 user-facing global restart command；仓库里只有 lower-layer watchdog / handoff / restart-storm recovery 事实。

因此当前问题不是“命令面已经存在，只差文档归档”，而是“只有 project ownership 底层事实部分完成，高层 command semantics 仍待冻结”。这继续支持本轮保持 `pre_brainstorm`。

## 缺失 handoff 的替代证据

虽然当前 worktree 不存在 `20260327-201112-start-restart-control-plane-followthrough.md`，但 continuity 没有断：

- manager interruption resolution:
  - `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/interruption-resolutions/20260327-202409-start-restart-control-plane-supervision-followthrough.md`
- manager continuity:
  - `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260327-210248.md`
- current worker continuity:
  - `.freely/run/worker-continuity-20260327-200651-start-restart-control-plane-semantics.md`
- session rotation handoff:
  - current round was relaunched after `context_compacted`, so branch-local pre-brainstorm artifacts and worker continuity remain the phase-appropriate continuity source before any further scope expansion

这三份 artifact 已足以覆盖：

- same-family continuation 仍由当前 worker lane 承接
- 当前 route 仍是 `pre_brainstorm`
- completed `I-20260318-1630` 只能提供 lower-layer global/shared supporting truth，不能 reopen
- manager follow-up 新增的 global semantics 要求已经被当前 lane 吸收，而不是停留在旧 prompt

## 边界草案

### 1. project-scoped assets

应该明确继续按 project identity 发现、校验、启动、停止：

- current worktree / project 下的 supervisor pid / ai pid
- project-local interruption dispatcher
- manager watchdog for this project
- project `.freely/run/` 里的 prompt、handoff、continuity、session-state、workcell-state
- project-local recovery / reentry decisions

project identity 目前最接近的 canonical anchor：

- pid file under `PROJECT/.freely/run/*`
- `ps` command line containing `runtime/freely ... --project <abs_path>` 或 `-C <abs_path>`
- 必要时的 cwd fallback

当前 runtime 真源直接支撑这些判断的函数是：

- `pid_matches_project()`
- `valid_supervisor_pid_for_project()`
- `valid_ensure_manager_watchdog_pid_for_project()`
- `valid_interruption_dispatcher_pid_for_project()`
- `valid_ai_pid_for_project()`

### 2. global/shared control-plane assets

不应被普通 project stop/start/force 隐式清理：

- shared slot/account watchdog state
- slot switch serialization lock
- active slot identity under `~/.codex/active-slot`
- any singleton launch gate / account inventory / cooldown/cache artifact whose lifetime outlives one project
- future truly singleton support daemons
- global restore inventory / restart manifest

### 2.1 asset taxonomy freeze draft

#### project-owned and safe for project force/restart

- supervisor pid/session for one `--project <abs_path>`
- manager watchdog for that same project
- interruption dispatcher for that same project
- worker prompt、manager continuity、session-state、workcell-state、recovery artifacts under that project's `.freely/run/`
- project-local AI session and its pid files

#### global/shared and only safe through explicit global action

- slot/account watchdog lifecycle when it spans all projects
- account-switch serialization lock and launch gate
- shared inventory / cooldown / cache artifacts whose lifetime outlives one project
- singleton support processes that are not anchored to one project path
- restore manifest that records which projects should come back after a global restart

### 3. semantic split draft

- `freely start`
  - 语义草案：ensure current project's control-plane/runtime is up
  - 当前 runtime 真源 `cmd_start()` 在发现已存在的 supervisor pid 时直接报 `already running`，因此它更接近“单 project bootstrap/attach gate”，还不是“自带 repair/restart 语义”的命令
  - 默认优先 attach/reuse healthy project-scoped components；发现 stale pid/state 时，只修 project-local artifacts
  - 若 global slot/account layer unavailable，则 defer to watchdog-owned recovery，不能在这里偷偷做 global reset
- `freely stop`
  - 语义草案：stop only this project's runtime/control-plane
  - 当前 runtime 真源 `cmd_stop()` 只读 project-local pid files，并通过 `valid_*_pid_for_project()` 校验 watchdog / dispatcher / supervisor pid 是否属于该 project 后才 kill；这证明 project-scoped stop 已有底层 identity 事实
  - 默认不触碰 shared slot/account/watchdog truth
- `freely restart`
  - 语义草案：project-scoped stop + fresh bootstrap of the same project control-plane/runtime
  - 只能重建本 project 的 supervisor / dispatcher / manager watchdog / AI session
  - 不负责恢复其他 project；若 shared/global layer 不健康，应返回显式升级信号而不是偷偷代做 global reset
- `freely start --force`
  - 候选语义：即使本 project 发现 stale pid / idle supervisor / partial local state，也强制重建本 project control-plane
  - 当前 runtime 真源尚未给 `start` 提供 `--force` 参数面，所以 force 目前仍只是待冻结 contract，不是已存在但文档缺失的命令
  - 明确非目标：不清 shared slot lock、不 wipe shared inventory/cache、不中断其他项目的 Codex/Node/Freely 进程

### 3.2 command-surface judgement refresh

基于本轮 runtime 真源扫描，当前更精确的状态是：

- `freely stop` 已有较稳定的 project-scoped 底层 blast radius
- `freely start` 只有 bootstrap / already-running gate 事实，还没有 attach-vs-repair-vs-fail-fast 的高层 contract
- `freely restart` 当前完全不存在 canonical user-facing surface
- `freely start --force` 当前完全不存在 canonical user-facing surface
- future global `stop` / `restart` / `reset` 目前只有需求，没有真源

因此最小裁决不是“现有命令已齐，只差 route”，而是“只有 project stop 的底层边界相对稳定；其余 control-plane 命令面仍需先冻结 owner taxonomy、blast radius 与 restore semantics”。

### 3.1 default stale-state priority draft

对 project-scoped `start` / `restart` / `start --force`，当前更合理的优先序：

1. attach/reuse 已健康且 project identity 匹配的本地 control-plane
2. repair project-local stale pid / partial readiness / idle supervisor
3. fresh bootstrap the same project runtime
4. 如果问题落在 shared/global owner，返回明确 escalation，让 explicit global action 或 watchdog owner 接管

这个优先序也应覆盖 interrupted local AI session：

1. 若当前 project 的 AI session target 仍可 attach/resume，可将其记录为 available continuity，但不把它自动等同于 `restart` 的默认副作用
2. 若 session 已不可恢复，但 supervisor / dispatcher / watchdog 仍属于同一 project，可做 project-local repair 或 fresh bootstrap
3. 不允许因为一个 project 的 interrupted AI session，就隐式触发跨项目 restore 或 global reset
4. project `restart` 默认只重建当前 project runtime/control-plane；interrupted AI work 必须通过单独显式的 resume/restore surface 接回，而不是在 restart 中静默恢复

### 3.3 safe project-scope repair set draft

project `start` 或 `start --force` 允许处理的 repair 集，当前应限制在单 project runtime 链，不跨到 shared/global 层：

1. 清理当前 project `.freely/run/` 下 stale pid file 与 stop marker 等易失 run-state
2. 当 supervisor pid 已不存在、dispatcher 未 ready、或 manager watchdog idle 且都能验证归属当前 project 时，重建同 project 的 supervisor / interruption dispatcher / manager watchdog
3. 在当前 project runtime chain 需要 fresh bootstrap 时，重建同 project 的 AI child process
4. 当 interrupted AI session 只影响当前 project 时，保留 continuity / handoff evidence 供后续显式 resume/restore；project repair 本身不静默吞掉这些 durable artifacts
5. 当 project-local control-plane 仍可健康 attach 时，优先 attach/reuse，而不是无条件 kill + rebuild
6. 若发现 lock / cache / inventory / watchdog reality 属于 shared owner，则 fail-fast 回 explicit global action，而不是继续 project-local repair

这意味着 `project force` 的安全上限应是“强制重建当前 project 的 runtime chain”，而不是“顺手打扫所有看起来相关的控制面残留”。

### 4. global reset surface draft

若未来需要“真的重置 shared control-plane”，应单独暴露显式 global action，而不是复用 project `start --force`：

- 例如独立的 watchdog/account/control-plane reset surface
- 明确要求 operator intent
- 明确只由 global/shared owner 执行
- 若定义 global `stop` / `restart`，其语义面也应落在这一层，而不是塞回 project command
- global `restart` 必须先生成 restore manifest，记住 restart 前哪些 project runtime 处于 running，再按该 manifest restore，而不是对所有已知 project 盲启动

当前更稳的命令面裁决是：

- global/shared action 使用显式 global namespace 或等价的一眼可见全局命令族
- project command family 下的 `--force` 不承担 global reset 含义
- 只要一个动作会影响多个 project 或 shared/singleton assets，它就必须被归类为 global action

### 4.1 global-only touch list draft

只有 explicit global action 才允许触碰的对象，当前应冻结为：

1. shared slot/account watchdog lifecycle
2. account-switch serialization lock 与 launch gate
3. shared slot inventory、cooldown、cache、availability ledger 等跨项目 artifact
4. truly singleton 的 support processes
5. global restore manifest，以及它对应的 previously-running project set

只要一个动作会影响以上任何对象，它就不再是 project `start` / `stop` / `restart` / `start --force`，而应被归类为独立 global action。

### 5. safe process-discovery identity draft

project-scoped recovery 不能依赖 `pkill codex`、`pkill node`、`pkill bash` 这类全局进程名匹配。更安全的 identity 组合应是：

1. project `.freely/run/*.pid` 作为 primary anchor
2. `ps` command line 中显式包含 `runtime/freely ... --project <abs_path>` 或 `codex exec ... -C <abs_path>`
3. project-local dispatcher / watchdog / supervisor pid 校验函数
4. 必要时以 cwd 作为最后 fallback，而不是作为唯一真相

只有同时满足 project anchor 与命令行归属时，project-scoped stop/force/restart 才可以 kill/rebuild 该进程。

### 5.1 global restart restore manifest draft

如果未来暴露 explicit global `restart`，最低 restore contract 不应只是“记住有哪些 project 目录存在”，而应至少记住：

1. 哪些 project 在 restart 前处于 `desired=running`
2. 哪些 project 在 restart 前已被 operator 显式 `stop`
3. 每个 project 最近一次可恢复的 `worktree_path`
4. 每个 project 最近一次可恢复的 `branch`
5. 每个 project 最近一次 continuity / handoff anchor
6. 每个 project 最近一次可用的 session / resume hint，或不可用原因
7. 每个 project 最近一次的 runtime intent，例如 `activity_state`、`last_exit_reason`
8. global restart 前是否已经存在 project-local repair failure 或显式 blocked escalation，避免 restart 后把已知坏态误判成“应该自动恢复”

这也意味着 global restart 更像“control-plane supervised fleet restore”，而不是“对所有项目重新执行一遍 `freely start`”。

### 5.2 durable landing point judgement

本轮进一步冻结的结论：

- future global restart restore manifest 不应落在任一 project 的 `.freely/run/`
- 更安全的 durable landing point 应位于 global control-plane namespace，下限是 `$FREELY_HOME` 下的 dedicated manifest artifact
- 原因不是“全局文件更方便”，而是 owner 与 blast radius 必须一致：
  - global restart 需要同时记住多个 project 的 `desired=running` / operator-stopped 排除集
  - project `stop` / `restart` / `start --force` 只能清理或重建单 project runtime chain，不能意外擦除 fleet restore memory
  - 若 manifest 放在某个 project `.freely/run/`，project-local force/repair 就会天然拥有误删全局恢复记忆的风险

因此可以先冻结“owner 层级”结论：manifest 是 global/shared truth，canonical durable home 属于 `$FREELY_HOME` 下的 dedicated global artifact；后续 IBM 再决定具体文件名和 schema。

### 5.3 interrupted AI work minimum-safe semantics

围绕 interrupted local AI work，本轮把最小安全语义再收紧一层：

1. project `restart` 默认不恢复 interrupted AI work
2. project `start` 默认也不恢复 interrupted AI work；它只负责让当前 project runtime/control-plane 回到可运行状态
3. interrupted AI work 的恢复必须来自显式 restore intent，而不是 `restart` / `force` 的隐式副作用
4. 这个 restore intent 可以在实现阶段 materialize 为 dedicated command 或显式 flag family，但语义层已经可以先冻结为“独立的 explicit resume/restore-work surface”，且当前更稳的 CLI 偏好是 dedicated project-scoped entrypoint
5. 该 surface 只能消费当前 project 的 durable continuity evidence，不能跨项目扫描或恢复其他 project 的未完成 AI work
6. 若当前 project 已被 operator 显式 stop，则 global restart 也不得借此 surface 把它自动恢复

因此当前可以先判定：真正需要冻结的不是“restart 顺便要不要 resume”，而是“resume/restore-work 必须是独立显式 operator intent、project-scoped，且默认优先以 dedicated surface 暴露”。

### 5.4 durable continuity vs ephemeral run-state

结合 runtime 真源，本轮可先把 project-local artifacts 分成两层：

#### ephemeral run-state，可由 project stop / local repair / force rebuild 清理或重建

- `session-state.env`
- `session-handoff.txt`
- `ai.pid`
- `supervisor.pid`
- `ensure-manager.pid`
- `interruption-dispatch.pid`
- `stop-requested`
- `restart-storm-window.tsv`

直接依据：

- `cmd_stop()` 明确删除 `session-state.env` 与 `session-handoff.txt`
- supervisor stop/start 直接围绕 pid files 与 stop marker 运作
- restart storm counter 被刻意留在独立窗口文件而不是 durable workcell truth

#### durable continuity evidence，project force 不得清理

- `workcell-state.env`
- `manager-worker-launch-state.env`
- worker continuity / manager continuity markdown
- interruption resolution artifacts
- delegated worker prompt / prompt evidence / intake evidence
- shared/watchdog memory consumed by this project, such as `codex-slot-cooldowns.tsv`
- 其他用于恢复 ownership、branch/worktree、restart point、next action、revisit trigger 的 project-owned continuity artifacts

这些 artifacts 的共同特征是：

- 它们定义生命周期 continuity，而不是当前瞬时进程句柄
- operator 或 manager 仍需要它们决定是否显式 resume/restore-work
- 如果 project force 清掉这些 evidence，global restart 与 project-scoped restore 都会退化成 blind bootstrap

## 行业模式对比草案

### A. per-service instance control

- 优点：最符合 `--project <abs_path>` 归属校验；易于避免误杀其他项目进程
- 风险：如果 force 语义不清，容易把 singleton/shared state 误当作 service-local state
- 对 Freely 的适配：project `start/stop/restart/force` 应默认落在这一层

### B. supervisor daemon + per-project worker

- 优点：符合 Freely 当前 manager watchdog / supervisor / dispatcher 的分层
- 风险：需要清楚区分 per-project watchdog 与 truly global watchdog，不然 `restart` 会跨层误伤
- 对 Freely 的适配：project restart 可以安全重建 supervisor/dispatcher/AI，但不该顺手重置 shared watchdog layer

### C. global agent control plane

- 优点：适合 slot/account serialization、shared launch gate、singleton support process
- 风险：若直接把 `freely start/stop/restart` 绑定到这层，会让 project command 获得过大的 blast radius
- 对 Freely 的适配：global stop/restart/reset 只应作为显式 operator action，且需要 restore-on-restart contract

### D. pidfile/socket/lock identity

- 这是当前最可行的 identity 基础
- project commands 应继续使用 `pidfile + ps --project + cwd fallback`
- shared control-plane 应继续使用 lock/socket/singleton identity，而不是 project pid
- 对 Freely 的适配：project-local pid validity 与 shared slot-switch lock 已具备底层事实，缺的是 CLI semantics freeze

### E. force-restart semantics

- 好的模式：先限定 blast radius，再决定 kill/repair scope
- 对 Freely 更合适的方向不是“一个 force 管所有层”，而是：
  - project force
  - explicit global reset

### 当前行业适配结论

- project scope 采用 `per-service instance control + supervisor daemon` 组合最贴合现状
- global/shared scope 采用 `singleton control plane + lock/manifest identity` 更安全
- 最不合适的模式是让 project command 直接兼做 global reset

## 当前建议

本轮保持 `pre_brainstorm`，但剩余任务已经从“继续冻结命令语义”收窄成“确定 follow-on IBM 的 owner 切分”：

1. project command semantics 与 global restart restore memory 是保持单 issue materialize，还是拆成两个紧邻 issue。
2. 若拆分为双 issue，哪一个作为 first materialization owner，哪一个作为依赖 follow-on。

## 当前裁决草案

### 1. 当前 route 仍应保持 `pre_brainstorm`

现有证据只足以证明底层 project ownership 已部分 materialize，不足以证明命令族已经拥有稳定 owner：

- `cmd_start()` 当前只有 `freely start --project <abs_path>` 参数面；若 supervisor pid file 仍指向存活进程，会直接返回 `already running`，没有 `--force`、没有 `restart`、也没有 stale-state repair contract。
- `cmd_stop()` 当前会清当前 project 的 `ai.pid`、`ensure-manager.pid`、`interruption-dispatch.pid`、`supervisor.pid`，并对 watchdog / dispatcher / supervisor 做 project 校验后再 kill；这证明 project stop 的底层 blast radius 已有实现事实。
- `valid_supervisor_pid_for_project()`、`valid_ensure_manager_watchdog_pid_for_project()`、`valid_interruption_dispatcher_pid_for_project()`、`valid_ai_pid_for_project()` 已把 `pidfile + 命令行中的 --project/-C + cwd fallback` 作为 project identity 保护层；这也说明仓库已经拒绝单纯按 `codex` / `node` / `bash` 进程名处理 project stop。
- 仓库中不存在 `cmd_restart()`，也没有 global restart restore manifest；因此 `restart` / `start --force` / global stop / global restart / explicit global reset 仍是 contract gap，不是现有 issue continuation。

结论：

- 本轮仍是 `source_class=continuation` 下的 `new_candidate_same_family_follow_on`。
- canonical owner 仍是新的 pre-brainstorm candidate，而不是 reopen `I-20260318-1630`。
- 在 `restart` / `force` / global action surface 冻结前，不进入 IBM，也不进入 runtime patching。

### 2. 命令面裁决方向

当前更稳的命令族方向应是两层分离，而不是把所有“重启/强制”揉成一个 `force`：

- project layer:
  - `freely start`
  - `freely stop`
  - `freely restart`
  - `freely start --force`
- explicit global/shared layer:
  - global `stop`
  - global `restart`
  - global `reset`

这里的关键不是具体命令拼写，而是 owner 和 blast radius：

- project layer 只允许读写、kill、repair、rebootstrap 当前 `--project <abs_path>` 所拥有的 runtime/control-plane。
- global/shared layer 才允许触碰跨项目共享的 slot/account watchdog、launch gate、global restore inventory 或 future singleton helper。
- project `--force` 不能成为 global reset 的语义捷径。

### 3. 预冻结的默认行为

若未来把这条 candidate 提升到 IBM，当前最接近 stable owner 的默认行为应是：

1. `freely start`
   - 语义是 ensure current project runtime/control-plane up。
   - 若当前 project 已健康运行，默认 attach/reuse，而不是报错后要求用户猜测下一步。
   - 若只发现 project-local stale pid / partial readiness，最多做 project-local repair。
   - 若问题落在 shared/global owner，返回显式 escalation。
2. `freely stop`
   - 语义是 stop only this project's runtime/control-plane。
   - 默认不清 shared slot/account state，不清全局 lock/cache/inventory，不触碰其他项目。
3. `freely restart`
   - 语义是 current project 的 controlled stop + fresh bootstrap。
   - 目标是重建同一 project 的 supervisor / dispatcher / manager watchdog / AI session，而不是 fleet-wide reset。
   - 默认不自动恢复 interrupted AI work；AI continuity 必须由独立显式 resume/restore surface 承接。
4. `freely start --force`
   - 语义是 project-scoped forced rebuild。
   - 允许越过 project-local stale pid / idle supervisor / partial state，但不允许越过 global/shared owner 边界。
   - 它只允许触碰本文件 `3.3 safe project-scope repair set draft` 列出的 project-safe repair 集。

### 4. global restart 的最低 restore contract

如果 future global `restart` 存在，它至少必须先保存 restore manifest，再做 stop/restart：

1. 记录 restart 前哪些 project 处于 `desired=running`。
2. 记录哪些 project 已被 operator 显式 `stop`，避免误恢复。
3. 记录每个 project 最近的 worktree / branch / continuity anchor，避免 global restart 只剩“目录存在”这一层弱事实。
4. 记录每个 project 最近一次的 runtime intent 与 continuity anchor，例如 `activity_state`、`last_exit_reason`、tool session / resume target，以及是否存在 interrupted AI work。
5. 若某 project 在 global restart 前已经因 shared/global owner 问题被显式 escalate 或 blocked，manifest 也必须保留该结论，避免 restart 后把它当作正常自动恢复对象。
6. restore 目标是 “restart 前处于运行态的 project set”，不是“当前磁盘上所有已知 project”。

只要这条 restore contract 还没冻结，就不应宣称 global restart 已经具备稳定 issue 边界。

### 4.1 command-surface preference draft

当前更稳的命令面方向不是把 global 语义塞进 project flag，而是：

1. project command family 继续保持 `freely start|stop|restart`
2. project force 只表达 local forced rebuild，不表达 shared/global reset
3. global/shared action 若存在，应使用显式 global namespace 或等价的一眼可见 surface
4. 无论最终采用独立 command 还是显式 global flag family，都必须让 operator 在调用时显式承认“这会影响多 project / shared control-plane”

### 4.2 interrupted AI work default draft

当前更稳的默认值应是：

1. project `restart` 默认只做 current project control-plane 的 controlled stop + fresh bootstrap，不静默恢复 interrupted AI work
2. 若 operator 明确要求恢复 interrupted AI work，这个 intent 必须通过独立显式的 project-scoped `resume/restore-work` surface 传入；若实现期保留 `--restore-work` flag，它也只能映射到同一显式语义，而不是藏在默认 `restart`
3. project `start --force` 允许放弃损坏的 project-local AI session，改为同 project fresh bootstrap，但仍应保留 durable continuity evidence，不得把这一步扩展成跨项目恢复
4. global `restart` 若存在，应依据 restore manifest 只恢复 restart 前 `desired=running` 的 projects；对其中的 interrupted AI work，也必须按各 project 的显式 restore contract 判断 resume 或 fresh_with_handoff，而不是 fleet-wide silent resume
5. operator 已显式 `stop` 的 project 不应被任何 global restart 自动恢复，也不应因为其遗留 interrupted AI evidence 被“顺带复活”
6. 若 future product 需要“重启 project control-plane 并恢复 interrupted AI work”，那也应是单独显式 surface 组合，而不是 project `restart` 的隐含副作用

### 4.2.1 explicit restore surface preference draft

基于当前 runtime 真源与 owner taxonomy，更稳的 materialization 方向已经可以再收紧一层：

1. `start` 继续表达“确保当前 project runtime/control-plane up”
2. `restart` 继续表达“对当前 project 做 controlled stop + fresh bootstrap”
3. interrupted AI work 的恢复继续保持单独 explicit intent，不再挤占 `restart` 默认语义
4. `cmd_start()` 当前只有 bootstrap/already-running gate，没有 repair+restore super-command 真相，因此把 restore 强行叠到 `start` / `restart` 上只会扩大 blast radius 与 operator 误判
5. 因此 IBM 前更推荐的 CLI materialization 方向是 dedicated project-scoped `resume/restore-work` entrypoint；若后续保留 `--restore-work` flag，也只能作为同一 explicit restore intent 的 alias，而不是把默认 `start` / `restart` 重新改回隐式恢复入口

### 4.3 project-local artifact taxonomy draft

基于当前 runtime/status 真源，project-local artifact 更接近以下分层：

1. 易失 run-state，可由 project repair/rebuild 清理或重建：
   - `supervisor.pid`
   - `ai.pid`
   - `interruption-dispatch.pid`
   - `ensure-manager.pid`
   - `stop marker`
   - `session-state.env`
   - `session-handoff.txt`
   - `restart-storm-window.tsv`
2. 更接近 durable project intent / continuity，不应被 project force 静默抹掉：
   - `workcell-state.env` 这类 project-level desired/runtime intent mirror
   - `manager-worker-launch-state.env` 这类 manager-side continuity/prompt consumption memory
   - worker continuity / manager continuity / interruption resolution 这类明确服务恢复与交接的 artifact
   - `.freely/intake/**` 与 worker prompt 这类后续恢复链仍会消费的证据面
   - shared/watchdog memory 在当前 project 下的消费镜像，例如 `codex-slot-cooldowns.tsv`
3. 当前真源信号支持这层区分：
   - `cmd_stop()` 明确会清 `session-state.env` 与 `session-handoff.txt`，因此它们更接近 session telemetry / ephemeral run-state，而不是 durable restore manifest
   - `workcell-state.env` 在 stop 后被重写而不是删除，并持续承载 `desired_runtime_state` / activity mirror，更接近 project-local durable intent
   - manager prompt/continuity 选择链会显式读取 continuity 与 worker prompt evidence，而不是依赖 `session-state.env` 独自承担恢复
   - intake / interruption resolution / cooldown artifact 也都表现为跨轮可复用 memory，而不是单次 supervisor scratch

### 4.3.1 minimum durable continuity white-list draft

若 future project-scoped restore surface 要避免退化成 blind bootstrap，当前最小 white-list 已可先冻结为：

1. `workcell-state.env`
2. `manager-worker-launch-state.env`
3. worker continuity / manager continuity markdown
4. interruption resolution artifacts
5. delegated worker prompt / prompt evidence
6. `.freely/intake/**` intake evidence

这些 artifact 的共同点是：它们承载 owner、branch/worktree、restart point、next action、revisit trigger、desired runtime intent 或 delegated continuation evidence，而不是仅仅记录瞬时 pid / telemetry。

这也把最后一轮未决项收窄为：follow-on IBM 的 owner 切分应保持单 issue 还是拆成 `project command semantics` / `global restart restore memory` 双 issue。

### 4.3.2 restore manifest landing-point freeze draft

global restart restore memory 的 owner 与落点，本轮可以再冻结一层：

1. canonical durable home 不属于任一 project `.freely/run/`
2. canonical directory-level landing point 应属于 `$FREELY_HOME/control-plane/restart/`
3. manifest 本体应是该目录下的 dedicated restore artifact，而不是混进 config、slot cache、cooldown ledger 或单 project state
4. 当前仍未决的是具体文件名、schema 与 retention/rotation policy，而不是 owner 层级或目录层级

这样做的原因是：

- global restart 需要记录 fleet-wide previously-running project set 与 operator-stopped exclusion set
- project `stop` / `restart` / `start --force` 不能天然拥有擦除这份 fleet restore memory 的权限
- `$FREELY_HOME/control-plane/restart/` 这一层已经足够把它与 project `.freely/run/`、shared slot cache、以及普通 config truth 分开，后续 IBM 只需继续 materialize artifact shape

### 4.3.3 final freeze pass

围绕本轮 handoff 要求的 5 个未决点，当前更稳的收口如下：

1. `freely restart` 应被视为需要 materialize 的一等 command surface，而不是长期隐藏在 `stop + start` 组合里的语义。
   - 在实现落地前，runtime 内部可以复用 `stop + start` 编排。
   - 但对 operator、issue owner 与 acceptance contract 来说，canonical surface 应是显式的 project-scoped `restart`，否则 blast radius、default restore policy 与 verification 无法稳定落盘。
2. `start` 与 `start --force` 之间暂不再新增第三个 repair-only 用户态 surface。
   - `start` 负责 `attach/reuse -> safe local repair -> bootstrap same project`。
   - `start --force` 负责跳过本地保守修复、直接重建当前 project runtime chain。
   - 若后续仍发现 repair-only contract 需要独立 operator intent，再作为 follow-on capability，而不是先把本 candidate 的命令面拆散。
3. explicit AI-work restore 的 canonical 命名优先冻结为 dedicated project-scoped `freely restore-work`。
   - `restart` 默认不恢复 interrupted AI work。
   - `restore-work` 只恢复当前 project 的 interrupted AI continuity。
   - 若实现期保留 `--restore-work` 形式，它只能是映射到同一 explicit restore intent 的 secondary alias，不能反向成为 primary surface，也不能把默认 `start` / `restart` 重新变回隐式恢复入口。
4. global restart restore manifest 的最小 durable shape 先冻结到目录、文件布局、字段层级与 retention policy：
   - directory: `$FREELY_HOME/control-plane/restart/`
   - latest pointer: `$FREELY_HOME/control-plane/restart/latest.json`
   - history: `$FREELY_HOME/control-plane/restart/history/<timestamp>.json`
   - retention: 永远保留 `latest.json` 与最近 20 份 timestamped history；更旧 history 可轮转删除
   - manifest envelope minimum:
     - `manifest_version`
     - `created_at`
     - `trigger`
     - `operator_scope`
     - `projects`
   - `projects[]` minimum:
     - `project_root`
     - `worktree_path`
     - `branch`
     - `desired_runtime_state_before_restart`
     - `operator_stopped`
     - `activity_state`
     - `last_exit_reason`
     - `continuity_anchor`
     - `resume_hint`
     - `blocked_or_escalated_before_restart`
5. project-scoped restore 的 mandatory anchors 与 auxiliary evidence 先冻结为两层：
   - mandatory restore anchors:
     - `workcell-state.env`
     - `manager-worker-launch-state.env`
     - worker / manager continuity artifacts
     - interruption resolution artifacts
     - delegated worker prompt evidence
     - `.freely/intake/**`
   - auxiliary evidence only:
     - `session-state.env`
     - `session-handoff.txt`
     - `*.pid`
     - `stop-requested`
     - `restart-storm-window.tsv`
     - `codex-slot-cooldowns.tsv`

这里把 `codex-slot-cooldowns.tsv` 降为 auxiliary，不是否认它有跨轮价值，而是因为它更接近 shared/watchdog memory 的消费镜像，不应成为 project-scoped `restore-work` 成败的 mandatory anchor。若 future global/shared restore 需要它，应由 global owner 在自己的 restore contract 中读取，而不是要求 project restore 把它当作最小必需项。

## owner-splitting judgement

### frozen decision

follow-on IBM 应 materialize 为两个紧邻 issue，而不是一个大而全的 command-family issue：

1. `project command semantics`
   - owner scope: 单 project runtime/control-plane chain
   - covers:
     - `freely start`
     - `freely stop`
     - `freely restart`
     - `freely start --force`
     - dedicated project-scoped `restore-work`
   - freezes:
     - attach/reuse -> local repair -> fresh bootstrap -> global escalation 的默认优先序
     - project force 的 safe repair set
     - process discovery / kill identity 只能依赖 project anchor
     - interrupted local AI work 在 project restart / force 下的默认行为

2. `global restart restore memory`
   - owner scope: all-project / shared control-plane memory
   - covers:
     - explicit global restart namespace 或等价 global action surface
     - restore manifest schema / retention / durable landing point
     - previously-running project set
     - operator-stopped exclusion
     - global restart 后的 fleet restore policy
   - freezes:
     - manifest durable home 继续位于 `$FREELY_HOME/control-plane/restart/{latest.json,history/<timestamp>.json}`
     - keep latest + last 20 history retention
     - mandatory restore anchors 与 auxiliary evidence taxonomy 不得回写到 project command owner 里重定义

### why not single issue

单 issue 会把两个不同 owner 再次揉回一起：

- `project command semantics` 只应决定单 project command 的 blast radius、repair semantics 与 restore-work default
- `global restart restore memory` 讨论的是 explicit global action、fleet restore memory 与 shared control-plane durability
- 两者 acceptance surface 不同，成熟度也不同：project command semantics 已接近 issue-ready，而 global restart restore memory 仍有 manifest / fleet restore schema 细节要在 IBM 内展开

如果现在强行合成一个 issue，IBM 很容易重新滑回“project force 顺手兼做 global reset”的混层。

### sequencing freeze

IBM 应按固定顺序 materialize，避免重新混层：

1. 先写 `project command semantics`
   - 先冻结 project-owned vs global/shared taxonomy 在 command surface 上的真正边界
   - 先定义 project restart / force / restore-work 的 operator semantics
2. 再写 `global restart restore memory`
   - 只在 explicit global action namespace 内工作
   - 依赖前一 issue 已冻结的 taxonomy、restore anchors 和 project-local exclusions
   - 不得回头改写 project `start` / `stop` / `restart` / `start --force` 的 blast radius
3. 两个 issue 都只能把 `I-20260318-1630` 当作 lower-layer supporting truth
   - 不 reopen global watchdog/bootstrap owner
   - 不重写 explicit resume target、session rotation 或 watchdog boundary 的既有 contract

## 推荐下一跳

- 当前 route_kind: `pre_brainstorm`
- 当前轮次完成形态: `promotion handoff ready`
- 下一跳应进入 `skill:doc-ibm-execution`
- 本轮已把最后一个 promotion gate 关闭：follow-on IBM 不再保持单 issue，而是按 owner 切成 `project command semantics` 与 `global restart restore memory` 两个紧邻 issue
- 由于当前 worker write scope 只允许 pre-brainstorm / milestone / continuity surfaces，本轮在 promotion handoff 停止，不直接写 `docs/B2-docs/**`
