---
local_id: raw-20260521T121158Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '1859'
    url: https://github.com/chatterzhao/freely/issues/1859
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-21T12:12:10Z'
updated_at: '2026-05-21T12:12:10Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题
当前版本号格式为 YYYYMMDD-nightly（如 20260521-nightly），不含时分，同一天多次打包会覆盖。

## 修复
改为 YYYYMMDDTHHMMZ-nightly（如 20260521T1207Z-nightly）。

涉及文件：
- bin/freely-package: 文档注释 + validate_version 正则
- bin/test-pre-merge-selfhost: VERSION 生成命令
