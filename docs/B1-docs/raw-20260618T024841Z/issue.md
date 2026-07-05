---
local_id: raw-20260618T024841Z41Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260618T024841Z-A
platform_ids:
  github:
    issue_id: '2959'
    url: https://github.com/chatterzhao/freely/issues/2959
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T02:48:57Z'
updated_at: '2026-06-21T20:12:52Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

对 #2956 实现的评审发现三个系统性问题：

### 1. raw issue 审计覆盖不全

声称"全量路径审计"但实施中发现了 4 个遗漏：
- `_fill_platform_ids` (行357): 仍用 `$ROOT_DIR/docs/issues/`
- `worktree-common.sh` wrapper: source 脚本路径在 worktree 中找不到
- `pr-create-guarded`: 缺少 worktree 清洁度检查
- `pr-create-guarded`: 缺少 phase_state 检查

根因：审计时只 grep 了 `docs/issues`，没有追踪完整的函数调用链。

### 2. candidate acceptance_criteria 与实际实现不一致

| candidate 写的 | 实际实现的 |
|---|---|
| wt-close 使用 git rev-parse 解析 ROOT_DIR | 使用 config.toml 推导 PROJECT_ROOT/PROJECT_WORKTREES_ROOT |
| worktree-common.sh 使用 git rev-parse | 使用 git worktree list 找主仓库 |

实际实现比 candidate 写的更好，但 candidate 没有更新——实施过程中的设计演进没有回写到治理文档。

### 3. raw issue 数据丢失风险

当前架构下 raw issue 在 worktree 的 docs/issues/ 中。wt-close 删除 worktree 后：
- raw issue 通过 merge 进入了 develop 的 docs/issues/ ✅
- 但如果在 develop 上再次 wt-close --force（清理残留），可能覆盖 develop 上的 raw issue
- raw-20260617T103956Z53Z 的 worktree 被删后，本地 raw issue 文件丢失

## 修复方向

1. **预研阶段**：路径审计工具应追踪函数调用链，不只是 grep 字面量
2. **实施阶段**：发现 candidate 与实际不一致时，必须回写 candidate
3. **收口阶段**：wt-close 应确保 raw issue 已存在于 develop 的 docs/issues/（通过 merge），再删除 worktree。如果 raw issue 仅在 worktree 中存在，应先 copy 到 develop
