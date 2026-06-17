---
local_id: I-20260617T090413Z-A
kind: linked
status: in_dev
phase_state: completed
promoted_from: raw-20260617T090413Z
source_candidate: docs/pre-brainstorms/20260617T090413Z--fix-rest-routing/candidates.md
verification_artifact_dir: docs/epics/fix-rest-routing/code-reviews
---
# I-20260617T090413Z-A: REST routing for a2a-exit
## 修复
a2a_task.py create/update 走 _rest_request → A2A Server REST 端点（保留 worker_prompts_csv）
a2a_server.py POST handler 兼容 worker_prompts_csv key
