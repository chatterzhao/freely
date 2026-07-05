---
local_id: I-20260403-1100-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '94'
    url: https://github.com/chatterzhao/freely/issues/94
    synced_at: '2026-04-27T11:23:09Z'
  gitee:
    issue_id: IJFO84
    url: https://gitee.com/zhaoquan/freely/issues/IJFO84
    synced_at: '2026-04-27T13:16:03Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md
last_synced_comment_at:
  github: '2026-04-27T11:23:09Z'
hash: ''
created_at: '2026-04-27T11:23:09Z'
updated_at: '2026-05-17T12:22:10Z'
platform_state: closed
---

`develop` 目前累积了一批在旧治理门禁放宽时期进入主线的 legacy governance drift。随着 `governance-merge-gate` 最近多轮收紧，这些历史断裂不再只是“文档有点旧”，而是直接阻塞 canonical `develop` 的 push 和后续 promotion followthrough。

当前问题不是一个单点 bug，而是一个链式 owner 缺口：

1. pre-brainstorm / candidate / issue / progress 真相面并不总是同时存在
2. 一部分旧 issue 缺少 `verification_artifact_dir`
3. 一部分旧 review 缺少 implementation decision note 必要字段
4. 一部分 review / candidate 仍使用旧 key 或缺少新的 continuity 字段
5. 历史上出现过的 `1200/1201/1202/1203` repair slices 已经退出当前文件系统，但 canonical docs 一度还把它们

canonical: docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md
