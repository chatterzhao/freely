---
local_id: raw-20260621T194436Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3284'
    url: https://github.com/chatterzhao/freely/issues/3284
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T19:44:53Z'
updated_at: '2026-06-21T19:44:53Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

Manager 在每轮 patrol 中可能对同一个 scan item 重复调用 `freely feedback`，创建多个 raw issue 指向同一实际问题。这导致：

1. 重复的 raw issue（同一问题多个 GitHub issue）
2. 重复的 `wt-create`（不同 raw_key，不同分支，但做同一件事）
3. 重复的 Worker 委派（僵尸进程累积）

## 修复

在 `freely feedback` 的用法提示中，加入去重指引：

```
创建 raw issue 前，先搜索是否已有 open 的同类 issue:

  gh issue list --repo <repo> --search "关键词 in:title" --state open

如果已有 title 相似的 open issue，复用现有 raw issue:
  - 在已有 issue 下 comment 补充信息
  - 用已有的 raw_key 创建/复用工位 (wt-create --raw-key <已有key>)

如果确认需要新建 raw issue:
  freely feedback --repo <repo> --title "..." --body "..."
```

## 改动范围

仅修改 `freely` runtime 中 `cmd_feedback` 函数的用法提示文本，不涉及逻辑变更。

可使用 FREELY_SKIP_IBM_GATE=1 绕过门禁（仅提示词修改）。

## 验证

- `freely feedback --help` 显示去重指引
- Manager prompt 中包含此指引 → Manager 行为改善

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
