- candidate_id: C-20260616T083810Z-A
- title: Governance enforcement — clarify fix-execution timing + document|cleanup|format scope + IBM skill guidance
- status: promoted
- milestone: M-20260616T083810Z-A
- promoted_issue_path: docs/issues/I-20260616T083810Z-A/issue.md
- decision_reason: SKIP_IBM_GATE abused; fix-execution ambiguous; error messages lack skill references; docs/cleanup/format unclear
- next_action: Materialize I-* issue in B2_IBM
---

# Candidate: Governance enforcement improvements

## Problem
1. FREELY_SKIP_IBM_GATE=1 used to merge code changes without IBM lifecycle
2. fix-execution "Fix first, govern later" misinterpreted as "govern never"
3. Gate error messages don't reference IBM skills
4. "docs/cleanup/format" ambiguous — should be "document|cleanup|format"

## Solution
1. Fix-execution SKILL.md: "Commit first, govern before PR" with explicit timeline
2. pre-commit hook: SKIP_IBM_GATE blocked → show exact skill commands
3. LAWS.md + hooks: "document|cleanup|format" clearer than "docs/cleanup/format"
