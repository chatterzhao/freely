---
local_id: I-20260507T143545Z-A
kind: linked
phase_state: completed
completed_at: "2026-05-19T23:20:00Z"
absorbed_at: '2026-05-16T14:27:11Z'
promoted_from: raw-20260507T143545Z45Z
source_candidate: docs/B1-docs/raw-20260507T143545Z45Z/candidates.md
canonical_issue_path: ''
platform_ids:
  github:
    issue_id: '248'
primary_platform: ''
last_synced_comment_at: {}
hash: ''
created_at: 2026-05-07 14:35:45+00:00
updated_at: '2026-05-17T12:25:33Z'
intake_id: ''
author: zhaoquan
channel: feat-execution
session_refs: []
pre_tests_path: docs/B2-docs/timestamp-seconds-upgrade/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/timestamp-seconds-upgrade/code-reviews
platform_state: closed
---

# I-20260507T143545Z-A: 时间戳格式带秒升级

- source_candidate: docs/B1-docs/raw-20260507T143545Z45Z/candidates.md
- pre_tests_path: docs/B2-docs/timestamp-seconds-upgrade/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/timestamp-seconds-upgrade/code-reviews

## 实现
- _normalize_key_variants: 支持 6位秒 + bare→new
- task-lifecycle-scan.py: 5 处 \d{4} → \d{4,6}
- pre-push.sh: 2 处 [0-9]{4} → [0-9]{4,6}
- issue-sync-batch.py: 1 处 \d{4} → \d{4,6}
