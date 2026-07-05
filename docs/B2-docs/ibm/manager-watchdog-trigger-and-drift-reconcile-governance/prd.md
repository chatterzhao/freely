# PRD: manager-watchdog-trigger-and-drift-reconcile-governance

## Goal

让 Freely 的主管 watchdog 语义从分散描述变成一致的三层 loop 真源表达，避免后续 AI 只读片段就误解主管职责或 loop 边界。

## Requirements

1. `auto-loop` 明确同时支持 `patrol-driven` 与 `event-driven` 入口。
2. verification / writeback / cleanup 被明确归回三层 loop 现有边界，不形成第四层。
3. 主管始终只做判断、解释、委派与监督完成。
4. delegated result 返回后，主管继续做 restart-point routing。
5. `external drift / out-of-band reconcile` 被明确纳入主管 patrol 检查面。
