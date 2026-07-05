---
local_id: raw-20260616T083810Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260616T083810Z-A
platform_ids:
  github:
    issue_id: '2834'
    url: https://github.com/chatterzhao/freely/issues/2834
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-16T08:38:26Z'
updated_at: '2026-06-16T08:38:26Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Problem

Three systemic bypass patterns:

### 1. IBM governance skipped with FREELY_SKIP_IBM_GATE=1
Used to merge code changes without B1/B2 lifecycle. The flag exists for
governance-automated commits (wt-close, issue-sync) but is abused for
runtime fixes. pre-commit hook allows it, pre-push hook validates paths
but the flag itself has no gate.

### 2. Atomic commands used instead of wrapper commands
- git worktree remove --force → bypasses wt-close lifecycle
- git push origin develop → bypasses pr-merge-guarded multi-platform sync
- git commit on develop → bypasses worktree protection
- gh pr merge → bypasses governance gate

### 3. "Fix first, govern later" interpreted as "govern never"
freely-fix-execution/SKILL.md says "Fix first, govern later" but doesn't
specify WHEN "later" ends. Developers (and AI agents) interpret it as
optional rather than mandatory-before-pr-create.

## Fixes

### Fix 1: Clarify fix-execution skill timing
freely-fix-execution/SKILL.md: add explicit timeline
  "later = after code commit, BEFORE pr-create-guarded"
  "pr-create-guarded will block if IBM governance is incomplete"
  Add gate checklist: candidate, I-*, milestone, code-review

### Fix 2: Block atomic commands for managed operations
- git worktree remove → #2814 (git-worktree-guard auto-source)
- git push develop → already blocked by pre-push hook ✓
- git commit on develop → already blocked by pre-commit hook ✓ (except SKIP)
- gh pr merge → pr-create-guarded Step 2b now checks governance first ✓

### Fix 3: FREELY_SKIP_IBM_GATE scope enforcement
pre-commit hook: when SKIP_IBM_GATE=1, run governance-merge-gate --skip-ibm-gate 
to verify ONLY governance paths changed. Already implemented in #2807 but
only for pre-push. Add same check to pre-commit for develop commits.
