---
local_id: raw-20260519T190823Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '743'
    url: https://github.com/chatterzhao/freely/issues/743
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-19T19:08:38Z'
updated_at: '2026-05-19T23:09:08Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-19T23:09:08Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## raw-20260519T190823Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260519T190823Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-05-19T19:08:23Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260519T190823Z`。实现前请用 `wt-create --raw-key 20260519T190823Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
phase_state: absorbed
source: feedback
created_at: "2026-05-19T19:08:23Z"
title: "governance gate dropped 被滥用作 fix 合并捷径"

## 问题

门禁允许 `phase_state=dropped` 作为 B1 终态放行。但实际使用中，完成了代码修改后直接标 `dropped` 绕过 IBM 治理链。

今天 4 个 fix 全是：代码写完了 → pr-merge-guarded 合并 → raw issue 标 dropped。dropped 语义是丢弃不推进，但实际代码已合并推进了。

## 修复方向

门禁在 `phase_state=dropped` 时应检查：

1. merge diff 是否包含代码变更（不只是 docs）？
   → 如有代码变更，dropped 不适用——代码已合并，不能假装丢弃
2. `dropped_reason` 是否写的是"fix merged to develop"等实际推进的描述？
   → 如果 reason 表明代码已合并，拒绝 dropped，要求走 absorbed 或 promoted
3. dropped 应只允许以下场景：
   - 代码从未提交，raw issue 被废弃
   - merge 内容仅为 raw issue 文件本身（批量吸收/清理）
   - 预研结论为"不做"，无代码产出

## 正确路径

fix 完成后应有 B1 brainstorm + candidate → I-* issue → 代码合并 → raw absorbed 到 I-* 链
