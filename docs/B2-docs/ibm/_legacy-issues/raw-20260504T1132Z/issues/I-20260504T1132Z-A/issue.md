---
local_id: I-20260504T1132Z-A
issue_title: raw key 格式统一：所有代码接受 YYYYMMDDTHHMMZ 和 YYYYMMDD-HHMM 双格式
kind: linked
phase_state: completed
promoted_from: raw-20260504T113200Z
platform_ids:
  github:
    issue_id: '203'
    url: https://github.com/chatterzhao/freely/issues/203
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/raw-key-format-unify/raw-20260504T113200Zissues/I-20260504T1132Z-A.md
created_at: '2026-05-05T00:00:00Z'
updated_at: '2026-05-05T09:54:48Z'
session_refs:
- tool: ccds
  session_id: 20260505-raw-key-unify
  role: worker
platform_state: 
---

## Scope

18 files: regex/glob patterns now accept both old (YYYYMMDD-HHMM) and new (YYYYMMDDTHHMMZ) raw key formats.

## Changes

- pre-push.sh, wt-create, task-lifecycle-scan.py, governance-merge-gate, freely: regex updated
- file-backup.sh, start-lead-agent.sh, availability-watchdog.sh: date generation → ISO 8601 UTC
- ibm-framework.md, CONSTITUTION.md, LAWS.md, AGENTS.md, 4 skill docs: format examples updated

## Code Review

docs/B2-docs/ibm/raw-key-format-unify/raw-20260504T113200Zcode-reviews/review.md
