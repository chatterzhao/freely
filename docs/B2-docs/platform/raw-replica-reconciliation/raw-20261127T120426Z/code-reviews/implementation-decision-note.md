---
issue_id: I-20261127T120426Z-A
issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T120426Z/issues/I-20261127T120426Z-A.md
phase_state: completed
---

# Implementation Decision Note
- issue_id: I-20261127T120426Z-A
- issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T120426Z/issues/I-20261127T120426Z-A.md
- decision: 新增显式 comment-delete 封装，adapter 校验 local_id→平台 issue 映射后调用平台 handler 删除单条评论。
- why_this: 手工 gh api DELETE 会绕过唯一平台写通道；封装入口能保留审计与失败汇总。
- alternatives_considered: 自动删除所有重复评论——身份风险过高；放宽副本门禁忽略评论数——会掩盖真实漂移；GH_REPO="" 裁剪平台——wrapper 会重探 GitHub，无效。
- boundary_non_goals: 不自动删除 #4734 历史评论；不改 Gitee issue_comment 设置；不改创建路径。
- residual_risk: 评论属于平台对象，删除后无法从本地恢复；调用方必须显式确认 comment_id。
