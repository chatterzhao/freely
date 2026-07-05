---
local_id: I-20260617T160003Z-A
kind: linked
status: in_dev
phase_state: completed
promoted_from: raw-20260617T160003Z
source_candidate: docs/B1-docs/raw-20260617T160003Z/candidates.md
canonical_issue_path: ""
platform_ids: {}
primary_platform: ""
last_synced_comment_at: {}
hash: ""
created_at: 2026-06-17T16:00:03Z
updated_at: 2026-06-17T16:00:03Z
intake_id: ""
author: zhaoquan
channel: freely-fix-execution
session_refs: []
pre_tests_path: docs/B2-docs/wt-close-force-overwrite-fix/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/wt-close-force-overwrite-fix/code-reviews
---

# I-20260617T160003Z-A: Fix wt-close --force overwriting pr-merge-guarded frontmatter

- source_candidate: docs/B1-docs/raw-20260617T160003Z/candidates.md
- pre_tests_path: docs/B2-docs/wt-close-force-overwrite-fix/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/wt-close-force-overwrite-fix/code-reviews

## 实现

wt-close Phase 3: 在写入 force_closed_at/reason 之前检查 phase_state。若已是 "absorbed"，说明 pr-merge-guarded 已处理，跳过写入。
