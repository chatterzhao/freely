---
candidate_id: C-20260616T030213Z-A
title: Align governance-merge-gate scope with LAWS.md FREELY_SKIP_IBM_GATE constraint
status: promoted
created: 2026-06-16T03:02:13Z
---

# Candidate: Restrict governance-only paths

## Problem
LAWS.md limits FREELY_SKIP_IBM_GATE=1 to docs/cleanup/format.
But is_governance_only_path() in governance-merge-gate includes
hooks/, scripts/runtime/, scripts/worktree/, scripts/tests/ —
all executable code paths.

This allows runtime script changes to skip IBM lifecycle.

## Solution
Remove hooks/, scripts/runtime/, scripts/worktree/, scripts/tests/
from is_governance_only_path(). Keep agents/, skills/, quality/.

## Impact
- Runtime script changes now require full IBM lifecycle
- FREELY_SKIP_IBM_GATE=1 limited to actual governance artifacts
- Aligns gate behavior with LAWS.md §3

## Acceptance
- [ ] hooks/ changes blocked by FREELY_SKIP_IBM_GATE
- [ ] scripts/runtime/ changes blocked by FREELY_SKIP_IBM_GATE
- [ ] docs/issues/ changes still allowed
- [ ] pre-brainstorms/ changes still allowed
