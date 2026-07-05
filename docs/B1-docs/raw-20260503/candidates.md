# C-20260503T000000Z-B: fix-execution skill

- candidate_id: `C-20260503T000000Z-B`
- title: `fix-execution skill for rapid bug fix workflow`
- status: `promoted`
- priority: `P1`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_to: `I-20260503T000000Z-B`
- promoted_issue_path: `docs/B2-docs/ibm/fix-execution-skill/issues/I-20260503T000000Z-B.md`
- source_intake: `raw-20260503-fix-skill`

## Problem

Bug fixes currently have no standard workflow. Fixes are done ad-hoc on develop,
governance is written before validation, and commits pile up at the end.

## Solution

New `skill:fix-execution` codifies: pre-merge worktree isolation for testing,
early hotfix worktree creation with incremental commits, governance after fix validation.
