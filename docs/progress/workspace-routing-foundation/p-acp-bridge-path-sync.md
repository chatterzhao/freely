# ACP Bridge Path Sync

- issue: `I-20260503-0115-A`
- issue_path: `docs/epics/workspace-routing-foundation/acp-bridge-path-sync/issues/I-20260503-0115-A.md`
- milestone: `M-20260306-workspace-routing-foundation`
- phase_state: `in_dev`
- runtime_state: `verified_on_develop`
- updated_at: `2026-05-03T01:15:00Z`
- next_action: `merge_to_develop_via_merge_guarded`

## Verification

- Daemon start → ACP bridge initializes → socket at correct hash-based path
- AI launches via ACP → session/resume → session/prompt → cycle runs successfully
- AI discovers and executes tasks correctly (temp worktree cleanup)
- All four files now use consistent `.freely/run/acp-bridge-{hash}.*` paths
