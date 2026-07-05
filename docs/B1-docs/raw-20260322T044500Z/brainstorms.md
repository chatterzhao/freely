# 预研头脑风暴：latest-manager-continuity-worker-consumption

## 背景

在真实狗粮中，`develop` 主管已经能够：

- 通过 `freely chat` 接住项目级治理信号
- 产出新的 `manager continuity`
- 写出新的 worker prompts
- 基于 `worktree-maintenance-governance` 给出合理 disposition

但当前 runtime 仍出现一个新的断点：

- 新的 `manager-continuity-20260322-042256.md` 已生成
- 对应的新 worker prompt 也已生成
- 现有 worker 却仍停留在更早一轮 delegated continuation
- `manager-worker-launch-state.env` 仍指向旧 continuity

这说明问题不再是主管不会判断，而是：

`latest manager continuity / worker prompt generation -> manager runtime launch consumption`

没有对齐到最新一轮监督结果。

## 观察证据

- 新 continuity:
  - `.freely/run/manager-continuity-20260322-042256.md`
- 新 prompts:
  - `.freely/run/worker-prompts/20260322-042256-worker-cli-retire-codex.txt`
  - `.freely/run/worker-prompts/20260322-042256-worker-manager-handoff-cleanup-codex.txt`
  - `.freely/run/worker-prompts/20260322-042256-worker-runtime-linkage-verify-codex.txt`
  - `.freely/run/worker-prompts/20260322-042256-worker-three-loop-continue-dev-codex.txt`
- 旧 launch state:
  - `.freely/run/manager-worker-launch-state.env`
  - `LAST_MANAGER_CONTINUITY_CONSUMED` 仍指向旧 continuity
- worker runtime truth:
  - `cli-first`、`manager-handoff`、`runtime-worker` 已被拉起
  - 但 `live-status` 仍显示它们在消费旧 delegated continuation ids

## 问题定义

Freely 现在缺少一个更严格的 canonical contract：

- 主管生成新的 continuity 后
- runtime 应该以“最新 continuity”为基准判断是否需要：
  - launch new worker
  - reenter active worker
  - skip because already consumed

不能只依赖旧的 consumed marker 或旧的 launch-state snapshot。

## 相关现有能力

- `20260322-0245--runtime-worker-launch-linkage-and-stall-recovery`
  - 解决了 manager 能把 worker prompt 变成真实 launch / stalled recovery
- `20260322-0412--worker-active-reentry-for-manager-delegated-continuation`
  - 解决了 active worker 遇到 delegated continuation 时的 local reentry
- `20260322-0049--manager-continuation-handoff-consumption`
  - 解决了主管 continuation handoff 的 generated/consumed evidence

当前缺口位于这三条能力的交叉处：

- 最新 manager continuity
- latest worker prompt set
- active/stale worker reentry / launch state

## 候选方向

1. 定义 latest-manager-continuity consumption gate
- runtime 每次尝试 worker launch / reentry 时，先比对最新 continuity 文件与 launch-state 中的已消费锚点。

2. 定义 worker prompt generation set identity
- 不只看某个 prompt 文件是否存在，而是看某一轮 manager continuity 派生出的 prompt 集是否已被消费。

3. active worker reentry 优先 latest prompt
- 若 worker 仍活跃但主管产生了更新的一轮 delegated prompt，必须允许把该 worker 重入到最新 prompt，而不是沿用旧 delegated intake 无限继续。

4. 观测面同步
- `live-status` / `manager-worker-launch-state.env` 应暴露：
  - latest continuity generated
  - latest continuity consumed
  - prompt set generated
  - prompt set consumed

## 为什么现在做

- 这是 Freely 真正开始用 Freely 自治开发后暴露的真实断点
- 若不修，主管虽然能判断，但 runtime 不能把最新监督结果推进成最新 worker 行为
- 这会导致旧任务继续跑、新监督结果悬空，破坏 auto-loop 的闭环

## 建议承接位置

不要新造平行技能。优先扩到：

- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/scripts/runtime/freely`
- 必要时补 `worktree-maintenance-governance` 的 handoff / launch reference

## 生命周期判断

- 这不是历史 closeout 问题
- 这是新的活跃 runtime gap
- 应进入新的 issue 生命周期，而不是回写历史已完成 issue
