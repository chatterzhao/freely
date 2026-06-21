---
local_id: raw-20260621T190007Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '3281'
    url: https://github.com/chatterzhao/freely/issues/3281
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T19:00:24Z'
updated_at: '2026-06-21T19:00:24Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

# feat: comprehensive gate enforcement — hard block raw git ops, soft block with --reason

## 设计原则

门禁分两类：

### 绝对禁止（硬拦截，无绕过方法）

这些原子 git 操作在任何情况下都不允许直接执行，必须通过封装命令：

| 禁止的操作 | 正确方式 |
|-----------|---------|
| `git branch <name>` | `wt-create` |
| `git branch -d/-D` | `wt-close` |
| `git worktree remove` | `wt-close` |
| `git push --delete` | `wt-close`（Phase 4） |
| `git push --force develop/main` | 永不允许 |
| `git commit` on develop/main | `pr-merge-guarded` |
| `git push` fix/feature/test 分支 | `pr-create-guarded` |

硬拦截被触发时的提示：

```
[GATE] 违规操作被拦截: <具体操作>

  此操作在任何情况下都不允许直接执行。
  正确方式: <封装命令>

  这是硬性门禁，无法绕过。
```

### 允许绕过但必须给理由（软拦截）

封装命令自身的 --force / --skip-* 等 flag，设计上允许绕过，但必须带 --reason：

| 命令 | Flag | 绕过什么 | 当前状态 |
|------|------|---------|---------|
| `wt-close` | `--force` | phase_state / pretests 检查 | 有 --reason 参数但不强制 |
| `wt-close` | `--skip-platform` | 平台 issue 关闭 | 无 --reason |
| `wt-close` | `--discard-unmerged` | 未合并提交保护 | 无 --reason |
| `freely init` | `--force` | 已有配置覆盖 | 无 --reason |
| `freely start` | `--force` | 启动检查 | 无 --reason |
| `freely daemon start` | `--force` | daemon 启动检查 | 无 --reason |
| `freely task-mode set` | `--force` | task-mode 检查 | 无 --reason |
| `pr-review-guarded` | `--verdict` | 审查维度判定 | 无 --reason |
| `governance-merge-gate` | `--skip-ibm-gate` | IBM 生命周期验证 | ✅ 已有限制（gov-only diff） |
| `FREELY_SKIP_IBM_GATE=1` | (多处) | IBM 治理门禁 | ✅ 已有限制 |
| `FREELY_SKIP_CREATE_GATE=1` | pre-push | 创建门禁 | ✅ 已有限制（docs-only） |
| `FREELY_WT_BYPASS_GUARD=1` | wt-close | worktree remove 保护 | ❌ hook 中不存在 |
| `FREELY_FORCE_WATCHDOG_REPROBE=1` | watchdog | 重新探测 | 无 --reason |

软拦截被触发时的提示：

```
[GATE] 你在违规绕过门禁: <门禁名称>

  本次操作绕过了以下检查: <列出被绕过的具体检查项>
  
  请严格执行门禁。如果确实满足绕过条件（不是偷奸耍滑），
  请查看该命令支持的绕过参数，加上:
    --reason "具体绕过原因"

  示例: ./bin/wt-close --force --reason "emergency cleanup: worktree corrupted" <branch>
```

## 修复清单

### A. 硬拦截

1. **pre-push hook**: `git push --delete` 改为硬拦截
   - 当前 L9-10 无条件放行所有 `git push --delete`
   - 改为：检测调用者进程树，只允许 wt-close 调用链路
   - 非 wt-close → 硬拦截，提示 "删除远程分支必须通过 wt-close"

2. **reference-transaction hook**: `FREELY_WT_BYPASS_GUARD=1` 加调用者检测
   - 当前此环境变量在 hook 中完全不存在
   - 改为：检测调用者，只允许 wt-close 使用，否则硬拦截

### B. 软拦截（--reason 强制）

3. **wt-close**: `--force` / `--skip-platform` / `--discard-unmerged` → 无 `--reason` 则阻塞
4. **freely init**: `--force` → 无 `--reason` 则阻塞
5. **freely start / daemon start**: `--force` → 无 `--reason` 则阻塞
6. **freely task-mode set**: `--force` → 无 `--reason` 则阻塞
7. **pr-review-guarded**: `--verdict` 必须带 `--reviewer` + `--reason`
8. **FREELY_FORCE_WATCHDOG_REPROBE=1**: 加审计日志
9. 所有绕过操作写入审计日志（append_runtime_event / skip-gate.log）

### C. pr-merge-guarded 清理

10. **移除 L408** `git push "$remote" --delete "$source_branch"`（已在 #3280 跟踪）

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
