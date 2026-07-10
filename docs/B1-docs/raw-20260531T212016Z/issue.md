---
local_id: raw-20260531T212016Z16Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2375'
    url: https://github.com/chatterzhao/freely/issues/2375
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-31T21:20:31Z'
updated_at: '2026-06-17T00:23:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed---

## 修复

1. select_launch_kind ACP 路径不再二次查询 session-store，直接信任 _tool_switch_launch_kind 返回 resume 时 tool_switch_events 记录的 session ID。避免 session-store 因 is_valid_uuid/工具不匹配/failed 状态覆盖正确结果。

2. monitor-ai-acp.sh stall watchdog 移除 debug log mtime 误判——AI 思考时无 debug 输出是正常行为。改为仅检查 bridge 进程是否存活。bridge 自身有 900s idle timeout 处理真正无响应场景。

## 根因
- session-store 的 is_valid_uuid 拒绝 opencode ses_ 格式
- session.get-active 不按工具过滤
- stall watchdog 在 AI 加载治理文档时误杀会话

## 验证
- fresh→prompt 正常转换
- L240=0
- worker 产出恢复
