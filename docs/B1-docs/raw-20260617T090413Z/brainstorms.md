# Brainstorm: REST routing for a2a_task.py create/update

## Discovery
Fix #2908 (execute() 字段补全) 未能解决 worker_prompts_csv=none。
根因: JSON-RPC tasks/send SDK handler 不传递 Freely 特有字段到 context.metadata。
需让 create/update 走 REST 端点（已处理所有 Freely 字段）。

## Decision
Promote. 添加 _rest_request()，create/update 走 REST bypass JSON-RPC。
