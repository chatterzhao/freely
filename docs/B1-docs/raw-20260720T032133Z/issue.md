---
local_id: raw-20260720T032133Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '4040'
    url: https://github.com/chatterzhao/freely/issues/4040
    synced_at: ''
  gitee:
    issue_id: IK28CK
    url: https://gitee.com/zhaoquan/freely/issues/IK28CK
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-20T03:21:59Z'
updated_at: '2026-07-20T03:21:59Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## Problem
Manager prompt的agent_working注入（L17091）只说不可重复委派，但不说替代动作。Manager AI不知道：已委派后该用a2a_task.py prompt而不是a2a-exit --state submitted。

## Fix
修改_append_worker_fleet_status_if_needed中的prompt注入：
1. 表格增加task_id列（从a2a_tasks查最新working任务的task_id）
2. 将不可重复委派替换为明确的决策规则：
   - 已委派且working → prompt跟进
   - 已委派但failed → 标记旧任务然后重新委派
   - 未委派 → 正常submitted委派
