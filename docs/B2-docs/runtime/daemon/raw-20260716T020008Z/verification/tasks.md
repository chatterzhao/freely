# Tasks: worker session writeback
- issue_id: I-20260716T020008Z-A
- [x] Add target_project/agent_id/slot params to capture_worker_session_id_and_store
- [x] Call acp_session_register after session_id capture
- [x] Pass params from launch_worker call sites
- [x] bash -n PASS
