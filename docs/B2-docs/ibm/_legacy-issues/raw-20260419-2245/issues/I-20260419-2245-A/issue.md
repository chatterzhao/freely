---
local_id: I-20260419-2245-A
kind: linked
phase_state: completed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260419-2245/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '158'
    url: https://github.com/chatterzhao/freely/issues/158
    synced_at: '2026-04-27T11:28:30Z'
  gitee:
    issue_id: IJFOAC
    url: https://gitee.com/zhaoquan/freely/issues/IJFOAC
    synced_at: '2026-04-27T13:17:38Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/runtime-claude-launch-and-session-evidence-governance/issues/runtime-claude-launch-and-session-evidence-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:28:30Z'
hash: ''
created_at: '2026-04-27T11:28:30Z'
updated_at: '2026-05-17T12:24:59Z'
platform_state: closed
---

Manual replay narrowed the tool-switch failure to two concrete seams:

1. Freely launched Claude-family `-p/--print` calls by passing prompt text on argv together with `--add-dir`, but current Claude CLI behavior required the prompt to be delivered via stdin in this path.
2. Freely could record a freshly generated Claude session id and later reuse it as a resume target without any verified Claude session evidence on disk.
3. That combination made a fallback tool look broken or hung even when `cl

canonical: docs/B2-docs/runtime/runtime-claude-launch-and-session-evidence-governance/issues/runtime-claude-launch-and-session-evidence-governance.md
