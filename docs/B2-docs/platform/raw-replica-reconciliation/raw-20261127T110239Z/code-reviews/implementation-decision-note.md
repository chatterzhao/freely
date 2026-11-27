---
issue_id: I-20261127T110239Z-A
issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T110239Z/issues/I-20261127T110239Z-A.md
phase_state: completed
---

# Implementation Decision Note
- issue_id: I-20261127T110239Z-A
- issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T110239Z/issues/I-20261127T110239Z-A.md
- decision: 评论前查状态、翻译 Gitee 401、promote-finalize 重跑幂等。
- why_this: 裸 401 混淆鉴权/路径/平台状态；重跑制造重复评论并阻塞副本对账。
- alternatives_considered: 自动开启 issue_comment——会改变仓库治理设置；删除重复评论——需独立封装与确认；用 GH_REPO="" 裁剪平台——wrapper 会从 git remote 重探，无效。
- boundary_non_goals: 不改平台设置、不删已有评论、不实现单平台裁剪。
- residual_risk: Gitee 状态读取失败时按 unknown 处理并继续 POST；真实 401 会被翻译层捕获。
