# Verification: pre-test-merge-responsibility-usage-and-lifecycle-governance

## Scope

- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
- `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/issues/pre-test-merge-responsibility-usage-and-lifecycle-governance.md`
- `docs/milestones.md`

## Findings

- `pre-test-merge` is now described consistently as a temporary validation batch, not a long-lived truth surface.
- stale / retire / rebuild semantics are stated in the governing truth sources and the branch-management references.
- promotion defaults to replaying the source feature result instead of treating an old batch snapshot as the durable truth.
- the follow-on lifecycle capability remains separately queued in milestones, so this issue stays bounded to governance definition.

## Verification

- `./bin/governance-check`
- `./bin/wt-status-all`

## Result

- pass
