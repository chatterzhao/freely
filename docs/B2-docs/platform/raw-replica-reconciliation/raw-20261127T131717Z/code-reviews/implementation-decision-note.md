---
issue_id: I-20261127T131717Z-A
issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T131717Z/issues/I-20261127T131717Z-A.md
phase_state: completed
---

# Implementation Decision Note
- issue_id: I-20261127T131717Z-A
- issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T131717Z/issues/I-20261127T131717Z-A.md
- decision: 平台身份只由规范标题前缀判定，正文提及不再参与。
- why_this: 正文引用是治理留痕，不是副本；把它当身份会让 create 永久 indeterminate。
- alternatives_considered: 放宽 create 的 indeterminate 拒绝——会制造重复副本；按 body 精确匹配并去重——正文措辞不可控，仍会误判。
- boundary_non_goals: 不改 raw_title_contract、不改 create 策略、不改平台写通道。
- residual_risk: legacy 无前缀标题不会被发现；此类副本须通过显式平台参数处理，不自动猜测。
