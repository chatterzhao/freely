# Implementation Decision
- decision: Route A2A extended operations through db_manager._db_rpc
- why: Freely-specific fields (worker_pid, delivery_status) not in A2A Task protobuf
- same pattern as: a2a_server.py SQLiteTaskStore._db_rpc
