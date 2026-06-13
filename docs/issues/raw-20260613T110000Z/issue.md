---
local_id: raw-20260613T110000Z
kind: raw
phase_state: absorbed
platform_ids: {}
primary_platform: local
canonical_issue_path: ''
created_at: '2026-06-13T11:00:00Z'
platform_state: local_only
updated_at: '2026-06-13T11:00:00Z'
---

a2a_task.py _client 变量/函数命名冲突导致 process_ai_reply 永远失败。
Manager AI 输出正确的 JSON state block 后 parse_a2a_task_json_reply 始终返回 exit_kind=error。

根因: 模块级变量 _client = None 被同名函数 def _client() 覆盖，
global _client 永远指向函数自身，process_ai_reply 调用 c.create() 时报 AttributeError。
