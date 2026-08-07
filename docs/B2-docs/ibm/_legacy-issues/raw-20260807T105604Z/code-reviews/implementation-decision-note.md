- issue_id: I-20260807T105604Z-A
- issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260807T105604Z/issues/I-20260807T105604Z-A.md

## Implementation Decision Note

- decision: 用 `git rm --cached` 解除 `.codex/config.toml` 跟踪，本地文件保留
- why_this: `.gitignore` 已忽略 `.codex/`，跟踪状态是历史遗留；untrack 是最小正确修复
- alternatives_considered: skip-worktree / example 模板 / 放宽 clean-tree 检查
- boundary_non_goals: 不做模板化、不改 clean-tree 检查、不新增配置面
- residual_risk: 历史提交仍含该文件内容；新克隆依赖 `freely init` / `sync-tooling` 物化本地配置
