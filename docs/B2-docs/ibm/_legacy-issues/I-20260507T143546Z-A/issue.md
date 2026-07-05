---
local_id: I-20260507T143546Z-A
kind: linked
phase_state: completed
completed_at: "2026-05-19T23:20:00Z"
absorbed_at: '2026-05-16T14:27:11Z'
promoted_from: raw-20260507T143546Z
source_candidate: docs/pre-brainstorms/20260507T143546Z--platform-pull-standardize/candidates.md
canonical_issue_path: ''
platform_ids:
  github:
    issue_id: '249'
primary_platform: ''
created_at: 2026-05-07 14:35:46+00:00
session_refs: []
pre_tests_path: docs/epics/platform-pull-standardize/verification/pre-tests.md
verification_artifact_dir: docs/epics/platform-pull-standardize/code-reviews
platform_state: closed
updated_at: '2026-05-17T12:25:37Z'
---

# I-20260507T143546Z-A: platform pull 标题标准化

- source_candidate: docs/pre-brainstorms/20260507T143546Z--platform-pull-standardize/candidates.md
- pre_tests_path: docs/epics/platform-pull-standardize/verification/pre-tests.md
- verification_artifact_dir: docs/epics/platform-pull-standardize/code-reviews

## 实现
- _created_at_to_key: 平台时间戳 → 标准 key
- _update_issue_title: 通过平台 API 更新标题
- pull_raw_issue: 比较并自动修正
