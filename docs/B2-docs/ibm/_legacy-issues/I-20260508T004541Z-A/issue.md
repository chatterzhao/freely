---
local_id: I-20260508T004541Z-A
kind: linked
phase_state: completed
completed_at: "2026-05-19T23:20:00Z"
absorbed_at: '2026-05-16T14:27:11Z'
promoted_from: raw-20260508T004541Z41Z
source_candidate: docs/B1-docs/raw-20260508T004541Z41Z/candidates.md
canonical_issue_path: ''
platform_ids:
  github:
    issue_id: '250'
primary_platform: ''
last_synced_comment_at: {}
hash: ''
created_at: 2026-05-08 00:45:41+00:00
updated_at: '2026-05-17T12:25:41Z'
intake_id: ''
author: zhaoquan
channel: feat-execution
session_refs: []
pre_tests_path: docs/B2-docs/skill-ref-cleanup/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/skill-ref-cleanup/code-reviews
platform_state: closed
---

# I-20260508T004541Z-A: skill 引用全局改为 skill:name

- source_candidate: docs/B1-docs/raw-20260508T004541Z41Z/candidates.md
- pre_tests_path: docs/B2-docs/skill-ref-cleanup/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/skill-ref-cleanup/code-reviews

## 实现
- deploy-skills: --tools claude,codex comma-separated, FREELY_TOOLS env
- start-lead-agent.sh: 14 refs → skill:name
- compose-context-source-prompt.sh: 4 refs → skill:name
- tool-launchers.sh: 2 refs → skill:name
