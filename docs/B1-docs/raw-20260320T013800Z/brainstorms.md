# 预研头脑风暴：插话入口运行面前置检查

## 背景
- `freely chat` 和 `freely tui` 是人类插话入口，语义上要求“主管第一时间注意到并处理”。
- 当前实现里，即使 `supervisor` 和 `interruption dispatcher` 都没运行，`freely chat` 仍会成功写入 intake，形成“看起来成功、实际上无人处理”的假成功。
- 这和 `freely intake chat` 的低层 durable 收件能力混在了一起，导致人类入口和底层入口边界不清。

## 问题定义
- 人类入口必须保证“现在有人会接住这条插话”，否则不应假成功。
- 低层 durable 收件仍然需要保留，供离线导入、恢复、脚本桥接使用。
- 前置检查应该尽量收在 runtime entrypoint，不把一堆状态判断扩散到上层 prompt 或 skill。

## 收敛判断
- `freely chat` / `freely tui` 视为高层 human entrypoint。
- `freely intake chat` 视为低层 durable intake primitive。
- high-level entrypoint 在提交前必须执行 runtime preflight：
  - 若 `interruption dispatcher` 已运行，则直接放行。
  - 若只有 `supervisor` 运行，则尝试拉起 dispatcher，并等待其 ready。
  - 若两者都没有，则报错，提示先启动 `freely start` 或 `freely ensure-interruption-dispatch --watch`。
- 错误提示必须明确给出 offline escape hatch：
  - 若只是想离线记录，不要求立即处理，则改用 `freely intake chat`。

## 非目标
- 不让 `chat/tui` 在未启动时自动偷偷写 intake。
- 不在这里补“自动拉起完整 supervisor”之外的大规模自恢复策略。
- 不把这条能力做成新的 skill；这是 CLI runtime contract。

## 结果语义
- 人类入口：保证“立即可被处理”，否则失败。
- 低层 intake：保证“立即可落盘”，不保证立即处理。
- 这两层语义必须显式分开。
