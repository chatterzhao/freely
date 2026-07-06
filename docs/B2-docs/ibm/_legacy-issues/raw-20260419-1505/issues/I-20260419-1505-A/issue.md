---
local_id: I-20260419-1505-A
kind: linked
phase_state: completed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260419-1505/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '156'
    url: https://github.com/chatterzhao/freely/issues/156
    synced_at: '2026-04-27T11:28:19Z'
  gitee:
    issue_id: IJFOAA
    url: https://gitee.com/zhaoquan/freely/issues/IJFOAA
    synced_at: '2026-04-27T13:17:35Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/runtime-supervisor-attach-reuse-followthrough-governance/issues/runtime-supervisor-attach-reuse-followthrough-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:28:19Z'
hash: ''
created_at: '2026-04-27T11:28:19Z'
updated_at: '2026-05-17T12:24:53Z'
platform_state: closed
---

The checkpoint branch `feature/checkpoint-lifecycle-trace-debuggability-20260419` preserves bounded runtime behavior that `develop` does not yet own:

1. Repeated `freely daemon start` should reuse a healthy same-project supervisor instead of launching another detached daemon-run process.
2. Foreground `freely start` should attach to the same live supervisor between AI cycles, including the narrower fallback where `ps` is unavailable but project ownership is still provable by cwd evidence.
3. Cl

canonical: docs/B2-docs/runtime/runtime-supervisor-attach-reuse-followthrough-governance/issues/runtime-supervisor-attach-reuse-followthrough-governance.md
