# Implementation Decision: REST routing for a2a-exit
- issue_id: I-20260617T090413Z-A
- reviewer: claude-sonnet-4-6
- decision: _rest_request() bypass JSON-RPC, create/update 直接 HTTP 到 REST 端点
- why_this: JSON-RPC tasks/send SDK handler 丢弃 worker_prompts_csv
- alternatives_considered: (A) 继续在 execute() 补字段 — 否决: SDK 不传递
- residual_risk: _rest_request 与 _unix_request 双路径维护
