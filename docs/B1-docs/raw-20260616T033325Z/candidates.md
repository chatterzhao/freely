- candidate_id: C-20260616T033325Z-A
- title: Add governance-merge-gate check in pr-create-guarded before PR creation
- status: promoted
- milestone: M-20260616T033325Z-A
- promoted_issue_path: docs/issues/I-20260616T033325Z-A/issue.md
- decision_reason: Developers discover IBM governance gaps only at push time; gate errors are unclear; FREELY_SKIP_IBM_GATE on develop lacks path validation
- next_action: Materialize I-* issue in B2_IBM
---

# Candidate: Pre-merge governance gate check

## Problem
1. pr-create-guarded does not run governance-merge-gate → governance gaps discovered too late
2. Gate error messages don't reference IBM skills
3. pre-commit FREELY_SKIP_IBM_GATE exits without validating governance-only paths

## Solution
1. pr-create-guarded Step 2b: run governance-merge-gate before PR creation
2. Show clear IBM skill references in gate errors
3. pre-commit: validate governance-only paths before allowing develop commits
