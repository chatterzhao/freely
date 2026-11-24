---
issue_id: I-20261124T054217Z-A
issue_path: docs/B2-docs/gate/platform/raw-20261124T054217Z/issues/I-20261124T054217Z-A.md
phase_state: completed
---

- issue_id: I-20261124T054217Z-A
- issue_path: docs/B2-docs/gate/platform/raw-20261124T054217Z/issues/I-20261124T054217Z-A.md

## Implementation Decision Note
- decision: cmd-update 汇总 GitHub/Gitee 写结果，任一失败非零退出并打印 per-platform 摘要。
- why_this: fail-closed 与双平台一致性是项目核心原则；部分成功伪装成功会导致无人值守下静默漂移。
- alternatives_considered: 只修 Gitee（GitHub 仍吞，否决）；自动重试（引入重复写与幂等复杂，超 scope，否决）。
- boundary_non_goals: 不改 create/close/comment 写命令；不改幂等与生命周期；不引入重试。
- residual_risk: 其它平台写命令可能有同类吞失败模式，需独立 issue 审计（本轮不夹带）。
