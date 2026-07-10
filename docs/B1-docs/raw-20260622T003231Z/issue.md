---
local_id: raw-20260622T003231Z31Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260622T003231Z-A
platform_ids:
  github:
    issue_id: '3307'
    url: https://github.com/chatterzhao/freely/issues/3307
primary_platform: github
canonical_issue_path: docs/issues/I-20260622T003231Z-A/issue.md
created_at: '2026-06-22T00:32:48Z'
updated_at: '2026-06-22T00:32:48Z'
author: platform
channel: github
platform_state: closed
---

Fix pre-push.sh local keyword for macOS bash compat

The pre-push hook uses 'local' keyword outside a function at line 13, which fails on macOS bash 3.x. This blocks git push --delete operations.
Fix: replace 'local' with compatible pattern.
