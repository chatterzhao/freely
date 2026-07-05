---
local_id: I-20260405-2358-D
kind: linked
phase_state: completed
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '117'
    url: https://github.com/chatterzhao/freely/issues/117
    synced_at: '2026-04-27T11:25:29Z'
  gitee:
    issue_id: IJFO8Y
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8Y
    synced_at: '2026-04-27T13:16:38Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/human/cli-help-and-dry-run-contract-followthrough-governance/issues/cli-help-and-dry-run-contract-followthrough-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:25:29Z'
hash: ''
created_at: '2026-04-27T11:25:29Z'
updated_at: '2026-05-17T08:01:54Z'
platform_state: closed
---

canonical CLI replay still exposes a narrow but important contract gap:

1. `wt-create --help` currently enters the creation path and can reach Git side effects before failing.
2. `wt-enter --help` and `wt-add --help` do not expose an explicit sourced-help success path.
3. `pr-merge-guarded --help` and top-level `freely --help` print usage but still signal error.
4. `ai switch codex --dry-run --format json` still runs the heavy auto-probe flow, so the output is not a bounded dry-run contract.

Thes

canonical: docs/B2-docs/human/cli-help-and-dry-run-contract-followthrough-governance/issues/cli-help-and-dry-run-contract-followthrough-governance.md
