---
local_id: I-20260508T004541Z-A
kind: linked
status: completed
phase_state: completed
promoted_from: raw-20260508T004541Z
source_candidate: docs/pre-brainstorms/20260508T004541Z--skill-ref-cleanup/candidates.md
canonical_issue_path: ""
platform_ids:
  github:
    issue_id: '250'
primary_platform: ""
last_synced_comment_at: {}
hash: ""
created_at: 2026-05-08T00:45:41Z
updated_at: 2026-05-08T00:45:41Z
intake_id: ""
author: zhaoquan
channel: feat-execution
session_refs: []
pre_tests_path: docs/epics/skill-ref-cleanup/verification/pre-tests.md
verification_artifact_dir: docs/epics/skill-ref-cleanup/code-reviews
---

# I-20260508T004541Z-A: skill 引用全局改为 skill:name

- source_candidate: docs/pre-brainstorms/20260508T004541Z--skill-ref-cleanup/candidates.md
- pre_tests_path: docs/epics/skill-ref-cleanup/verification/pre-tests.md
- verification_artifact_dir: docs/epics/skill-ref-cleanup/code-reviews

## 实现
- deploy-skills: --tools claude,codex comma-separated, FREELY_TOOLS env
- start-lead-agent.sh: 14 refs → skill:name
- compose-context-source-prompt.sh: 4 refs → skill:name
- tool-launchers.sh: 2 refs → skill:name
