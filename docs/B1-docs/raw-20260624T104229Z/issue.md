---
local_id: raw-20260624T104229Z29Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T104229Z-A
platform_ids:
  github:
    issue_id: '3426'
    url: https://github.com/chatterzhao/freely/issues/3426
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T10:42:48Z'
updated_at: '2026-06-24T10:42:48Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题
wt-create 成功后的提示信息硬编码了步骤列表（如 "1. 在 test-pre-merge-* 改源码"），且文本陈旧（仍写 stop/start daemon、cp 修改）。

## 修复
wt-create 接收 --skill 参数（如 freely-fix-execution），成功信息应从参数中提取 skill 名称，提示：
"请阅读 skill:freely-fix-execution，按其规范流程执行。"

不应在 wt-create 脚本里重复/硬编码 skill 内的步骤——skill 是流程的权威来源。
