---
local_id: raw-20260628T182243Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3608'
    url: https://github.com/chatterzhao/freely/issues/3608
    synced_at: ''
  gitee:
    issue_id: IJXE7P
    url: https://gitee.com/zhaoquan/freely/issues/IJXE7P
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-28T18:23:05Z'
updated_at: '2026-06-28T18:23:05Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Problem
B2 skill defines docs/epics/{epic}/{story}/raw-{raw-key}/ but code still reads/writes old paths (docs/issues/I-*, docs/epics/*/verification/).

## Scope
6 files: bin/freely-review, bin/pr-review-guarded, checkpoint-guard, governance-merge-gate, governance-promotion-gate, task-lifecycle-scan.py.

## Acceptance
All code uses docs/epics/*/*/raw-{raw-key}/ pattern. Existing files NOT moved.
