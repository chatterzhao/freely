---
local_id: raw-20260621T063130Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T063130Z-A
platform_ids:
  github:
    issue_id: '3204'
    url: https://github.com/chatterzhao/freely/issues/3204
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T06:31:48Z'
updated_at: '2026-06-21T20:13:34Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

`wt-create` 创建 fix 工位时同时创建了 test-pre-merge 工位，两者通过 raw-key 关联：
- fix 分支: `fix/raw-{raw_key}-{slug}`
- test-pre-merge 分支: `test-pre-merge-{raw_key}-{slug}`

但 `wt-close` 只关闭指定的 fix 分支，不清理配对的 test-pre-merge。test-pre-merge 文档说是"disposable test sandbox"，但没有自动清理机制。

## 设计

raw-key 是通用标识符，所有命名都是确定的。`wt-close` 关闭 `fix/raw-{raw_key}-{slug}` 时：
1. 从分支名解析 raw_key 和 slug
2. 推导 test-pre-merge 分支: `test-pre-merge-{raw_key}-{slug}`
3. 检查分支/工位是否存在
4. 存在则一并关闭（test-pre-merge 是 disposable，跳过检查和 platform close）

无需额外存储关系——raw-key 就是关联键。
