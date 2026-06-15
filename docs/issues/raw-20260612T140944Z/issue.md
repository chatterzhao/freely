---
local_id: raw-20260612T140944Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2569'
    url: https://github.com/chatterzhao/freely/issues/2569
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/issues/I-20260612T140944Z-A/issue.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-12T14:10:01Z'
updated_at: '2026-06-13T01:10:00Z'
intake_id: ''
author: platform
channel: github
session_refs:
- fix/raw-20260612T140944Z-a2a-handoff-compat
---

原始 scope: a2a_tasks 表 raw_key 列 INSERT 遗漏。

经过 B1_IBM 预研后，scope 扩大为：彻底将 Freely 的 handoff 机制重构为 A2A 协议，
包括集成官方 a2a-sdk、双传输（Unix+TCP）、Agent 发现、A2X-style 注册中心，
以及所有相关代码、文档、命名全量对齐。

详见 candidate C-20260612T140944Z-A。
