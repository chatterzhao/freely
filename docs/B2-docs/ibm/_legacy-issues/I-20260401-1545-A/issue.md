---
local_id: I-20260401-1545-A
kind: linked
phase_state: completed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '81'
    url: https://github.com/chatterzhao/freely/issues/81
    synced_at: '2026-04-27T11:21:59Z'
  gitee:
    issue_id: IJFO7L
    url: https://gitee.com/zhaoquan/freely/issues/IJFO7L
    synced_at: '2026-04-27T13:15:39Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/acp-optional-adapter-boundary-governance/issues/acp-optional-adapter-boundary-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:21:59Z'
hash: ''
created_at: '2026-04-27T11:21:59Z'
updated_at: '2026-05-17T08:01:39Z'
platform_state: closed
---

ACP 边界已经冻结，runtime `adapter axis` 也已经 materialize 到 config / dispatch / status truth。下一步如果继续停在抽象层，只会重复“ACP 可不可以”而不产生真实判断。

第一刀 prototype 应优先选 `codex`，原因是：

1. `codex` 是当前宪法已承诺工具面，且 direct path 是 Freely 最成熟的 canonical implementation。
2. `codex` 没有 `cc-use-codex-cli` 的 nested capability 复杂度。
3. ACP 官方 agents / registry 当前已有 Codex CLI adapter 现实，因此它不是纯 speculative target。
4. Freely 对 `codex` 的 strongest contract 是 explicit resume evidence；因此第一刀 prototype 必须收窄为 fresh path，而不是一开始就假定 ACP 能无损替代 current

canonical: docs/epics/workspace-routing-foundation/codex-acp-fresh-path-prototype/issues/codex-acp-fresh-path-prototype.md
