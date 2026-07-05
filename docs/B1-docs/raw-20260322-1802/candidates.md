# Candidates - 20260322-1802--pre-test-merge-semantic-audit-and-recovery

## Compatibility Note

- 历史 candidate/path 保留 `pre-test-merge` 命名，当前 canonical 语义按 `test-pre-merge-*` 测试批次前缀族解释。

## Audit results

- `already absorbed by develop`
  - `61121e1` runtime behavior for latest-manager-continuity driven worker launch and local reentry
  - current manager routing docs and tests that validate the launch/reentry path

- `still missing and worth recovering`
  - `pre-test-merge` lifecycle governance as a first-class Freely capability
  - stale batch detection, explicit batch retirement, and batch re-creation when the validation batch is no longer authoritative

- `obsolete / superseded`
  - `61121e1` generated-vs-consumed launch-state observability fields
  - `9f4f8a6` as a standalone discovery artifact, because later continuity-handoff workstreaming in `develop` already carries the same substantive direction

- `needs-more-verification`
  - whether richer launch-state observability is still needed
  - whether batch freshness belongs in runtime status, branch-management skill logic, or only governance docs

## Candidate issue

### C-20260322-1802-A

- title: `pre-test-merge governance and lifecycle capability`
- status: `absorbed`
- adoption_type: `supporting_evidence`
- decision_reason: the audit confirmed that the remaining gap is governance/lifecycle, not a direct runtime rollback. That problem is now owned by the formal governance issue instead of this audit worktree.
- promoted_issue_path: `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/issues/pre-test-merge-responsibility-usage-and-lifecycle-governance.md`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- source_brainstorm: `docs/pre-brainstorms/20260322-1802--pre-test-merge-semantic-audit-and-recovery/brainstorms.md`
- session_refs:
  - tool: `codex`
  - session_id: `current-thread`
  - jsonl_path: `unavailable://codex-thread-only`
  - role: `analyst`
- next_action: no further implementation work in this audit branch; use this artifact as supporting evidence while the governance issue proceeds through IBM/dev/verification
- revisit_trigger: reopen only if a future semantic diff exposes a non-governance recovery gap that the governance issue does not cover
