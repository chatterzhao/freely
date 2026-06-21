---
local_id: I-20260405-1615-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '110'
    url: https://github.com/chatterzhao/freely/issues/110
    synced_at: '2026-04-27T11:24:37Z'
  gitee:
    issue_id: IJFO8Q
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8Q
    synced_at: '2026-04-27T13:16:28Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/feature-owned-test-pre-merge-family-promotion-model-governance/issues/feature-owned-test-pre-merge-family-promotion-model-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:24:37Z'
hash: ''
created_at: '2026-04-27T11:24:37Z'
updated_at: '2026-06-21T15:21:53Z'
platform_state: closed
---

当前仓库对 `test-pre-merge-*` 仍停留在旧模型：

1. `feature/*` 仍被描述为可直接 merge 到 `develop` 的默认 promote 单位。
2. `test-pre-merge-*` 仍主要被描述为 shadow batch / replay 证据面。
3. multi-feature 组合测试是否只是验证证据、还是能成为 bundle promote 单位，没有被冻结。

这已经不只是命名或流程提示问题，而是 develop promotion model 本身没有冻结：

- 如果 `feature/*` 仍能直接进 `develop`，就始终存在“忘记先过 develop-like 预集成 lane”的制度逃逸面。
- 如果多个 feature 要并行做集成验证，又没有统一的 single-feature / multi-bundle 语义，就会让 `pr-merge-guarded`、hook、`governance-check`、runtime/status 在不同地方各自发明自己的模型。
- 如果在 owner issue 之前就直接

canonical: docs/epics/workspace-routing-foundation/feature-owned-test-pre-merge-family-promotion-model-governance/issues/feature-owned-test-pre-merge-family-promotion-model-governance.md
