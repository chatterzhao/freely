---
local_id: raw-20260628T182243Z43Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260628T005815Z-A
pre_tests_path: docs/B2-docs/human/discuss/raw-20260628T005815Z15Z/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/human/discuss/raw-20260628T005815Z15Z/code-reviews
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

- absorbed_into: I-20260628T005815Z-A
- pre_tests_path: docs/B2-docs/human/discuss/raw-20260628T005815Z15Z/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/human/discuss/raw-20260628T005815Z15Z/code-reviews

## Problem
B2 skill defines docs/B2-docs/{epic}/{story}/raw-{raw-key}/ but code still reads/writes old paths (docs/issues/I-*, docs/B2-docs/*/verification/).

## Scope
6 files: bin/freely-review, bin/pr-review-guarded, checkpoint-guard, governance-merge-gate, governance-promotion-gate, task-lifecycle-scan.py.

## Acceptance
All code uses docs/B2-docs/*/*/raw-{raw-key}/ pattern. Existing files NOT moved.
