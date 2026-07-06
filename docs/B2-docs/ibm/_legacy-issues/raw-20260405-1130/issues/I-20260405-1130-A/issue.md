---
local_id: I-20260405-1130-A
kind: linked
phase_state: absorbed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260405-1130/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '105'
    url: https://github.com/chatterzhao/freely/issues/105
    synced_at: '2026-04-27T11:24:10Z'
  gitee:
    issue_id: IJFO8K
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8K
    synced_at: '2026-04-27T13:16:19Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/packaging/issues/project-level-agents-bootstrap-and-management-contract-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:24:10Z'
hash: ''
created_at: '2026-04-27T11:24:10Z'
updated_at: '2026-05-17T12:22:44Z'
platform_state: closed
---

Freely already behaves as if project-root `AGENTS.md` were a formal product contract:

1. `freely init` creates a minimal project-level `AGENTS.md` when missing.
2. runtime and lead-agent prompts read the project root `AGENTS.md` first.
3. self-hosting Freely follows the same pattern.

But that behavior has been scattered across runtime code, tests, and high-level guidance rather than frozen as a reusable capability contract. The missing contract leaves four important boundaries implicit:

1. ex

canonical: docs/B2-docs/config/packaging/issues/project-level-agents-bootstrap-and-management-contract-governance.md
