# Progress: project-level-agents-bootstrap-and-management-contract-governance

- issue_id: `I-20260405-1130-A`
- issue_path: `docs/B2-docs/config/packaging/raw-20260402-0403issues/project-level-agents-bootstrap-and-management-contract-governance.md`
- title: `Project-level AGENTS bootstrap and management contract governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260326-freely-product-architecture`
- branch: `feature/project-level-agents-contract-closeout-20260405-0325`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-0325-feature-project-level-agents-contract-closeout`
- updated_at: `2026-04-05`
- closure_status: `merged-and-verified`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Freely now carries a formal reusable capability contract for project-level `AGENTS.md` bootstrap and management semantics.
- The contract freezes four boundaries: create when missing, preserve when present, read the project root first, and treat self-hosting as the same rule.
- A focused regression now proves `freely init` preserves an existing project-owned `AGENTS.md`.
- The owner closes as `merged-and-verified` without widening into richer template injection, project-specific synthesis, or AGENTS migration flow.

## Completion Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-init-preserves-existing-agents-md`
- `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
- `bash docs/system/workspace/scripts/tests/test-freely-init-ai-default-precedence`
- `git diff --check`
- `./bin/governance-check`
- `docs/B2-docs/config/packaging/raw-20260402-0403code-reviews/20260405-project-level-agents-bootstrap-and-management-contract-governance-verification.md`
- `docs/B2-docs/config/packaging/raw-20260402-0403code-reviews/20260405-project-level-agents-bootstrap-and-management-contract-canonical-closeout-verification.md`

## Next Action

- No further action in this owner unless canonical `develop` regresses project-level `AGENTS.md` preservation or read-order truth.
