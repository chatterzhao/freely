# Implementation Decision Note
- issue_id: I-20260509T022152Z-A
- issue_path: docs/issues/I-20260509T022152Z-A/issue.md
- decision: worker_prompt_launchable_for_manager_project 在已提取 target_branch 后增加 shell case prefix 检查；仅 fix/* 和 feature/* 允许通过，其他 branch 返回 1（not launchable）
- why_this: 对根因链最精确的修复——改动仅限于一个函数（L9695-9717），已有 WORKER_PROMPTS_NOT_LAUNCHABLE 处理路径（L13177）直接复用，符合最小作用域原则
- alternatives_considered: 自动重定向到配对工位（主管可能选错工位，runtime 猜测不可靠）；prompt 生成时检查（影响更大）；hook 层友好提示（hook 已是第二道防线）
- boundary_non_goals: 不改 worker_prompt_resolved_worktree（路径解析和 branch 验证是两层职责）；不改 AI prompt 格式（主管侧修正 worktree 路径就能通过）；不改 hotfix/release 判断
- residual_risk: 若将来出现合法非 fix/feature worker target（如 release/* 临时维护）会误拒——缓解：放行 hotfix/* 作扩展点，空 branch 值已放行；被拒后已有 WORKER_PROMPTS_NOT_LAUNCHABLE -> resume_invalid 路径，不会无限重启
