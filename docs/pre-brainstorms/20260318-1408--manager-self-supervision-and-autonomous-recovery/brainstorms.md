# Manager Self-Supervision And Autonomous Recovery

## Trigger

这次后台 supervisor/worker 实际已经停摆，但问题不是主管自动发现，而是人工主动要求检查后才暴露：

- `wt-fleet-status` 已显示全盘 `down/down`
- `freely baseline-status --project <develop>` 仍残留陈旧 `supervisor_pid`
- 主管没有主动发起“后台工位巡检失败”的恢复动作

这说明 Freely 已经有 worker supervision 的局部能力，但缺少“主管自我监督”这一层。

## Problem

当前主管模式的设计仍有三个缺口：

1. `develop` 上的主管 prompt 只在“被启动的一轮”里做排班，没有独立的巡检职责；一旦该轮结束或失败，没人再确认主管/worker 是否还活着。
2. `wt-fleet-status` 只是 CLI 观察面，不会主动驱动恢复；需要人工运行后才知道盘面失活。
3. supervisor 当前更像“托管单个项目会话”，而不是“持续监督整个工位舰队”。这与 Freely 自举时对主管的要求不匹配。

## Decision

Freely 需要把“主管自检 + 工位巡检 + 自主恢复”提升为 control-plane 正式能力：

1. `develop` 主管位必须定期读取项目级 fleet 状态，而不是只在启动首跳时看一次。
2. 主管位需要显式区分：
   - 主管自己是否健康；
   - 应继续运行的 worker 是否缺席；
   - 某工位是应冻结还是异常掉线。
3. 若主管发现“应运行的工位缺席”，下一轮优先级必须切到 supervision / recovery，而不是继续普通路由。
4. 这种检查不能只靠 Git hook；应落在 runtime hook / cycle post-hook / periodic wakeup。
5. 主管仍然不直接实现业务；它只做巡检、排班、委派和恢复。

## Role Boundaries

这条能力必须明确分层，避免主管变成“万能执行者”：

1. `manager`
   - 只负责读取全局工位状态、发现异常、输出清晰委派或清晰告警。
   - 不直接修业务问题，不代替 worker 做本地恢复，不接管账号切换。
   - 发现问题后的动作应是：
     - 指定目标工位；
     - 指定 owner；
     - 指定下一步是 `runtime_recovery_requested / delegate / freeze / merge / cleanup` 中哪一种。

2. `worker`
   - 只负责自己工位上的 doc loop / dev loop / verification。
   - 本地 checkpoint、continuity、resume/fresh_with_handoff 由工位 runtime 和 worker 自己配合处理。

3. `runtime / scripts`
   - 负责 AI 已经无能为力时的脚本恢复动作，例如：
     - AI 响应已经结束，当前会话不可能再“自己启动自己”
     - 进程已经退出或 supervisor/worker 已经消失，当前 AI 不可能再自行 fork/restart
     - 账号限额后的 `ai switch`
     - 认证失败、token 失效、CLI 退出码要求重新登录或重新选择账号
     - 选择最早恢复账号并等待唤醒
     - `context compacted` / 会话轮换后，由脚本重新拉起新进程并带上 continuity / 角色提示
     - 进程退出后的本工位重启
   - 如果重启的是主管工位，脚本恢复时继续带主管角色提示；
     如果重启的是 worker 工位，脚本恢复时继续带 worker 角色提示。

结论：
- `runtime` 管生存
- `worker` 管执行
- `manager` 管编排

主管若发现“账号限额”这类问题，不应自己处理；它只需要识别“该问题的 owner 是本工位 runtime”，然后让脚本链路继续接管。
这里的“接管”是指主管输出恢复判定，实际切号、等待和重启仍由 runtime 执行。

## AI-Powerless Boundary

下列情况应被明确视为“AI/manager/worker 无能为力”，只能交由 runtime / scripts：

1. 当前 AI 输出已经结束，无法在自身响应终止后再次调用自己。
2. 目标进程已退出、被杀掉或尚未启动，AI 无法在不存在的进程内继续执行恢复。
3. 命中 `primary` / `secondary` 限额、认证失败或账号失效时，当前 AI 往往已经不能继续可靠地产出动作。
4. 发生 `context compacted`、fresh session rotation、resume after exit 时，需要脚本重新发起带角色提示的新工具进程。
5. 需要等待未来某个 `reset_at` 时刻并在窗口到达后唤醒，AI 不能假定自己在睡眠后仍持续可用；必须由外层 runtime 重检并重新启动。

因此：
- `manager` 只能把这类情况标记为 `runtime-owned`
- `worker` 只能回写 blocker / continuity
- 真正的恢复动作必须由 runtime / scripts 落地

## Initial Capability Shape

- `manager-supervision tick`
  - 周期读取 `wt-fleet-status --format json`
  - 识别 `expected-active worktree` 与 `actual up/down`
  - 写回 `session-state` 的主管监督结论
- `manager recovery route`
  - 当主管或目标 worker 意外掉线时，自动转入 recovery/delegation handoff
  - 若异常 owner 属于 `runtime`，只生成结构化恢复目标，不让主管自己下场修
- `manager continuity`
  - 将“本轮应继续的 worker、冻结列表、异常列表、待恢复列表”作为 continuity artifact，而不是只依赖人工聊天记忆
- `runtime-owned account recovery`
  - 限额/认证问题由当前工位 runtime 直接处理
  - 主管只需看到结果状态，不接管切号逻辑

## Intended Landing

- `docs/LAWS.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/worktree/wt-fleet-status`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
