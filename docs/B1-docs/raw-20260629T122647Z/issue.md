---
local_id: raw-20260629T122647Z47Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3623'
    url: https://github.com/chatterzhao/freely/issues/3623
    synced_at: ''
  gitee:
    issue_id: IJXO03
    url: https://gitee.com/zhaoquan/freely/issues/IJXO03
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-29T12:27:08Z'
updated_at: '2026-06-29T12:27:08Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260629T122647Z-A

platform_state: closed---

## 背景

freely feedback 当前只有创建功能，需要新增 edit 子命令支持编辑已有 raw issue。

## 相关修复

- platform-adapter.py: update_issue() 改为接受 platform_ids dict
- cmd_feedback: 新增 edit 子命令
- body 编辑时保留原始 kind (fix/feature)

## 验收

- [x] freely feedback edit --raw-key ... --title ...  可用
- [x] freely feedback edit --raw-key ... --body ...   可用
- [x] --help 显示 edit 子命令
- [x] 向后兼容