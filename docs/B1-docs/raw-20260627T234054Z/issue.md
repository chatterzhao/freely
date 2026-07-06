---
local_id: raw-20260627T234054Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260627T234054Z-A
platform_ids:
  github:
    issue_id: '3600'
    url: https://github.com/chatterzhao/freely/issues/3600
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-27T23:41:14Z'
updated_at: '2026-06-27T23:41:14Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 根因

当前 wt-create --source platform 直接 pull_raw_issue，不检查平台的 assignee 状态。这导致：
- 多人/多设备可能同时对同一个 issue 开工位
- 平台上的 assignee 信息未被利用
- 传统 PM→assign 开发者的流程不受支持

## 设计

### wt-create 新增 assignee 检查

wt-create --raw-key xxx --source platform 流程调整为：

1. platform-adapter 查询平台 assignee（github + gitee 双平台）
2. 若已被他人 assign → 拒绝，提示 issue 已被 @xxx 认领
3. 若无人 assign → platform-adapter 将 self 设为 assignee
   - 名字从 git config user.name 读取
   - adapter 封装同时操作 github + gitee
4. 然后 pull_raw_issue（平台 issue → 本地 issue.md）
5. 创建工位

### platform-adapter 新增方法

- get_assignees(platform, issue_number) → list of assignee logins
- set_assignee(platform, issue_number, login) → ok/error
- 对 github 用 gh api，对 gitee 用对应 API

### 不纳入

- chat 重构（评论独立、讨论 session 化）— 另外独立设计
- 评论处理状态（adopted/discarded 子评论）— 另外独立设计
- wt-close 评论检查 — 另外独立设计
