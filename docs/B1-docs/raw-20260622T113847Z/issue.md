---
local_id: raw-20260622T113847Z47Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260622T113847Z-A
platform_ids:
  github:
    issue_id: '3354'
    url: https://github.com/chatterzhao/freely/issues/3354
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T11:39:07Z'
updated_at: '2026-06-22T11:39:07Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 问题

wt-close 孤儿模式（工位已删除）当前跳过 platform close，导致平台 issue 泄漏。
需要一个新的 `--platform-only` 参数，只关闭平台 issue，不改动本地文件。

## 设计

```
wt-close --platform-only <branch> --reason "..."

只做:
  1. 从 branch 提取 raw key
  2. 读 $PROJECT_ROOT/docs/B1-docs/raw-xxx/issue.md（只读，不动 develop）
  3. 获取 raw issue 的 GitHub issue number → API close
  4. 读 absorbed_into → 获取 I-* issue
  5. 如果 I-* phase=completed 且 platform_state!=closed → 同样 API close
  6. 不写本地 issue.md（platform_state 保持 open，下次 scan 同步修正）

不做:
  - 不改 develop 上任何文件
  - 不删分支
  - 不改 phase_state

适用场景:
  - 工位已被删除，但平台 issue 仍然 OPEN 的孤儿 issue
  - 已有 15 个已知孤儿需要此功能收口

## --skip-platform 文档更新

同时更新 --skip-platform 的文档，明确唯一合法场景:
  "平台 issue 已通过其他渠道手动关闭，无需同步"

## 涉及文件

- `docs/system/workspace/scripts/worktree/wt-close` — 新增 --platform-only 参数 + Phase 2 platform close 逻辑
- `docs/system/workspace/scripts/worktree/wt-close` — --help 中补充 --platform-only 说明

🤖 Generated with [Claude Code](https://claude.com/claude-code)
