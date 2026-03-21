# PRD: milestone-planning-and-state-maintenance

## Problem

milestone 是 Freely 的 standing source 和编排入口，但排期、状态维护与跨产物 reconcile 长期缺少明确 owner。

## Product Requirement

Freely 必须把 milestone planning / state maintenance 定义成专门 worker 能力，由 manager 在 standing-source scan 下按需委派，负责 sequencing 与状态写回一致性。

## Non-goals

- 不让该 worker 直接写业务代码
- 不让该 worker 替代 manager 做顶层优先级裁决
- 不把所有文档维护都混成 milestone maintenance
