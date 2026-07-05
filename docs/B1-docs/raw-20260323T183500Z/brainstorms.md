# 预研头脑风暴：worker-delegated-continuation-active-stall-recovery

## 背景

这轮真实 dogfood 里，manager 已经把 retained dirty worker tree 的 continuation 正确写回成新的 worker handoff，并且 target worker 也保持 active：

- manager continuity 与 worker prompt 都已生成
- target worker intake 收到了新的 delegated continuation
- worker runtime 仍显示 `ai_active`

但随后又暴露出新的假活断点：

- worker AI 进程继续存活
- worker cycle log 不再推进
- prompt 已经含 `Delegated continuation handoff`
- manager watchdog 只会恢复 `supervisor down` 的 worker，不会处理 `supervisor up + AI fake-live` 的 worker

结果是：Freely 会卡在“worker 看上去还活着”，但 canonical closeout、retirement、以及后续 discovery/new worktree 都无法继续。

## 问题定义

当前 runtime 对 worker 的恢复只覆盖：

- manager handoff 转 worker intake / local continuation reentry
- expected-running worker 掉线后重新启动 supervisor

但还没覆盖：

`worker already active -> delegated continuation 已进入当前 prompt -> AI 假活且无新输出 -> 外层没有 runtime-owned recovery`

如果这条 contract 缺失，三层 loop 会在 worker 收口阶段再次断裂，无法稳定走完：

`reuse/create worktree -> writeback -> merge -> cleanup/retirement -> next patrol`

## 候选方向

1. 把 `active worker + delegated continuation prompt + stale cycle log` 视为 runtime 可监督异常
2. 由 manager watchdog 对 expected-running worker 补一层 stall detection，而不只检查 `supervisor down`
3. 若命中 stall contract，触发 worker 本地 continuation reentry / restart，而不是等待人工 stop/start
4. 将这条 contract 记录为 runtime-owned 边界，避免再误归到 worker 语义层

## 建议承接位置

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- worker stall recovery tests

## 生命周期判断

- 这是 Freely 自举中暴露的 runtime control plane 通用缺口
- 它不等于已完成的 active-worker reentry issue；那条 issue解决的是“handoff 进入 active worker”
- 这条新缺口解决的是“进入以后，worker AI 假活时如何自动恢复”
