# 预研：manager chat reentry and cleanup misrouting

## Context

- 日期：2026-03-21
- 触发：
  - 在 `develop` 工位真实执行了：
    - `freely start`
    - `freely chat "<项目级主管任务>"`
  - 结果显示：
    - 主管进程确实被拉起
    - chat 被 intake 成功
    - 但新任务没有触发新的主管级 patrol / restart-point routing
    - 而是被错误吸收到旧的 `cleanup://merged-worktree-followthrough`

## Problem

Freely 当前的 `chat -> intake -> interruption dispatcher` 路径能够做到：
- durable intake
- 自动 claim / triage
- 进入 one-shot interruption manager handler

但在广义主管巡检任务上，当前 interruption manager prompt 过度偏向 cleanup/worktree 收口：

- 只要消息里出现 `检查 worktree / 哪些 worktree 可 merge / 现在该怎么收口`
- 就容易默认：
  - `delegate`
  - `restart_point=cleanup`
  - `ownership=worker`

这会导致：
- 新的项目级监督任务没有回到主管主循环
- 旧 continuity / cleanup followthrough 过早吞掉新 signal
- 用户虽然只通过 chat 插话，但 Freely 没有按新的 supervisor task 正确重启与路由

## Proposed Clarification

### 1. 区分“纯 cleanup 请求”和“广义主管巡检请求”

若用户是在问：
- 已合并 worktree 该怎么收口
- 哪些 merged branch 可以退休
- 纯 cleanup / retirement handoff

则可以默认：
- `restart_point=cleanup`
- `ownership=worker`

但若用户同时要求：
- 检查 `worktree + milestones + issues + intake + runtime`
- 或显式要求“你现在是主管 / 检查所有 / 自我开发自己”

则不应直接吞到 cleanup。

### 2. 广义主管巡检任务应回到 manager continuation

这类 signal 更像：
- 新的项目级 supervision request
- 应让主管下一轮重新做：
  - `live-status`
  - `fleet-status`
  - restart-point routing

因此更合理的默认是：
- `delegate`
- `classification=control`
- `restart_point=continuation`
- `ownership=manager`

### 3. 这条问题应通过真实集成测试守住

不能只修 prompt wording。

至少应补：
- interruption manager handler prompt regression
- `freely chat` -> intake -> dispatcher -> delegated continuation 的回归

## Likely Landing

1. `docs/system/workspace/scripts/runtime/interruption-manager-handler`
2. `docs/system/workspace/scripts/runtime/freely`
3. `docs/system/workspace/scripts/tests/test-interruption-manager-handler`
4. `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`

## Expected Result

1. 新的主管级 chat signal 不再被旧 cleanup continuity 过早吸收
2. 纯 cleanup 请求仍然保持 cleanup 路径
3. 广义主管巡检请求回到 manager continuation / restart-point routing
