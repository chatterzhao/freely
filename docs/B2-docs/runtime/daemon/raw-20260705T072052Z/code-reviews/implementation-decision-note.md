---
issue_id: I-20260705T072052Z-A
issue_path: docs/B2-docs/runtime/daemon/raw-20260705T072052Z52Z/issues/I-20260705T072052Z-A.md
phase_state: completed
---
- issue_id: I-20260705T072052Z-A
## Implementation Decision Note
- decision: daemon 启动 A2A server 前 truncate 日志
- why_this: 与 acp-bridge _truncate_log 行为一致，阻止无限膨胀
- alternatives_considered: logrotate / Python RotatingFileHandler → 过度设计
- boundary_non_goals: 不修改 a2a_server.py 内部日志逻辑
- residual_risk: 无。truncate 在启动时执行，不影响当前运行日志
