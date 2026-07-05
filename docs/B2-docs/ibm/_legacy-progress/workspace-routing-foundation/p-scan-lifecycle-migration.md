# Progress: scan-lifecycle-migration

- issue_id: `I-20260503-0200-A`
- issue_path: `docs/B2-docs/runtime/scan-lifecycle-migration/issues/I-20260503-0200-A.md`
- title: `scan: switch to task-lifecycle-scan v2 with full lifecycle chain trace`
- phase_state: `in_dev`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/scan-lifecycle-migration`
- updated_at: `2026-05-03`
- session_refs:
  - {tool: ccds, session_id: "20260503-scan-lifecycle", role: "author"}

## Summary
- 切换到 task-lifecycle-scan v2，扫描从 147 条噪声降到 35 条精准输出
- 完整生命周期链条追踪（12 mandatory + 2 optional stations）
- Chat inbox 信号扫描，分支命名规范强制
- AF_UNIX socket 用 hash 短路径
