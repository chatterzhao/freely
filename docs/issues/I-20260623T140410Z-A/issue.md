---
local_id: I-20260623T140410Z-A
kind: linked
status: in_b2_ibm
phase_state: in_b2_ibm
promoted_from: raw-20260623T140410Z
source_candidate: docs/pre-brainstorms/20260623T140410Z--restore-tasks-edge-cases/candidates.md
canonical_issue_path: ""
platform_ids:
  github:
    issue_id: '3390'
    url: https://github.com/chatterzhao/freely/issues/3390
primary_platform: github
last_synced_comment_at: {}
hash: ""
created_at: 2026-06-23T14:04:10Z
updated_at: 2026-06-23T14:55:00Z
intake_id: ""
author: zhaoquan
channel: freely-fix-execution
session_refs:
  - tool: claude-code
  - analysis_issue: https://github.com/chatterzhao/freely/issues/3390
pre_tests_path: docs/epics/a2a-state-management/verification/pre-tests.md
verification_artifact_dir: docs/epics/a2a-state-management/code-reviews
---

# I-20260623T140410Z-A: A2A 状态管理全量修复

- source_candidate: `docs/pre-brainstorms/20260623T140410Z--restore-tasks-edge-cases/candidates.md`
- pre_tests_path: `docs/epics/a2a-state-management/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/a2a-state-management/code-reviews`

## 概述

全量审计 A2A task state 的所有修改点，修复 14 项问题：
A0（stop 不动状态）、A1-A3（重启状态修正边界）、B1-B4（环境恢复通知）、C1-C6（审计 bug 修复）。

涉及 5 个文件：`freely`、`a2a_server.py`、`a2a_task.py`、`freely_db_manager.py`、`wt-close`。
