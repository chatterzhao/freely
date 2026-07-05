# Tasks: per-agent tool/slot
- issue_id: I-20260705T024320Z-A
- [x] 1. _acp_session_close 加 base_tool，调用点传参
- [x] 2. _ensure_acp_bridge_running 加 slot 参数，env/.tool 用 slot
- [x] 3. daemon start bridge loop 传 slot
- [x] 4. worker launch socket 传 base_tool，--agent 用查询结果
- [x] 5. _stop_acp_bridge caller 传 base_tool
- [x] 6. stop_project_runtime 扫描全部 base_tool
- [x] 7. sse-watchdog.sh bridge socket 传 base_tool
- [x] 8. bash -n + grep 验证
