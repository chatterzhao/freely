# Implementation Decision: manager-semantic-loop-active-worker-suppression-governance

- issue_id: `I-20260405-1505-A`
- issue_path: `docs/epics/workspace-routing-foundation/manager-semantic-loop-active-worker-suppression-governance/issues/manager-semantic-loop-active-worker-suppression-governance.md`
- date: `2026-04-05`

## Decision

Use a bounded suppression helper for semantic-loop monitoring that prefers currently discoverable active worker lanes but falls back to the persisted manager launch-state `ACTIVE_RUNNING_WORKER_COUNT` when it is higher.

## Why This

- The failing regression is about false positives, so a conservative suppression-only fallback is acceptable.
- The launch-state file is already runtime-owned truth and is refreshed for status surfaces; if that file still says an active worker exists, semantic-loop monitoring should avoid flagging a manager loop until the runtime truth is reconciled.
- This keeps the change local to semantic-loop suppression instead of rewriting broader activity-state or fleet counting semantics.

## Rejected Alternatives

- Reopen `I-20260322-0445`: rejected because that owner is completed and its canonical generated/consumed contract remains true.
- Treat launch-state count as global authoritative active-worker status everywhere: rejected because that would widen this lane beyond semantic-loop suppression.
