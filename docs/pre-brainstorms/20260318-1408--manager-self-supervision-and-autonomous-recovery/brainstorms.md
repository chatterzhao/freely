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

## Initial Capability Shape

- `manager-supervision tick`
  - 周期读取 `wt-fleet-status --format json`
  - 识别 `expected-active worktree` 与 `actual up/down`
  - 写回 `session-state` 的主管监督结论
- `manager recovery route`
  - 当主管或目标 worker 意外掉线时，自动转入 recovery/delegation handoff
- `manager continuity`
  - 将“本轮应继续的 worker、冻结列表、异常列表、待恢复列表”作为 continuity artifact，而不是只依赖人工聊天记忆

## Intended Landing

- `docs/LAWS.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/worktree/wt-fleet-status`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
