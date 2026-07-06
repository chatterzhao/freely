# Tasks: Worker Launch 保护工位验证

## Dev

- [x] `worker_prompt_launchable_for_manager_project` 增加 branch prefix 检查
  - 提取 `target_branch`（已 L9706）
  - case 判断：`fix/*|feature/*` 放行，其他拒绝
  - 拒绝时 return 1 + `log_info` 输出错误原因
  - 空 branch 值放行
- [x] 验证现有 test suite 不受影响
  - `test-freely-worker-prompt-worktree-header-compat` — PASS
  - `test-freely-worker-prompt-natural-language-contract-compat` — PASS
  - `test-freely-manager-worker-launch-linkage` — pre-existing infrastructure failure (needs ACP bridge)
  - `test-freely-manager-exit-contract-autodelegates-cleanup-when-existing-prompt-is-nonlaunchable` — pre-existing failure (unrelated to this change)
- [x] 新增测试文件：`test-freely-worker-prompt-protected-branch-rejected`
  - develop → rejected ✅
  - main → rejected ✅
  - test-pre-merge-* → rejected ✅
  - release/* → rejected ✅
  - fix/* → accepted ✅
  - feature/* → accepted ✅
  - empty branch → accepted ✅
- [x] commit + merge 准备 — committed as d5dd570c

## Post-merge

- [x] 从当前 fix worktree pr-merge-guarded 到 test-pre-merge → develop
  - merge already completed; fix commit d5dd570c confirmed in develop
