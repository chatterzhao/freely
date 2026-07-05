# PRD: Worker Launch 保护工位验证

## Goal

消除 worker 在保护分支（develop/main/test-pre-merge-*）启动导致 hook 拦截、快速退出、restart storm 的根因链。
Runtime 层验证 worker target branch 必须是可写工位（fix/*/feature/*），否则拒绝 launch 并报明确错误。

## Background

参见 `docs/B1-docs/raw-20260509T022152Z52Z/brainstorms.md` 根因分析。

## Dev-Loop Handoff

### 改点

**文件**: `docs/system/workspace/scripts/runtime/freely`
**函数**: `worker_prompt_launchable_for_manager_project()` (L9695)

在 L9706 `target_branch` 提取后，增加 prefix 检查：

```bash
case "$target_branch" in
  fix/*|feature/*) ;;  # OK
  *)
    log_info "worker target branch '%s' is a protected branch; worker must target fix/* or feature/*. Manager should update continuity to delegate to a writable worktree." "$target_branch"
    return 1
    ;;
esac
```

若 `target_branch` 为空字符串或无法提取，**放行**（不破坏已有流程）。

### Non-goals

- 不修改 AI prompt 生成
- 不修改 worker_prompt_resolved_worktree
- 不做自动重定向
- 不触及 hotfix/release 判断
