---
local_id: raw-20260629T160852Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260629T160852Z-A
platform_ids:
  gitee:
    issue_id: IJXOMM
    url: https://gitee.com/zhaoquan/freely/issues/IJXOMM
    synced_at: ''
primary_platform: gitee
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T00:09:15+08:00'
updated_at: '2026-06-30T00:09:15+08:00'
intake_id: ''
author: platform
channel: gitee
session_refs: []
---

\n\n## 背景

当前 wt-close 只接受 branch 参数，但 wt-create 用的是 --raw-key。两者不对称。

Phase 6b 已经自动关联 test-pre-merge，但 help 文案没有明确说明，导致用户可能分开关闭 test 工位。

## 改动

### 1. 新增 raw-{key} 参数
支持 wt-close raw-20260629T132042Z 直接传 raw key，内部推导 fix/feature 分支名。

### 2. help 强调
明确写传 fix|feature 分支名，不要传 test-pre-merge，会自动通过 raw key 关联处理。

## 验收
- raw-{key} 参数可用
- help 明确说明传 fix|feature 分支
- help 说明 test-pre-merge 自动关联
