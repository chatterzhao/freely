---
candidate_id: C-20260616T030213Z-A
title: Align governance-merge-gate scope with LAWS.md
status: promoted
promoted_issue_path: docs/issues/I-20260616T030213Z-A/issue.md
created: 2026-06-16T03:02:13Z
---

# Candidate: Restrict governance-only paths

## Problem
LAWS.md limits FREELY_SKIP_IBM_GATE=1 to docs/cleanup/format but
is_governance_only_path() in governance-merge-gate included hooks/,
scripts/runtime/, scripts/worktree/, scripts/tests/ — all executable code.

## Solution
Remove those paths. Keep agents/, skills/, quality/ as governance-only.

## Acceptance
- [ ] Runtime scripts blocked by FREELY_SKIP_IBM_GATE
- [ ] Doc paths still allowed
