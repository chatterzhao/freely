---
issue_id: I-20260627T084523Z-A
issue_path: docs/issues/I-20260627T084523Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260627T084523Z-A
- issue_path: docs/issues/I-20260627T084523Z-A/issue.md

## Implementation Decision Note

- decision: sync_tooling 写入前加 reconcile + count + pick 三步；wt-close 加 session/close
- why_this: 两条 agent-id.env 写入路径保持一致；ACP 协议优雅关闭优于强杀
- alternatives_considered: 只修 patrol 路径不修 sync_tooling（无法根治绕过）；在 Phase 6 而非 Phase 4.5 关 session（太晚，PID 可能已被强杀）
- boundary_non_goals: 不拦截 git worktree remove（原生 git 命令无法 hook）；不改 manager patrol 并发逻辑（已正确）
- residual_risk: reconcile 依赖 agent-id.env 文件读取正确性；session/close 依赖 bridge socket 存活
