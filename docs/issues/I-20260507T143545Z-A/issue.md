---
local_id: I-20260507T143545Z-A
kind: linked
status: in_verification
phase_state: in_verification
promoted_from: raw-20260507T143545Z
source_candidate: docs/pre-brainstorms/20260507T143545Z--timestamp-seconds-upgrade/candidates.md
canonical_issue_path: ""
platform_ids: {}
primary_platform: ""
last_synced_comment_at: {}
hash: ""
created_at: 2026-05-07T14:35:45Z
updated_at: 2026-05-08T00:00:00Z
intake_id: ""
author: zhaoquan
channel: feat-execution
session_refs: []
pre_tests_path: docs/epics/timestamp-seconds-upgrade/verification/pre-tests.md
verification_artifact_dir: docs/epics/timestamp-seconds-upgrade/code-reviews
---

# I-20260507T143545Z-A: 时间戳格式带秒升级

- source_candidate: docs/pre-brainstorms/20260507T143545Z--timestamp-seconds-upgrade/candidates.md
- pre_tests_path: docs/epics/timestamp-seconds-upgrade/verification/pre-tests.md
- verification_artifact_dir: docs/epics/timestamp-seconds-upgrade/code-reviews

## 实现
- _normalize_key_variants: 支持 6位秒 + bare→new
- task-lifecycle-scan.py: 5 处 \d{4} → \d{4,6}
- pre-push.sh: 2 处 [0-9]{4} → [0-9]{4,6}
- issue-sync-batch.py: 1 处 \d{4} → \d{4,6}
