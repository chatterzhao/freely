---
local_id: raw-20260716T000513Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260716T000513Z-A
platform_ids:
  github:
    issue_id: '3919'
    url: https://github.com/chatterzhao/freely/issues/3919
    synced_at: ''
  gitee:
    issue_id: IK1BNE
    url: https://gitee.com/zhaoquan/freely/issues/IK1BNE
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-16T00:05:36Z'
updated_at: '2026-07-16T00:05:36Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因

### 问题 1: agent_assign 写入时机不对
agent_assign 只在 sync_project_tooling_from_source (line 6042) 调用。Manager 通过 freely wt-create CLI 创建工位后不会触发这个函数。agent_working 表永远没有 Worker 条目。

应在 Manager 委派 Worker 时（a2a-exit submitted → daemon _handle_needs_worker）调用 agent_assign。

### 问题 2: Worker 缺少 verification contract  
Manager 创建工位后委派 Worker，但未写入 worker-verification-contract.env（owner_issue/pre_tests_path 等字段）。Worker daemon 启动时检查该文件，缺失则无法启动。

## 修复方案
1. 在 daemon 委派 worker 路径（_handle_needs_worker / worker launch）中调用 agent_assign 写入 agent_working
2. Manager prompt 增加委派时的 contract 写入指导
