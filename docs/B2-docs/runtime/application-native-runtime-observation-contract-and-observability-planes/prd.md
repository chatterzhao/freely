# PRD: application-native-runtime-observation-contract-and-observability-planes

## Problem

Freely 现在有观察信号，但没有统一的应用无关 contract 去说明：

- 先看什么
- 怎么判断还在推进
- 怎么判断已经空转
- 怎么把状态、会话、流、artifact 暴露给用户和主管

## Product Goal

建立一套可复用的 `application-native runtime observation contract`，让 Freely self-host 成为第一份 concrete profile，并让未来任意应用都能挂接自己的 observation surfaces。

## Requirements

1. 冻结五个 observation planes 与最小 identity block
2. 冻结 `progress signal / stall signal / acceptance evidence` 三类 schema
3. 冻结 CLI / TUI / GUI / API 共享的最小 `status card` 与 `deep ref group` contract
4. 明确 artifact plane 才是 `acceptance evidence` 的 canonical truth surface
5. 明确 current-state / fleet / API 只镜像最小摘要与 `acceptance_ref`
6. 保留 richer runtime / UI productization 为 follow-on scope

## Non-Goals

1. 不在本 issue 直接实现完整 GUI/TUI 产品面
2. 不把 Freely 自己的 `live-status/jsonl/cycle log` 写死成所有应用唯一观察法
3. 不把多 subagent day-1 提升为独立 backend 一等实体

## Success Criteria

- issue completion 与 delete gate 的观察 contract 共享同一套 acceptance evidence schema
- Freely self-host profile 被写清且不妨碍 future app 泛化
- 后续 richer runtime / UI productization 不再需要重开基础 contract 争论
