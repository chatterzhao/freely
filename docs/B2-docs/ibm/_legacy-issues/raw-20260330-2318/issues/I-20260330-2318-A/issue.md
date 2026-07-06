---
local_id: I-20260330-2318-A
kind: linked
phase_state: absorbed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260330-2318/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '70'
    url: https://github.com/chatterzhao/freely/issues/70
    synced_at: '2026-04-27T11:21:22Z'
  gitee:
    issue_id: IJFO78
    url: https://gitee.com/zhaoquan/freely/issues/IJFO78
    synced_at: '2026-04-27T13:15:19Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/manager-attach-reuse-missing-ai-repair-governance/issues/manager-attach-reuse-missing-ai-repair-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:21:22Z'
hash: ''
created_at: '2026-04-27T11:21:22Z'
updated_at: '2026-05-17T12:21:08Z'
platform_state: closed
---

`develop` live validation finally proved the false `already_running_attach` path. After a correct `tool_auto_switch_selected previous_tool=kiro-cli active_tool=codex`, the manager bootstrap immediately emitted `supervisor_attach_reuse ... ai_pid_state=missing role_hint=manager` and rewrote workcell state to `running/up/up/already_running_attach`.

That means the defect is narrower than a general `live-status` redesign:

1. manager attach reuse can accept a live supervisor without a confirmed liv

canonical: docs/B2-docs/ibm/manager-attach-reuse-missing-ai-repair-governance/issues/manager-attach-reuse-missing-ai-repair-governance.md
