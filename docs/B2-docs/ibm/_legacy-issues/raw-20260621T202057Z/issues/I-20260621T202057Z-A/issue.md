---
local_id: I-20260621T202057Z-A
kind: I
phase_state: completed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260621T202057Z/code-reviews
source_candidate: docs/milestones.md#C-20260621T202057Z-A
platform_ids:
  github:
    issue_id: ''
    url: ''
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T14:30:00Z'
updated_at: '2026-06-22T14:30:00Z'
intake_id: ''
author: claude
channel: local
session_refs: []
---

# I-20260621T202057Z-A: Batch implementation of 11 remaining issues

## Scope

Batch implementation covering:
- #3290: Runtime raw issue validation before worker launch
- #3302: Block new comments on closed platform issues
- #3340: platform-adapter PR operations (create/merge/close)
- #3336: freely init platform configuration gate
- #3312: docs: [命令]/[skill] markers in AGENTS.md flow
- #3311: three-loop docs: Manager persistent session, ACP fault detection, dispatch modes
- #3310: three-loop docs: closeout Phase 4.5, pr-merge no longer deletes remote

## PRD

All changes are infrastructure/quality improvements. No architectural changes.

## Tasks

1. Add raw issue validation in worker_prompt_launchable_for_manager_project ✅
2. Add closed-issue check in platform-adapter add_comment() ✅
3. Add PR operations to platform-adapter ✅
4. Add platform config gate to freely init ✅
5. Add [命令]/[skill] markers to AGENTS.md ✅
6. Update three-loop capability lifecycle doc ✅

## Pre-tests

- worker launch blocks when raw issue is closed/absent ✅
- add_comment blocks on closed issues ✅
- platform-adapter create-pr/merge-pr/close-pr CLI works ✅
- freely init blocks without FREELY_REPO_PLATFORMS ✅
- AGENTS.md flow has proper [命令]/[skill] markers ✅
