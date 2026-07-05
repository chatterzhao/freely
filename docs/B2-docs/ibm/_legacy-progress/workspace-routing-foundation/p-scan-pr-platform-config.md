# PR scan surface + FREELY_REPO_PLATFORMS config

- issue: `I-20260501-0000-A`
- issue_path: `docs/epics/workspace-routing-foundation/scan-pr-platform-config/issues/I-20260501-0000-A.md`
- candidate: `C-20260501-0000-A`
- candidate_path: `docs/B1-docs/raw-20260501-0000/candidates.md`
- milestone: `M-20260306-workspace-routing-foundation`
- phase_state: `done_pre_brainstorm`
- runtime_state: `verified_on_worktree`
- updated_at: `2026-05-03T15:30:00Z`
- next_action: `merge_to_develop_via_merge_guarded`

## Verification

- `FREELY_REPO_PLATFORMS` 配置正确加载到环境变量中
- 空配置时 `scan_repo_platform_prs()` 立即返回（向后兼容）
- `github` 映射到 `gh` CLI，`gitee` 映射到 `gitee` CLI
- PR snapshot 在 task-source-scan JSON 中生成 `open_pull_requests` 表面
- `governance-check` 无新增失败
