---
local_id: raw-20260629T030408Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260629T030408Z-A
platform_ids:
  github:
    issue_id: '3617'
    url: https://github.com/chatterzhao/freely/issues/3617
    synced_at: ''
  gitee:
    issue_id: IJXH5I
    url: https://gitee.com/zhaoquan/freely/issues/IJXH5I
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-29T03:04:29Z'
updated_at: '2026-06-29T03:04:29Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---


## 问题

之前将 skill 名从 `freely-feat-execution` 重命名为 `freely-feature-execution`，但未完成：

1. **wt-create 仍校验 `freely-feat-execution`**，拒绝 `freely-feature-execution`
2. 多个活跃脚本、hooks、AGENTS.md 仍引用 `freely-feat-execution`
3. AGENTS.md 流程描述仍用 `feat:` 简写

## 波及文件（8个活跃代码文件，17处）

| # | 文件 | 行 |
|---|------|-----|
| 1 | `docs/system/workspace/scripts/worktree/wt-create` | 7,13,15,73,74,174,760 |
| 2 | `docs/system/workspace/scripts/runtime/freely` | 6549,8480,23578,23703 |
| 3 | `docs/system/workspace/scripts/worktree/wt-close` | 924 |
| 4 | `docs/system/workspace/scripts/worktree/pr-create-guarded` | 138 |
| 5 | `docs/system/workspace/scripts/tests/test-wt-close-protected-branch-guard` | 82 |
| 6 | `.githooks/pre-commit.sh` | 282 |
| 7 | `.githooks/reference-transaction.sh` | 116 |
| 8 | `AGENTS.md` | 25 |

## 验收标准

1. 全仓 `grep -r "feat-execution\|freely-feat"` 在活跃代码（scripts/hooks/skills/agents/AGENTS.md）中零命中
2. `freely-feat-execution` 改为 `freely-feature-execution`
3. `feat:` 流程简写改为 `feature:`
4. wt-create 接受 `freely-feature-execution` 为合法 skill

