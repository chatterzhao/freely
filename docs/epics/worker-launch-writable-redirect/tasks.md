# Tasks: Worker Launch 保护工位验证

## Dev

- [ ] `worker_prompt_launchable_for_manager_project` 增加 branch prefix 检查
  - 提取 `target_branch`（已有 L9706）
  - case 判断：`fix/*|feature/*` 放行，其他拒绝
  - 拒绝时 return 1 + `log_info` 输出错误原因
  - 空 branch 值放行
- [ ] 验证现有 test suite 不受影响
  - `test-freely-manager-worker-launch-linkage`
  - `test-freely-manager-exit-contract-autodelegates-cleanup-when-existing-prompt-is-nonlaunchable`
  - `test-freely-worker-prompt-worktree-header-compat`
  - `test-freely-worker-prompt-natural-language-contract-compat`
- [ ] 新增测试文件：`test-freely-worker-prompt-protected-branch-rejected`
  - develop → rejected
  - main → rejected
  - test-pre-merge-* → rejected
  - fix/* → accepted
  - feature/* → accepted
  - empty branch → accepted
- [ ] commit + merge 准备

## Post-merge

- [ ] 从当前 fix worktree merge-guarded 到 test-pre-merge → develop
