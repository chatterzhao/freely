# PRD: session ID capture ses_ 格式
- issue_id: I-20260720T045011Z-A
## Goal
capture_worker_session_id_and_store 接受 opencode ses_ 格式 session ID
## Implementation
L13093: 硬编码 UUID regex → is_valid_session_id "$_session_id"
