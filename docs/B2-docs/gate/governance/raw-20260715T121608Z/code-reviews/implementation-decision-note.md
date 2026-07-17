---
issue_id: I-20260715T121608Z-A
issue_path: docs/B2-docs/gate/governance/raw-20260715T121608Z/issues/I-20260715T121608Z-A.md
phase_state: completed
---

- issue_id: I-20260715T121608Z-A
- issue_path: docs/B2-docs/gate/governance/raw-20260715T121608Z/issues/I-20260715T121608Z-A.md

## Implementation Decision Note

- decision: 工位 scope 内收敛 3 I-* completed（附 merge 实证）+ C-20260612 milestones 历史补锚；13 个跨 raw 终态收敛被 GATE 1（工位隔离）实拦后移交 runtime manager 治理通道（证据随 chat 指令下发）；6 个欠账/无据项显式留档
- why_this: 状态真源只能跟证据走；07-15 scanner 计数（15/13）与今日现状的差额已被日常 lane 消化，如实按今日证据收敛
- alternatives_considered: 按 07-15 清单盲改（部分已收敛、部分无证据，否）；等 runtime worker 处理（已实测 worker ACP init 超时且无产出移除工位，否）
- boundary_non_goals: 不动无 merge 证据的 3 个 legacy I-*；不修 worker ACP init 超时缺陷（另案跟进）
- residual_risk: absorbed 无 I-* 锚的 13 个 raw 若未来 gate 收紧需 archive 线补锚；3 个欠账 I-* 的历史 RED-GREEN 补章属欠账治理线 scope，本 lane 不代偿
