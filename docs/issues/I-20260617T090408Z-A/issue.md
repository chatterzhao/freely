---
local_id: I-20260617T090408Z-A
kind: linked
status: in_dev
phase_state: completed
promoted_from: raw-20260617T090408Z
source_candidate: docs/pre-brainstorms/20260617T090408Z--fix-worker-prompts-csv/candidates.md
pre_tests_path: docs/epics/fix-worker-prompts-csv/pre-tests.md
verification_artifact_dir: docs/epics/fix-worker-prompts-csv/code-reviews
---
# I-20260617T090408Z-A: Fix worker_prompts_csv dead loop

## 根因
a2a_server.py FreelyAgentExecutor.execute() 在 tasks/send 时不持久化 worker_prompts_csv 等 Freely 特有字段。
Manager 的 a2a-exit --workers=... 调用创建 A2A task 后，worker_prompts_csv 被丢弃。
freely runtime _db_exit_contract_field 返回空，导致 validate 看到 none → Worker 不启动 → 死循环。

## 修复
execute() 中补齐: worker_prompts_csv, completion_summary, next_action, evidence_paths, session_id
