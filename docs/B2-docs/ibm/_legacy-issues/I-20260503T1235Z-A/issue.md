---
local_id: I-20260503T1235Z-A
issue_title: "fix: defer worker auto-recovery to after first AI patrol"
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
promoted_from: raw-20260503T1235Z
source_candidate: docs/B1-docs/raw-20260503/candidates.md#C-20260503T1235Z-A
platform_ids:
  github:
    issue_id: "186"
    owner: chatterzhao
    repo: freely
  gitee:
    issue_id: ""
primary_platform: github
canonical_issue_path: "docs/B2-docs/ibm/_legacy-issues/I-20260503T1235Z-A/issue.md"
hash: ""
created_at: "2026-05-03T12:39:03Z"
updated_at: "2026-05-14T07:30:00Z"
session_refs:
  - {tool: ccds, session_id: "20260503-auto-recovery-race", role: "author"}
platform_state: closed
---

## Implementation

Modified `manager_runtime_recover_workers_if_needed` to accept a `skip_continuity_recovery` parameter.
On the supervisor's first cycle (`FIRST_ROUND=true`), continuity-based worker recovery is skipped
because the fleet cache isn't populated until `build_prompt` runs.

### Changes

- `docs/system/workspace/scripts/runtime/freely`: Added `skip_continuity_recovery` parameter to
  `manager_runtime_recover_workers_if_needed`; supervisor loop passes `$FIRST_ROUND` as the guard.
- First-round workers are launched via the post-AI-cycle handler (`delegate_workers` exit contract),
  which already existed and was unaffected.

### Verification

- Selfhost test passed: packaged daemon completes first cycle without premature worker launch.
