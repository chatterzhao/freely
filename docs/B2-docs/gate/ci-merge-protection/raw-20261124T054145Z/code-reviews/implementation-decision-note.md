---
issue_id: I-20261124T054145Z-A
issue_path: docs/B2-docs/gate/ci-merge-protection/raw-20261124T054145Z/issues/I-20261124T054145Z-A.md
phase_state: completed
---

- issue_id: I-20261124T054145Z-A
- issue_path: docs/B2-docs/gate/ci-merge-protection/raw-20261124T054145Z/issues/I-20261124T054145Z-A.md

## Implementation Decision Note

- decision: 三处一起修——workflow 补 checks: write、pr-merge-guarded 的自签 check helper 改 fail-closed、develop 分支保护按 workflow 注释设置；分支保护排在代码合并并验证 CI 能建 check 之后执行，避免中间态卡死 PR。
- why_this: 三处断点互相掩盖，任一处单独修都无法让「禁止绕过门禁」成为可验证事实；fail-closed 是唯一不引入新绕过通道的语义。
- alternatives_considered: 只补权限（check 存在但无人强制，否）；补权限+保护但保留自签 fallback（仍有绕过通道，否）；GitHub Ruleset / 第三方 CI（超出本 raw 边界，延后到后续评估）。
- boundary_non_goals: 不改 check 名、不改 verify job、不改 SUMMARY 格式；不放宽任何既有 governance gate；不触碰平台 issue 生命周期；分支保护设置动作不在自动化回归内，本轮只验证结果。
- residual_risk: 分支保护依赖平台一次性设置，仓库重建/迁移需重配——已用 AT-003 的 API 读取证据兜底。实现期事实修正：全仓 grep 确认 `_set_governance_check_pass()` 只有定义、无调用点，自签 fallback 是死代码而非活跃绕过通道；仍按契约移除并改 fail-closed，消除未来被接线时的风险。证据：Grep 全工作树唯一命中为函数定义本身。
