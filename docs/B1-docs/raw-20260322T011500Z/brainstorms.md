# Brainstorms

## Topic
CLI-first entrypoint and observability surface unification.

## Problem

Freely 当前已经有：
- `freely start`
- `freely chat`
- `freely tui`
- `freely live-status / baseline-status / fleet-status`

但它们还没有完全收敛成“一个统一的 Freely 前台控制面”：

1. 用户仍容易把 `start`、`chat`、`tui` 理解成几套不同系统，而不是同一个 `freely` control surface。
2. `chat` 是高层 human entrypoint，但 `tui` 仍有自己的提交路径细节，没有完全复用 `chat` 的 post-submit runtime chain。
3. CLI 输出已经形成可观测面，但还没有被明确冻结为 TUI / GUI 的 canonical backend interface。
4. 用户仍可能误以为需要直接进入外部 AI 工具的 TUI，而不是只使用 `freely`。

## Converged Direction

- `freely` 应是唯一正式前台命令。
- 外部 AI 工具只在后台由 runtime 调用；用户不应把 `codex` / `claude` / 其他工具的 TUI 当作主操作面。
- 非交互 CLI 面是 canonical interface：
  - `freely chat`
  - `freely status family`
  - `freely intake status`
  - 未来的 machine-readable snapshot
- `freely tui` 只是这个 canonical interface 的交互壳。
- 未来 GUI 也应复用同一接口，不另造业务语义。

## Immediate Gap

当前最小实现缺口不是 GUI，而是：

1. `cmd_tui` 提交消息后，没有像 `cmd_chat` 一样显式执行：
   - `ensure_interruption_dispatch_once`
   - `reactivate_worker_runtime_if_needed_after_chat`
2. 这意味着：
   - `tui` 虽然最终写的是同一个 intake
   - 但提交后链路还不完全等价于 `chat`
3. 因此当前还不能把 `tui` 和未来 GUI 放心地说成“只是共用 backend 的前端”

## Target

这条线要收敛的是：

- `freely` 作为唯一正式前台命令
- `chat` 作为 canonical submit primitive
- `tui` 调同一 submit contract
- CLI status family 作为 canonical observability backend
- 后续 TUI / GUI 只是不同渲染层

## Not This

这条线不先做：

- 真正的 Tauri GUI 实现
- 大规模桌面前端工程
- 直接去操纵外部 AI 工具 TUI

优先顺序应是：

1. 先把 CLI-first control surface contract 收稳
2. 再让 TUI 纯粹成为其交互层
3. 再让 GUI 复用同一 contract
