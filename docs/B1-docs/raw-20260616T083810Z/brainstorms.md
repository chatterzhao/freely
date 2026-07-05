# Brainstorm: Governance enforcement

## Discovery

Three systemic bypass patterns were identified in the Freely governance system:

### 1. FREELY_SKIP_IBM_GATE=1 abused
The flag exists for governance-automated commits (wt-close, issue-sync) but is used for runtime fixes. pre-commit allows it, pre-push validates paths but the flag itself has no gate.

### 2. Atomic commands bypass wrapper scripts
- `git worktree remove --force` bypasses wt-close lifecycle
- `git push origin develop` bypasses pr-merge-guarded multi-platform sync
- `git commit on develop` bypasses worktree protection
- `gh pr merge` bypasses governance gate

### 3. "Fix first, govern later" interpreted as "govern never"
The fix-execution skill doesn't specify WHEN "later" ends, so agents interpret it as optional.

### Involved files

1. `docs/system/workspace/skills/freely-fix-execution/SKILL.md`
2. `.githooks/pre-commit`
3. `.githooks/pre-push`
4. `bin/pr-create-guarded`
5. `docs/system/workspace/hooks/governance-merge-gate`
6. Related GitHub issues (#2807, #2814)

## Research

### Fix 1: Clarify fix-execution skill timing
- Add explicit timeline: "later = after code commit, BEFORE pr-create-guarded"
- Add gate checklist: candidate, I-*, milestone, code-review
- `pr-create-guarded` blocks if IBM governance is incomplete

### Fix 2: Block atomic commands for managed operations
- `git worktree remove` → use wrapper (tracked in #2814)
- `git push develop` → already blocked by pre-push hook ✓
- `git commit on develop` → already blocked by pre-commit hook ✓
- `gh pr merge` → pr-create-guarded Step 2b checks governance ✓

### Fix 3: FREELY_SKIP_IBM_GATE scope enforcement
- pre-commit hook: when SKIP_IBM_GATE=1, run governance-merge-gate --skip-ibm-gate
- Verify ONLY governance paths are changed
- Already in pre-push (#2807), add same to pre-commit

## Decision

**All three fixes — comprehensive governance enforcement.**

### Implementation
1. Update `freely-fix-execution/SKILL.md` with explicit "Commit first, govern before PR" timeline
2. Add scope enforcement for FREELY_SKIP_IBM_GATE in pre-commit hook
3. Clarify LAWS.md + hooks: "document|cleanup|format" wording
4. Verify all gate paths are covered

### Acceptance
- [x] fix-execution SKILL.md has explicit governance timeline
- [x] pre-commit hook enforces SKIP_IBM_GATE scope
- [x] Atomic commands blocked or deprecated for managed ops
- [x] "document|cleanup|format" clarified in LAWS.md and hooks
