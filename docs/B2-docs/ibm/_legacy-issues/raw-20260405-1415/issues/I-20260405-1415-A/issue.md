---
local_id: I-20260405-1415-A
kind: linked
phase_state: absorbed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260405-1415/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '108'
    url: https://github.com/chatterzhao/freely/issues/108
    synced_at: '2026-04-27T11:24:28Z'
  gitee:
    issue_id: IJFO8N
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8N
    synced_at: '2026-04-27T13:16:23Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/issues/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:24:28Z'
hash: ''
created_at: '2026-04-27T11:24:28Z'
updated_at: '2026-06-21T15:21:49Z'
platform_state: closed
---

Freely 已经在当前 Codex owner 中冻结了长期方向: tool auth/switch/probe 应逐步抽成 standalone `ai-switch-cli` backend，而 Freely 保持 control plane / orchestration / priority / recovery policy。现在缺的不是“是否要拆”，而是：

- 何时才算达到可拆分门槛
- 哪些 helper 必须先从 Freely 内部的 inline script 中收敛成可迁移的 generic surface
- 当前本机已有的 `/Users/zhaoyu/Downloads/code/my-codex-account-switch/codex-account-switch` 空骨架应如何处理

如果不先把这条边界冻结，后续很容易出现两类治理退化：

1. 过早拆分，导致 Freely 和 standalone repo 双份维护仍在变化的 tool-private file knowledge
2. 一直不拆，导致 Freely 持续吸收 backend-sp

canonical: docs/B2-docs/ibm/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/issues/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md
