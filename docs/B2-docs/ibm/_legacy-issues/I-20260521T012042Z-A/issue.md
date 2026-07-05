# I-20260521T012042Z-A: Manager keepalive stale-pid scanning

- title: Manager keepalive stale-pid scanning
- source: `raw-20260521T012042Z` (GitHub #1519, Runtime Crash Postmortem)
- milestone: M-20260521T012042Z-A
- source_candidate: `docs/B1-docs/raw-20260521T012042Z/candidates.md#C-20260521T012042Z-A`
- issue_id: I-20260521T012042Z-A
- phase_state: completed
- component: runtime

## Branch

- feature branch: `feature/raw-20260521T012042Z-stale-pid-keepalive`
- implementation commit: `36e1b480`
- merged to develop: pending (pr-merge-guarded)

## Deliverables

### B2_IBM
- PRD: `docs/B2-docs/stale-pid-keepalive/prd.md`
- Pre-tests: `docs/B2-docs/stale-pid-keepalive/pre-tests.md`
- Tasks: `docs/B2-docs/stale-pid-keepalive/tasks.md`
- Code review: `docs/B2-docs/stale-pid-keepalive/code-reviews/prd-review.md`
- Implementation decision: `docs/B2-docs/stale-pid-keepalive/code-reviews/implementation-decision-note.md`

### Dev-loop Implementation
- `docs/system/workspace/scripts/runtime/handoff.py` — Schema migration, CLI commands
- `docs/system/workspace/scripts/runtime/freely` — PID recording, scan function, keepalive integration
- `docs/system/workspace/scripts/tests/test-stale-pid-keepalive-*` — 11 test scripts
