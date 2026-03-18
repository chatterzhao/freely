# Manager Self-Supervision And Autonomous Recovery

## Trigger

这次后台 supervisor/worker 实际已经停摆，但问题不是主管自动发现，而是人工主动要求检查后才暴露：

- `wt-fleet-status` 已显示全盘 `down/down`
- `freely status --project <develop>` 仍残留陈旧 `supervisor_pid`
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
     - 账号限额后的 `ai switch`
     - 选择最早恢复账号并等待唤醒
     - 进程退出后的本工位重启
   - 如果重启的是主管工位，脚本恢复时继续带主管角色提示；
     如果重启的是 worker 工位，脚本恢复时继续带 worker 角色提示。

结论：
- `runtime` 管生存
- `worker` 管执行
- `manager` 管编排

主管若发现“账号限额”这类问题，不应自己处理；它只需要识别“该问题的 owner 是本工位 runtime”，然后让脚本链路继续接管。
这里的“接管”是指主管输出恢复判定，实际切号、等待和重启仍由 runtime 执行。

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
