---
local_id: raw-20260715T055018Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260715T055018Z-A
platform_ids:
  github:
    issue_id: '3902'
    url: https://github.com/chatterzhao/freely/issues/3902
    synced_at: ''
  gitee:
    issue_id: IK15W3
    url: https://gitee.com/zhaoquan/freely/issues/IK15W3
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-15T05:50:41Z'
updated_at: '2026-07-15T05:50:41Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因

### 问题 1: daemon start 不刷新 scan
手工启动 daemon 后，task_source_scan_regeneration_reason_for_project 无"daemon just started"触发条件，且 15 分钟内无 HEAD 变化/worker 完成/intake 新增时复用旧缓存。daemon 停止期间 scan 已过期（缓存 0 items，实际 50 items），导致 prompt 无 scan 数据注入，AI 无的放矢。

### 问题 2: tool_unproductive 不触发 auto→listen
stop_ai→listen 只在 kind=="stop_ai" 时触发（line 16059）。tool_unproductive 走 default 分支 continue，永远不会切 listen。由于 mode 还是 auto，watchdog 重启 supervisor 后又启动 AI，形成重启循环。

listen 模式本身行为正确——每 300s 全量刷新 scan，有 ready 任务自动切 auto。

## 修复方案

1. start_project_runtime 中清理旧 scan 缓存，迫使首次 build_prompt 重新 scan
2. 将 auto→listen 切换逻辑从 stop_ai 专属提升为通用——auto 模式下，AI 以任何原因退出，scan 无 ready 即切 listen
