#!/usr/bin/env python3
"""DEPRECATED: a2a_client.py has been merged into a2a_task.py.

All functionality (A2AClient, Task, TaskState, EXIT_KIND_TO_TASK_STATE) 
now lives in a2a_task.py. This file is kept as a compatibility shim.

Remove after 2026-07-14 (Phase 4c completion).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
print("[DEPRECATED] a2a_client.py → use a2a_task.py instead", file=sys.stderr)
# Re-export for backward compat
from a2a_task import A2AClient, EXIT_KIND_TO_TASK_STATE, TaskState, Task  # noqa
