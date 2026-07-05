# Progress: github-first-external-issue-source-governance

- issue_id: `I-20260407-1042-A`
- issue_path: `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/issues/github-first-external-issue-source-governance.md`
- title: `GitHub-first external issue source governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/external-issue-source-lifecycle-governance-20260420`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-feature-external-issue-source-lifecycle-governance`
- updated_at: `2026-04-20`
- closure_status: `issue_materialized`
- verification_status: `feature-local-pass`

## Summary

This owner now carries the bounded GitHub-first external-source governance package:

- the external-source family contract is frozen strongly enough for issue materialization
- source scan, canonical metadata, dedupe authority, source closeout, and publication reuse rules are now owner-scoped truth
- source-routing consumer docs have started adopting `external issue` as the durable source-family term
- runtime/API automation remains explicitly deferred to a later implementation owner

## Verification Evidence

- `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/code-reviews/20260420-github-first-external-issue-source-governance-decision.md`
- `docs/epics/workspace-routing-foundation/github-first-external-issue-source-governance/code-reviews/20260420-github-first-external-issue-source-governance-verification.md`
- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- `bash docs/system/workspace/scripts/tests/test-human-chat-routing`
- `./bin/governance-check`
- `git diff --check`

## Next Action

Local verification now passes. Next is guarded promote, then decide whether the follow-on should remain document-driven or begin runtime persistence/writeback implementation.
