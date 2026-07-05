---
local_id: raw-20260616T030213Z13Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260616T030213Z-A
platform_ids:
  github:
    issue_id: '2795'
    url: https://github.com/chatterzhao/freely/issues/2795
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-16T03:02:30Z'
updated_at: '2026-06-16T03:02:30Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Problem

LAWS.md says FREELY_SKIP_IBM_GATE=1 is only for "docs/cleanup/format".
But governance-merge-gate --skip-ibm-gate classifies ALL workspace scripts
(docs/system/workspace/scripts/runtime/, worktree/, hooks/) as governance-only,
allowing runtime code changes to bypass IBM lifecycle.

This inconsistency means:
1. Runtime fixes to freely scripts, acp-bridge, tool-launchers etc. can merge
   without B1_IBM → candidate → B2_IBM → I-* chain
2. Developers (and AI agents) can use FREELY_SKIP_IBM_GATE=1 to merge code
   changes by claiming they're "governance infrastructure"
3. The fix-execution "Fix first, govern later" path has no enforcement — fixes
   merge without governance and governance is never completed later

## Options

### Option A: Align gate to LAWS.md (strict)
- Restrict governance-only paths to: AGENTS.md, CONSTITUTION.md, LAWS.md,
  PROJECT_INTENT.md, milestones.md, docs/B1-docs/raw-, docs/B2-docs/,
  docs/progress/, docs/issues/
- All workspace scripts REQUIRE IBM lifecycle
- FREELY_SKIP_IBM_GATE=1 only works for pure doc changes

### Option B: Align LAWS.md to gate (permissive)  
- Expand "docs/cleanup/format" to include workspace infrastructure scripts
- FREELY_SKIP_IBM_GATE=1 works for docs/system/workspace/scripts/* changes
- But runtime code changes should still go through IBM lifecycle

### Option C: Split workspace scripts into "infrastructure" vs "runtime"
- docs/system/workspace/scripts/runtime/freely → RUNTIME (needs IBM)
- docs/system/workspace/scripts/worktree/wt-close → RUNTIME (needs IBM)
- docs/system/workspace/hooks/pre-commit.sh → RUNTIME (needs IBM)
- docs/system/workspace/scripts/quality/governance-merge-gate → INFRA (skip OK)
- docs/system/workspace/scripts/runtime/acp-bridge.py → INFRA (skip OK)

## Recommendation
Option A. Align gate to LAWS.md. Runtime code changes should NOT skip IBM.
Fix-execution already has the governance path (skill:freely-fix-execution
explicitly says "Fix first, govern later" — meaning governance MUST come later,
not that it's optional).
