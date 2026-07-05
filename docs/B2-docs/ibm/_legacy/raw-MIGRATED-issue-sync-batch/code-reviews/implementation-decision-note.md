---
issue_id: I-20260625T061044Z-A
issue_path: docs/issues/I-20260625T061044Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260625T061044Z-A
- issue_path: docs/issues/I-20260625T061044Z-A/issue.md

## Implementation Decision Note

- decision: 在 cmd_daemon_start 中 platform 检测后、scan 前运行 issue-sync batch
- why_this: 机械同步不需要 AI判断，放在 daemon 启动时清除可减少 Manager token
- alternatives_considered: 单独脚本定期 cron → 需要额外调度；scan 内嵌 → 耦合
- boundary_non_goals: 不创建复杂的自动化 pipeline
- residual_risk: batch 失败不阻塞 daemon 启动（log_warn）
