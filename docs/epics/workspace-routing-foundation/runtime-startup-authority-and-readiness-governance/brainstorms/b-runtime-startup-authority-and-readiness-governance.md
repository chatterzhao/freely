# Brainstorm: runtime-startup-authority-and-readiness-governance

## Boundary

- This issue exists because foreground duplicate-start, daemon false-ready, fake-supervisor acceptance, and stop-marker ghost retention all trace back to one missing runtime abstraction: authoritative launch identity plus launch readiness.
- The owner is bounded to startup truth publication and the consumers of that truth.
- The owner is not allowed to redesign the manager continuity contract; it can expose phases that a later handoff owner will build on.

## Candidate Design Direction

### 1. Publish launch truth explicitly

- Introduce a runtime-owned launch record for the current startup attempt.
- Minimum fields:
  - `launch_id`
  - `project_root`
  - `entrypoint_mode`
  - `supervisor_pid`
  - `started_at`
  - `startup_phase`

### 2. Delay unlock until startup authority exists

- The start lock should protect the boundary where later starters decide whether they are looking at:
  - no launch
  - one launch still publishing startup truth
  - one launch already authoritative
- Releasing the lock after `supervisor.pid` but before authoritative startup publication is the race to close.

### 3. Separate diagnostics from authority

- `ps` and cwd-based discovery can remain useful for:
  - stale process inspection
  - repair hints
  - emergency diagnostics
- They should no longer be sufficient for:
  - daemon ready
  - authoritative stop-marker retention
  - validating that the current project already has a live authoritative launch

### 4. Keep daemon parity inside this owner's verification

- The daemon symptom should remain in this owner's closeout gate unless later evidence proves a different root cause.
- That avoids splitting one startup-authority defect into artificial foreground and daemon owners.
