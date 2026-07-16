---
local_id: raw-20260716T121311Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260716T040152Z-A
platform_ids:
  github:
    issue_id: '3945'
    url: https://github.com/chatterzhao/freely/issues/3945
    synced_at: ''
  gitee:
    issue_id: IK1K6Q
    url: https://gitee.com/zhaoquan/freely/issues/IK1K6Q
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-16T12:13:34Z'
updated_at: '2026-07-16T12:13:34Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

daemon 启动全部失败，根因就是一个 dirty file。但因为这个原因不明显，导致多轮错误修改。

## 修改

1. 回退 PR #3939 #3941 #3943 中不需要的 writeback/stall detection 修改
2. 保留 server stdout closed fatal 移除 (这个是对的)
3. 简化 start_project_runtime 的 dirty check 报错——当前输出大量重复废话
   淹没真正原因。改为: 列出 dirty 文件 + 一条 git checkout 命令即可
