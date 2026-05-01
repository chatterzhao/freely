# Progress: bash32-daemon-compat-fix

- issue_id: `I-20260429-1745-A`
- issue_path: `docs/epics/workspace-routing-foundation/bash32-daemon-compat-fix/issues/I-20260429-1745-A.md`
- title: `Fix daemon self-detection suicide + bash 3.2 pipefail crash`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/fix-daemon-bash32-crash-20260429`
- updated_at: `2026-04-29`
- session_refs:
  - {tool: ccds, session_id: "20260429-bash32-fix", jsonl_path: "unavailable://manual", role: "author"}

## Summary

- Two defensive fixes for macOS bash 3.2 compatibility in the freely runtime supervisor.
- Changes are minimal: add `$$` exclusion in supervisor detection, replace bare `ls` glob with nullglob-guarded array.
- No core logic or architecture changes.
