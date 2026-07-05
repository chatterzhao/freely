# Brainstorm: ACP bridge cleanup on stop
## Context
daemon stop left acp-bridge.py orphaned, blocking restart.
## Fix
Read bridge pid from _acp_bridge_pid_file, terminate in stop_project_runtime before the restart-preserving case.
