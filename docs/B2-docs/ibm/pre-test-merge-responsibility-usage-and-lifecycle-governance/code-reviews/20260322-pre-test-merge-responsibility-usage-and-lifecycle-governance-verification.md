# Verification: pre-test-merge-responsibility-usage-and-lifecycle-governance
- issue_id: `I-20260322-1801`

## Compatibility Note

- 历史 verification/path 保留 `pre-test-merge` 命名，当前 canonical 语义按 `test-pre-merge-*` 测试批次前缀族解释。

## Scope

- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
- `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/issues/pre-test-merge-responsibility-usage-and-lifecycle-governance.md`
- `docs/milestones.md`

## Findings

- historical `pre-test-merge` references now resolve to the `test-pre-merge-*` batch family, consistently described as a temporary validation surface rather than a long-lived truth surface.
- stale / retire / rebuild semantics are stated in the governing truth sources and the branch-management references.
- promotion defaults to replaying the source feature result instead of treating an old batch snapshot as the durable truth.
- the follow-on lifecycle capability remains separately queued in milestones, so this issue stays bounded to governance definition.

## Verification

- `./bin/governance-check`
- `./bin/wt-status-all`

## Result

- pass
