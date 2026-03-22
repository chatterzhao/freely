# PRD: manager-chat-reentry-and-cleanup-misrouting-governance

## Goal

让广义主管巡检 chat 在 interruption 路径中，重新进入 manager continuation，而不是被 cleanup followthrough 过早吸收。

## In Scope

- interruption manager prompt routing
- delegated continuation absorption
- cleanup path preservation

## Out of Scope

- 新的 event bus
- supervisor 常驻聊天会话
- 完整 patrol 自动化
