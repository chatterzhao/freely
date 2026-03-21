# 预研：status family baseline rename and future aggregation

## Trigger

- Freely 现在已经同时存在三种状态面：
  - `status`
  - `live-status`
  - `fleet-status`
- 其中当前 `status` 的真实职责已经偏向 durable / baseline snapshot，而不是“当前谁在干活、在干什么”。
- 用户明确提出：先把现在的 `freely status` 重命名为 `freely baseline-status`，为未来把 `freely status` 收成聚合入口腾出语义空间。

## Problem

当前名字和职责已经开始错位：

- `status` 实际输出的是配置、session-state、dirty summary、checkpoint、pid 摘要
- `live-status` 才是当前态控制面
- `fleet-status` 是项目级 worktree 视图

如果不先把这三个面命名收紧，后续再把 `status` 做成聚合入口时会更混乱。

## Direction

先做一层轻量但完整的重构：

1. 把当前 `status` 的正式 baseline 语义改成 `baseline-status`
2. 让 `status` 直接成为 family 聚合入口，而不是继续伪装成 baseline alias
3. 当前活跃文档与测试开始优先使用 `baseline-status`
4. 同时落下第一版 `status family`：
   - `baseline-status`
   - `live-status`
   - `fleet-status`
   - `freely status --view baseline|live|fleet|all`

## Scope Boundary

本轮只做：

- baseline 命令命名
- status family 聚合入口
- 当前活跃 skill / 文档 / 测试同步

本轮不做：

- 统一 JSON family 输出

## Anti-Retrogression

本轮不能把现有依赖 `freely status` 的狗粮链路直接打断。

因此：

- baseline-specific 文档和测试迁移到 `baseline-status`
- `status` 默认输出聚合视图，但保留 `--view baseline|live|fleet|all`
- 不回退 `live-status` / `fleet-status` 的独立职责
