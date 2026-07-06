---
local_id: I-20260624T004524Z-A
kind: linked
status: completed
phase_state: completed
promoted_from: raw-20260624T004510Z24Z
source_candidate: docs/B1-docs/raw-20260624T004510Z24Z/candidates.md#C-20260624T004524Z-A
canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260624T004524ZI-20260624T004524Z-A/issue.md
milestone: "M-20260624T004524Z-A"
title: "fix: defer _restore_tasks to background thread to prevent A2A startup timeout"
platform_ids:
  github:
    issue_id: '3398'
primary_platform: github
last_synced_comment_at: {}
hash: ""
created_at: 2026-06-24T00:45:41Z
updated_at: 2026-06-24T05:30:00Z
intake_id: ""
author: zhaoquan
channel: freely-fix-execution
session_refs: []
pre_tests_path: docs/B2-docs/a2a-restore-async/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/a2a-restore-async/code-reviews
---

# I-20260624T004524Z-A: A2A server _restore_tasks 异步化

- source_candidate: `docs/B1-docs/raw-20260624T004510Z24Z/candidates.md#C-20260624T004524Z-A`
- pre_tests_path: `docs/B2-docs/a2a-restore-async/verification/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/a2a-restore-async/code-reviews`
- milestone: M-20260624T004524Z-A

## 实现

1. `a2a_server.py`: `_restore_tasks()` 从 `__init__` 移除，改为 `start()` 中的 daemon 后台线程
2. `freely`: 修正 health check 超时消息 "may be TCP-only" → "check DB size, zombie PIDs, or disk I/O"
