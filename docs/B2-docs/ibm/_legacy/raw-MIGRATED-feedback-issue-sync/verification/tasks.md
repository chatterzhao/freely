# Tasks: cmd_feedback → issue-sync alignment

- issue_id: raw-20260624T141559Z59Z

## Task List

### T1: 重写 cmd_feedback 函数 ✅
- 文件: `docs/system/workspace/scripts/runtime/freely`
- 改动: 去掉 `--repo` 参数，写本地 `docs/issues/` 文件，调用 `issue-sync create`
- 状态: completed

### T2: 删除 _resolve_gh_repo() ✅
- 文件: `docs/system/workspace/scripts/runtime/freely`
- 改动: 删除不再使用的 helper 函数
- 状态: completed

### T3: 修复 crash reporter ✅
- 文件: `docs/system/workspace/scripts/runtime/freely` L21465
- 改动: 去掉 `--repo "$FREELY_REPO_URL"`
- 状态: completed

### T4: 更新 --help ✅
- 文件: `docs/system/workspace/scripts/runtime/freely`
- 改动: 更新 usage 文本，移除 `--repo`，添加 auto-detection 说明
- 状态: completed

### T5: 功能测试 ✅
- 环境: test-pre-merge worktree
- 覆盖: help 输出、参数校验、错误处理、E2E 创建
- 状态: completed

### T6: B1_IBM 治理 ⬜
- 产物: brainstorms.md + candidates.md + milestones.md
- 状态: completed (commit d5d8e70d7)

### T7: B2_IBM 治理 ⬜
- 产物: prd.md + pre-tests.md + tasks.md + code-review
- 状态: in_progress

### T8: pr-create-guarded ⬜
- 状态: pending

### T9: pr-review-guarded ⬜
- 状态: pending

### T10: pr-merge-guarded ⬜
- 状态: pending

### T11: wt-close ⬜
- 状态: pending
