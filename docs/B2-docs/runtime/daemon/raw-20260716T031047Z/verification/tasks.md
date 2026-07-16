# Tasks: agent_working raw_key fix
- issue_id: I-20260716T031047Z-A
- [x] 1. Add _raw_key extraction in capture_worker_session_id_and_store
- [x] 2. Fix acp_session_register call to use _raw_key
- [x] 3. Fix agent_assign pre-launch to use _worker_raw_key
- [x] 4. bash -n syntax check
- [x] 5. Verify grep confirms raw_key extraction present
