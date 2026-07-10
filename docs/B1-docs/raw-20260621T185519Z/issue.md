---
local_id: raw-20260621T185519Z19Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3280'
    url: https://github.com/chatterzhao/freely/issues/3280
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T18:55:36Z'
updated_at: '2026-06-21T18:55:36Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 问题

`pr-merge-guarded` L408 直接执行了 `git push --delete`：

```bash
git push "$remote" --delete "$source_branch" 2>/dev/null || true
```

这是由 `bd92c578b6` (2026-06-13) 添加用于 Gitee 平台清理的。后续重构 `7a55e030d` (2026-06-15) 移除了 `gh pr merge --delete-branch`，但**遗漏了 L408**。

## 设计原则

分支生命周期归 `wt-close` 负责，`pr-merge-guarded` 只管 merge。

`pre-push` hook (L9-10) 当前**无条件放行**所有 `git push --delete`，无法拦截违规调用。

## 修复

1. **移除** `pr-merge-guarded` L408 的 `git push --delete`

2. **确认** `wt-close` 已有远程分支删除（Phase 4 L414-418）：
   - Gitee: `gitee API delete` → fallback `git push --delete`
   - GitHub: `git push --delete`
   - 之后 `git remote prune`

3. **加强** `pre-push` hook：`git push --delete` 只允许 wt-close 调用链路（和 reference-transaction hook 一样用进程树检测）

## 验证

- `pr-merge-guarded` 不再包含任何远程分支删除代码
- 手动 `git push origin --delete fix/raw-xxx` 被 pre-push hook 拦截
- `wt-close` 能正常删除远程分支

## 附录：所有绕过机制清单

| 机制 | 位置 | 绕过什么 | 是否验证 |
|------|------|---------|---------|
| `FREELY_SKIP_IBM_GATE=1` | hooks | IBM 治理门禁 | ✅ 只允许 governance-only |
| `FREELY_SKIP_CREATE_GATE=1` | hooks | 创建门禁 | ❓ 待查 |
| `wt-close --force` | wt-close | phase_state / pretests 检查 | 无验证 |
| `wt-close --skip-platform` | wt-close | 平台 issue 关闭 | 无验证 |
| `wt-close --discard-unmerged` | wt-close | 未合并提交保护 | 需 --force |
| `governance-merge-gate --skip-ibm-gate` | gate | IBM 生命周期验证 | ✅ 只允许 gov-only diff |
| `freely daemon start --force` | freely | daemon 启动检查 | 无验证 |
| `wt-create --force` | wt-create | 创建检查 | 无验证 |
| `pre-push` 放行 push --delete | hook | 远程分支删除 | ❌ **无任何限制** |
| `FREELY_WT_BYPASS_GUARD=1` | wt-close | worktree remove 保护 | ❌ 空 flag，hook 中不存在 |

后续需要为每个绕过机制加上 `--reason` / 调用者验证 / AI 拦截提示。

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
