---
local_id: I-20260401-1831-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '84'
    url: https://github.com/chatterzhao/freely/issues/84
    synced_at: '2026-04-27T11:22:13Z'
  gitee:
    issue_id: IJFO7Q
    url: https://gitee.com/zhaoquan/freely/issues/IJFO7Q
    synced_at: '2026-04-27T13:15:43Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/worker-reactivation-and-local-reentry-residual-runtime-governance/issues/worker-reactivation-and-local-reentry-residual-runtime-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:22:13Z'
hash: ''
created_at: '2026-04-27T11:22:13Z'
updated_at: '2026-05-17T12:21:40Z'
platform_state: closed
---

完成 `I-20260401-1303-A-2` 的当前 materialization slice 后，当前 worktree 只剩两条红测，而且它们都不再属于 security/materialization：

1. `test-freely-chat-worker-reactivation` 仍可能在 worker `operator_stop` 后走到 attach reuse，写出 optimistic `already_running_attach`，但没有 durable `ai.pid`。
2. `test-freely-interruption-direct-answer` 暴露出 worker-side local continuation reentry 的 canonical active-worker predicate 仍未冻结，导致 completed owner 的验证口径与现行 runtime/test truth 不再完全一致。

这已经不是新的安全基线问题，而是 workspace-routing 的 worker-runtime residua

canonical: docs/B2-docs/ibm/worker-reactivation-and-local-reentry-residual-runtime-governance/issues/worker-reactivation-and-local-reentry-residual-runtime-governance.md
