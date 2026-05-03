---
local_id: I-20260503-0200-A
issue_title: "scan: switch to task-lifecycle-scan v2 with full lifecycle chain trace"
kind: linked
status: completed
phase_state: completed
promoted_from: raw-20260503-0200
platform_ids:
  github:
    issue_id: ""
  gitee:
    issue_id: ""
primary_platform: github
canonical_issue_path: "docs/epics/workspace-routing-foundation/scan-lifecycle-migration/issues/I-20260503-0200-A.md"
created_at: "2026-05-03T02:00:00Z"
updated_at: "2026-05-03T02:00:00Z"
session_refs: []
---

## Pre-Brainstorm Summary
废弃的 task-source-scan.py 仍在 runtime 中使用，输出147条噪声。
新版 task-lifecycle-scan.py 已实现但未接入。本次切换到 v2 并增加完整生命周期链条追踪。

## Scope
- TASK_SOURCE_SCAN_SCRIPT → task-lifecycle-scan.py
- Chain trace: 12 mandatory + 2 optional stations per key
- Chat inbox scan (Phase 0)
- Branch naming convention enforcement
- AF_UNIX socket hash-based short path
