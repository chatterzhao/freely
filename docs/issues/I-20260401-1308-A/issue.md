---
local_id: I-20260401-1308-A
kind: linked
status: completed
platform_ids:
  github:
    issue_id: "80"
    url: "https://github.com/chatterzhao/freely/issues/80"
    synced_at: "2026-04-27T11:21:56Z"
primary_platform: github
canonical_issue_path: "docs/epics/workspace-routing-foundation/build-artifact-exposure-and-release-allowlist-audit-governance/issues/build-artifact-exposure-and-release-allowlist-audit-governance.md"
last_synced_comment_at:
  github: "2026-04-27T11:21:56Z"
hash: ""
created_at: "2026-04-27T11:21:56Z"
updated_at: "2026-04-27T11:21:56Z"
---

Freely has already converged on a broader security direction: automation and enforced workflow should replace operator memory wherever possible. But the current repo still has a very practical gap:

1. build output can exist without a canonical forbidden-artifact scan,
2. there is no explicit release allowlist for output files,
3. `doctor` does not audit build artifact exposure at all, and
4. production sourcemap posture is still implicit rather than written into build truth.

This owner fixes t

canonical: docs/epics/workspace-routing-foundation/build-artifact-exposure-and-release-allowlist-audit-governance/issues/build-artifact-exposure-and-release-allowlist-audit-governance.md
