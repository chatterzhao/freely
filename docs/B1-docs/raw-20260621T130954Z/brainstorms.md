# Brainstorm: a2a_task.py _unix_request Route Stripping Bug

## Root Cause

`A2AClient._unix_request()` (L155) strips specific path segments before `_rpc_map` lookup:

```python
_stripped = re.sub(r'/tasks/[^/]+', '/tasks', _base)
```

This regex replaces `/tasks/latest-manager`, `/tasks/pending-delivery`, `/tasks/launched-pids` with `/tasks`, making dedicated `_rpc_map` entries unreachable.

### Impact Chain

1. `latest_manager()` returns `{}` → `parse_a2a_task_json_reply` gets empty state
2. Returns `repair:["no_a2a_exit_called"]` → fallback validation path
3. `exit_contract_action` not `delegate_workers` → `manager_runtime_launch_workers_after_ai_cycle_if_needed` never called
4. Workers stay in `submitted` state forever → restart storm

## Resolution

Change 3 methods from `_request` (JSON-RPC) to `_rest_request` (raw HTTP), matching `list()`/`create()`/`update()`.
