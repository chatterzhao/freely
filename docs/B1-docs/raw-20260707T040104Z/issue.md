---
local_id: raw-20260707T040104Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3793'
    url: https://github.com/chatterzhao/freely/issues/3793
    synced_at: ''
  gitee:
    issue_id: IJZBJJ
    url: https://gitee.com/zhaoquan/freely/issues/IJZBJJ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-07T04:01:25Z'
updated_at: '2026-07-07T04:01:25Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

pre-commit.sh 的 develop 拦截消息列出了禁止的绕过命令，但漏了 `git update-ref develop`——这是一种 plumbing 级别的绕过方式，应该明确禁止。

## 改动

1. `.githooks/pre-commit.sh`: 在 develop 拦截消息的禁止列表中增加 `❌ git update-ref develop (plumbing 绕过,严禁)`
2. `SKILL.md`: 铁律 ZERO 注释区已有此项，本次确认不重复

## 范围

仅 pre-commit.sh 1 行文本插入。
