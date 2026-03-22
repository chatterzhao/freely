# PRD

## Goal

让 `freely` 成为唯一正式 front-door command，并让 `chat` / `tui` 共用同一个 high-level runtime submit contract。

## Requirements

1. `tui` 提交消息后，必须与 `chat` 走同一 post-submit chain。
2. CLI status family 作为 canonical backend interface 被正式写清。
3. 真源明确未来 TUI/GUI 复用同一 contract。

## Non-Goals

- 不在本 issue 内实现 Tauri GUI
- 不把外部 AI 工具 TUI 重新拉回主路径
