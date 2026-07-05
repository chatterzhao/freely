---
local_id: I-20260618T100000Z-A
kind: linked
status: in_dev
phase_state: completed
promoted_from: raw-20260618T100000Z00Z
source_candidate: docs/B1-docs/raw-20260618T100000Z00Z/candidates.md
canonical_issue_path: ""
platform_ids: {}
primary_platform: ""
last_synced_comment_at: {}
hash: ""
created_at: 2026-06-18T10:00:00Z
updated_at: 2026-06-18T10:00:00Z
intake_id: ""
author: freely-manager
channel: freely-fix-execution
session_refs: []
pre_tests_path: docs/B2-docs/wt-create-chat-inbox-id-bug/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/wt-create-chat-inbox-id-bug/code-reviews
---

# I-20260618T100000Z-A: wt-create chat-inbox ID normalization

- source_candidate: `docs/B1-docs/raw-20260618T100000Z00Z/candidates.md`
- pre_tests_path: `docs/B2-docs/wt-create-chat-inbox-id-bug/verification/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/wt-create-chat-inbox-id-bug/code-reviews`

## 实现

Fix already committed as `1f6a60340` in branch `fix/raw-20260618T100000Z00Z-wt-create-chat-inbox-id-bug`.

Changes: 4 call sites across 3 functions now pass `$ts_bare` (bare numeric) instead of `$ts` (ISO with TZ) to `chat-inbox.py` commands.
