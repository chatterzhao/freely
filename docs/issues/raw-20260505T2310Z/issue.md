---
local_id: raw-20260505T2310Z
issue_title: "fix: secret detection false positive on file paths with sk- prefix"
kind: raw
phase_state: closed
platform_ids:
  github:
    issue_id: '228'
    url: https://github.com/chatterzhao/freely/issues/228
primary_platform: github
created_at: '2026-05-05T23:10:22Z'
updated_at: '2026-05-05T23:10:22Z'
intake_id: 20260505T2310Z-secret-detection-false-positive
author: human
channel: github
session_refs: []
platform_state: 
---

## Problem

Pre-commit hook matches `sk-[a-zA-Z0-9_-]{32,}` against file path slugs in .md docs (e.g. `sk-source-scan-idle-replan-boundary-governance`). These are not API keys.

## Expected

False positive detection should also cover double-quote and unquoted YAML file path references, not just backtick-quoted ones.
