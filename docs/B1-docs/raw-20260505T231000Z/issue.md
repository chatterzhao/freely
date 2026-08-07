---
local_id: raw-20260505T231000Z00Z
issue_title: 'fix: secret detection false positive on file paths with sk- prefix'
kind: raw
- phase_state: dropped
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17 04:47:25+00:00
platform_ids:
  github:
    issue_id: '228'
    url: https://github.com/chatterzhao/freely/issues/228
primary_platform: github
created_at: '2026-05-05T23:10:22Z'
intake_id: 20260505T2310Z-secret-detection-false-positive
author: human
channel: github
session_refs: []
platform_state: closed
---

## Problem

Pre-commit hook matches `sk-[a-zA-Z0-9_-]{32,}` against file path slugs in .md docs (e.g. `sk-source-scan-idle-replan-boundary-governance`). These are not API keys.

## Expected

False positive detection should also cover double-quote and unquoted YAML file path references, not just backtick-quoted ones.
