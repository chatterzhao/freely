# 研究：Doc-loop 治理维护职责补全（Constitution / Laws / Skills）

## Context

- 日期：2026-03-05 14:02 UTC
- 触发：Freely 自举执行中，doc-loop 语义被收敛为 `IBM`，但对“治理资产维护”职责不够显式，导致执行偏向业务文档产物，弱化宪法/法律/skills 的持续维护。
- 约束：遵循宪法第 11、16 章与法律第 11、16 章，先 pre-brainstorms，再进入 doc/dev 落地。

## 现状问题

1. `doc-loop-execution` 以 `IBM` 为主，治理文档维护仅以“如需变更规范文档”方式出现，不足以形成默认职责。
2. 法律第 11 章对 doc-loop 的验收描述偏抽象，未明确“治理资产维护”在 doc-loop 内的可验收证据。
3. 结果是执行中容易出现“先写业务文档，治理资产后补”甚至遗漏。

## 收敛判断

Doc-loop 应采用“双轨语义”：
- 业务轨：`IBM`（issue 接入、brainstorm、mapping）
- 治理轨：`G`（Constitution / Laws / Skills 一致性维护）

治理轨不替代业务轨，但在以下场景必须触发：
- 出现治理漂移（宪法/法律/skills 与当前执行链冲突）
- 出现术语/路由/证据口径不一致
- 发生 dogfooding 规则收敛或门禁语义调整

## 最小变更原则

1. 不新增第四层循环；仍保持三层循环（auto/doc/dev）。
2. 在 doc-loop 内显式纳入治理维护职责（`IBM + G`）。
3. 验收仍由法律门禁裁决，不把步骤写进法律正文。

## 结论

该问题已具备 issue-ready 条件，应晋升为 P0 候选并进入落地。

