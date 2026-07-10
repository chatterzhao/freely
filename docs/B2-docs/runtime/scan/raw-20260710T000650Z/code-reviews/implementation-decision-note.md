---
issue_id: I-20260710T000650Z-A
issue_path: docs/B2-docs/runtime/scan/raw-20260710T000650Z/issues/I-20260710T000650Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260710T000650Z-A

## Implementation Decision Note

- decision: 1) pre-scan-fix.sh 批量处理 terminal phase 本地文档，走 workflow + --skip-ibm; 2) scan raw_key → platform_id fallback
- why_this: 636 items 是纯本地文档残留，不应进入 Manager AI cycle；platform_ids 缺失用 raw_key 回退是最小改动
- alternatives_considered: 静默跳过 — 用户要求脚本自动修复而非跳过; 每个 item 单独 raw issue — 用户要求批量处理
- boundary_non_goals: 不修改 issue-sync batch 命令；不改变 Manager prompt 构建逻辑
- residual_risk: pre-scan-fix.sh 在无平台 API 环境下优雅降级（检查无 items 则 skip）
