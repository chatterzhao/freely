# Brainstorm: cli-first-entrypoint-and-observability-surface-unification

## Core Decision

Freely 的前台入口要收敛成：

- `freely` 是唯一正式 front-door command
- `chat` 是 canonical high-level submit primitive
- `tui` 只是交互壳，不应再有自己的一套 post-submit 运行语义
- 未来 GUI 也复用同一 backend contract

## Immediate Implementation Cut

当前最小实现不是 GUI，而是：

1. 抽一个 shared human front-door submit helper
2. 让 `cmd_chat` 和 `tui_submit_message` 都走它
3. 这样 `tui` 在提交后也会自然继承：
   - runtime bootstrap
   - dispatcher ensure
   - worker runtime reactivation gate

## Observability Position

CLI-first 的意思不是只有 CLI，没有 TUI/GUI，而是：

- CLI status family 是 canonical backend interface
- TUI/GUI 只是展示层 / 交互层
- 不再把外部 AI 工具 TUI 当作主产品面
