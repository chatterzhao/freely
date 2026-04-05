# Progress: project-level-agents-bootstrap-and-management-contract-governance

- issue_id: `I-20260405-1130-A`
- issue_path: `docs/epics/freely-product-architecture/project-level-agents-bootstrap-and-management-contract-governance/issues/project-level-agents-bootstrap-and-management-contract-governance.md`
- title: `Project-level AGENTS bootstrap and management contract governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260326-freely-product-architecture`
- branch: `feature/project-level-agents-management-contract-20260405-0305`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-0305-feature-project-level-agents-management-contract`
- updated_at: `2026-04-05`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Freely now carries a formal reusable capability contract for project-level `AGENTS.md` bootstrap and management semantics.
- The contract freezes four boundaries: create when missing, preserve when present, read the project root first, and treat self-hosting as the same rule.
- A focused regression now proves `freely init` preserves an existing project-owned `AGENTS.md`.
- The owner remains narrow and does not widen into richer template injection or AGENTS migration flow.

## Verification Snapshot

- Passed in this worktree:
  - `bash docs/system/workspace/scripts/tests/test-freely-init-preserves-existing-agents-md`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-ai-default-precedence`
  - `./bin/governance-check`
