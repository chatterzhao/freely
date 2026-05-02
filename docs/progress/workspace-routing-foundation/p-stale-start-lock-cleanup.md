# Progress: stale-start-lock-cleanup

- issue_id: `I-20260502-1028-A`
- issue_path: `docs/epics/workspace-routing-foundation/stale-start-lock-cleanup/issues/I-20260502-1028-A.md`
- title: `fix: clean stale start lock before daemon stop`
- phase_state: `in_dev`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `hotfix/stop-clean-stale-lock-20260502`
- updated_at: `2026-05-02`
- session_refs:
  - {tool: ccds, session_id: "20260502-stale-lock", jsonl_path: "unavailable://manual", role: "author"}

## Summary

3-line fix in `stop_project_runtime()`: clean stale start lock before acquiring lock for daemon stop. Daemon full lifecycle verified on 2026-05-02.

## Verification

- [x] daemon start → daemon status shows running
- [x] scan correctly identifies tasks across 5 surfaces
- [x] worker delegation via exit_contract works
- [x] lifecycle trace checkpoints L001→L092 complete
- [x] continuity file shows route decision for next task
- [x] packaged version runs correctly (712 files)
