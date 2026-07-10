---
local_id: raw-20260620T012922Z22Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260620T012922Z-A
platform_ids:
  github:
    issue_id: '3112'
    url: https://github.com/chatterzhao/freely/issues/3112
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T01:29:40Z'
updated_at: '2026-06-20T01:29:40Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## Problem

consume_delegate_workers uses a double-quoted heredoc python3 -c "..." inside
$() to filter worker tasks. This heredoc produces empty output in the daemon
context (set -euo pipefail), likely due to subtle quoting/escaping issues in
bash's heredoc processing within command substitution.

CLI testing with file-based Python filter succeeds (87 rows). Same pipeline with
heredoc returns empty in daemon context.

## Fix

Extract the Python filter code to a standalone script:
docs/system/workspace/scripts/runtime/consume_worker_tasks.py

Change the freely script from:
  _worker_tasks=$(python3 ... list ... | python3 -c "...heredoc..." ...)
to:
  _worker_tasks=$(python3 ... list ... | python3 "$CONSUME_FILTER_PY" ...)

This eliminates all heredoc quoting ambiguity.
