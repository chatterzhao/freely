---
issue_id: I-20261124T054241Z-A
issue_path: docs/B2-docs/runtime/daemon/raw-20261124T054241Z/issues/I-20261124T054241Z-A.md
phase_state: completed
---

- issue_id: I-20261124T054241Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20261124T054241Z/issues/I-20261124T054241Z-A.md

## Implementation Decision Note
- decision: main() 汇总三类 outcome 计数并打印，failed>0 非零退出，slot_unavailable 视为待重试不计失败。
- why_this: fail-closed 原则；退出码是外部判断恢复健康的唯一契约，恒 0 会掩盖部分失败。
- alternatives_considered: 直接 raise（丢汇总、否决）；只打印不改码（外部仍误判、否决）。
- boundary_non_goals: 不改 resume_persisted_sessions 返回结构、不改 session/resume 调用、不改 DB/A2A 交互、不处理 watchdog_sse 的异常忽略（独立 issue）。
- residual_risk: slot_unavailable 计为成功可能掩盖 slot 持续不可用；由后续 manager/patrol 观察 session 健康兜底，本轮保持语义不变。
