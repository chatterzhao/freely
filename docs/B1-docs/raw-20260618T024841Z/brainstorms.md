# Brainstorm: raw issue completeness fixes

## Discovery
Post-merge review of #2956 found three gaps: candidate drift, audit incompleteness, data loss risk.

## Decision
Three small fixes, all low risk.

### 1. Candidate sync
Update C-20260618T015503Z-A acceptance_criteria to match actual implementation (PROJECT_ROOT derivation, git worktree list).

### 2. Audit methodology note
The path audit for #2956 used grep for docs/issues. Call-chain tracing would have caught _fill_platform_ids and worktree-common.sh wrapper. Document this as a lesson for future audits.

### 3. wt-close guard
Before deleting worktree, check if raw issue exists in develop's docs/B1-docs/raw-. If not, copy from worktree. Prevents data loss.
