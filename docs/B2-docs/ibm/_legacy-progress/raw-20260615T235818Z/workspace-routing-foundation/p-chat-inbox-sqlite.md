# Progress: chat-inbox-sqlite

- issue_id: `I-20260429-2040-A`
- issue_path: `docs/B2-docs/human/chat-inbox-sqlite/raw-20260429-2040issues/I-20260429-2040-A.md`
- title: `SQLite chat-inbox staging for protected-branch chat intake`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/chat-inbox-sqlite-20260429`
- updated_at: `2026-04-30`
- session_refs:
  - {tool: ccds, session_id: "20260429-chat-inbox-sqlite", role: "author"}
  - {tool: ccds, session_id: "20260430-acp-session-store", role: "author", absorbed: true}
- absorbed_candidates:
  - `docs/B1-docs/raw-20260430T000000Z/candidates.md#C-20260430-0000-A`

## 2026-04-30: ACP session-store absorbed

Hotfix absorbed into this issue: session-store.py replaces fragile cycle-log text parsing
with SQLite-backed session identity. See code-reviews/20260430-acp-session-store-verification.md
for implementation decision and review evidence.

## 2026-04-30 (2): Auto-init on start

Added ensure_freely_db() lazy-init called from start_project_runtime.
Existing projects no longer need manual re-init after upgrade.

## 2026-04-30 (3): Self-healing startup cleanup

Added _cleanup_stale_runtime_state() called from start_project_runtime.
Validates all PID files (supervisor, ai, acp-bridge, interruption-dispatcher),
removes stale lock/socket/marker files, and auto-cleans polluted session IDs.

## 2026-04-30 (4): Extend startup self-heal for acp_bridge

Extended existing startup_self_heal mechanism (not a new function):
- acp_bridge role added to PID validation loop
- Socket cleanup alongside stale bridge PID
- Marker file cleanup on every start
- Polluted session ID auto-heal

- self_heal_stale_lock: completed

- acp_bridge_lazy_restart: completed

- acp_resume_evidence_session_store: completed

- acp_no_inmemory_fallback: completed

- acp_permission_fix: completed

- alias_env_inheritance: completed

- auth_regex_fix: completed

- bridge_pid_fix: completed

- auto_force_clean_start_on_storm: completed

- stop_cleanup: completed
- no_attach_storm: completed

- diagnostic_logging: completed

- settle_cleanup: completed

- settle_cleanup_logging: completed

- cleanup_worker_launchable: completed

- worker_launch_on_delegate: completed


- worker_launch_docs: completed
