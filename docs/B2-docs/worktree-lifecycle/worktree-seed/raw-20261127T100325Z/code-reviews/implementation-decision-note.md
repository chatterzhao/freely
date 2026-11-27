---
issue_id: I-20261127T100325Z-A
issue_path: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261127T100325Z/issues/I-20261127T100325Z-A.md
phase_state: completed
---

# Implementation Decision Note
- issue_id: I-20261127T100325Z-A
- issue_path: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261127T100325Z/issues/I-20261127T100325Z-A.md
- decision: 失败回执用 `${raw_key}` 显式变量边界。
- why_this: bash 在全角标点紧邻 `$var` 时将其纳入变量名，`set -u` 下抛错并掩盖平台部分失败事实。
- alternatives_considered: 改用 ASCII 括号——会改变既有中文回执风格；关闭 `set -u`——会削弱 fail-closed。
- boundary_non_goals: 不改 issue-sync 汇总、不改 #4731 判据。
- residual_risk: 扫描只覆盖 wt-create；其他脚本若有同类写法需另轮处理。
