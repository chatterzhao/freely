# PR Review: raw-20260716T031047Z
- issue_id: I-20260716T031047Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20260716T031047Z/issues/I-20260716T031047Z-A.md
- branch: fix/raw-20260716T031047Z-agent-working-raw-key
- reviewer: Claude
- verdict: pass
## Overall Verdict: pass
Adds raw_key extraction from target_project path in capture_worker_session_id_and_store and agent_assign pre-launch.
Three targeted changes: (1) extract _raw_key from path, (2) use in acp_session_register, (3) use in agent_assign.
Safe fallback: ${_raw_key:-agent_id} preserves old behavior if path doesn't contain raw_key.
