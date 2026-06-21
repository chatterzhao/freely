---
local_id: raw-20260620T051432Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260620T051432Z-A
platform_ids:
  github:
    issue_id: '3145'
    url: https://github.com/chatterzhao/freely/issues/3145
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T05:14:49Z'
updated_at: '2026-06-21T18:25:29Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## Problem

manager_max_parallel_workers() returns "unbounded". Manager creates unlimited worker
tasks per cycle with no backpressure. With 76 scan items, 76 workers → 30+ daemon
instances → 200% CPU.

Manager patrol never checks active worker count before delegating. No mechanism to
signal 'too many workers' back to Manager.

## Design

### Two-tier concurrency in Runtime

- Soft cap (7): when reached, Runtime launches workers but injects a WARNING into
  the Manager's next prompt via A2A message/continuity artifact, saying:
  "Active workers: 7/10. Consider waiting for completions before delegating more."

- Hard cap (10): when reached, Runtime REFUSES to launch new workers. Marks submitted
  tasks as 'input-required' with reason: "worker_capacity_full: active=10/10. Wait
  for completions or increase max_parallel_workers config."

### Manager visibility

Both warnings and blocks are communicated to Manager via:
1. A2A task state (input-required with reason)
2. Runtime injects worker fleet status into Manager prompt (active count, limits)
3. Continuity artifact includes 'worker_capacity_warning' when near limit

### Configurable

max_parallel_workers defaults to 10 (hard) / 7 (warn). Overridable via config.toml:
  [runtime]
  max_parallel_workers = 10
  worker_warn_threshold = 7
