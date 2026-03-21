# 预研：watchdog live status surface and manager supervision

## Trigger

- 这几轮 Freely 自举里，后台 `supervisor / interruption dispatcher / AI` 进程明明还活着，但外部看起来像“停住了”。
- 当前已有 `freely baseline-status`、`fleet-status`、`.freely/run/prompt-*`、`manager-continuity-*`、`session jsonl`、`ps`，但这些都是碎片；主管和用户都需要人肉拼接。
- 用户明确提出：应该有一个 watchdog CLI，只看“当前有哪些 AI 在跑、pid 是什么、正在做什么”，默认不刷水流，但要给出 `jsonl` 地址和提示词截取，方便需要时深挖。

## Problem

Freely 现在不是完全不可观测，而是缺少一个 canonical current-state surface。

这带来三类实际问题：

1. 进程还活着，但没人知道它是在有效推进、停在 handoff，还是只剩 dispatcher 在等。
2. 主管在 `develop` 上承担监督职责时，没有统一入口判断“现在全局谁在做什么”，只能靠 `baseline-status + fleet-status + prompt + continuity + ps` 临时拼。
3. interruption 已经是事件源，但主管监督还没有一张同源当前态面板，所以全局视野不稳定。

## Direction

应新增一个最小的 `live-status` surface，作为 watchdog / runtime 当前态视图：

- 默认输出当前态，不输出流水
- 只展示活跃 pid，不展示已退出 pid
- 至少包含：
  - `supervisor / interruption dispatcher / AI` 的 pid 与 command
  - 当前 `branch / role / activity_state`
  - 提示词截取，让人知道当前 AI 是哪个、在做什么
  - manager continuity 摘要
  - 最近 active intake / resolution 摘要
  - `jsonl / cycle_log / prompt_file` 深挖入口

## Supervision Judgment

主管不需要再起一套独立 watchdog 循环去反复刷日志。

更合理的协议是：

1. 主管轮次开始时，先读 `freely live-status --project <develop>`
2. 若当前问题涉及全项目 worktree，再结合 `freely fleet-status`
3. 只有当 `live-status` 暴露 `runtime-owned` 异常、handoff 卡住、或 intake 堆积时，才进入更深的 runtime / continuity / interruption 路径

也就是说：

- interruption 仍然是事件源
- `live-status` 是当前态控制面
- manager supervision 以“每轮先读当前态”为协议，而不是继续依赖人工 grep

## Scope Boundary

本轮只做最小可用面：

- CLI current-state surface
- prompt excerpt / continuity excerpt / deep refs
- manager / supervision skill 接线
- 脚本测试

本轮不做：

- 独立 Web UI
- 长驻流式 watch daemon
- 完整 stall detection 评分系统
- 全仓库统一 JSON API server

## Intended Landing

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/tests/test-freely-live-status`
