---
local_id: I-20260318-0930
kind: linked
status: completed
platform_ids:
  github:
    issue_id: "15"
    url: "https://github.com/chatterzhao/freely/issues/15"
    synced_at: "2026-04-27T11:13:23Z"
primary_platform: github
canonical_issue_path: "docs/epics/workspace-routing-foundation/checkpoint-commit-and-multi-worktree-supervision-governance/issues/checkpoint-commit-and-multi-worktree-supervision-governance.md"
last_synced_comment_at:
  github: "2026-04-27T11:13:23Z"
hash: ""
created_at: "2026-04-27T11:13:23Z"
updated_at: "2026-04-27T11:13:23Z"
---

Freely 当前已经会 worktree 隔离、session handoff、rate-limit account switch，但仍不会像项目负责人一样管理多个工位：

- 不能可靠判断什么时候必须先 checkpoint，而不是继续堆脏树
- 不能阻止一个 commit 同时混入 control-plane 与 product-plane
- 缺少一个 CLI-first 的工位总览，无法统一安排继续开发、冻结等待、集成批次与合并顺序

canonical: docs/epics/workspace-routing-foundation/checkpoint-commit-and-multi-worktree-supervision-governance/issues/checkpoint-commit-and-multi-worktree-supervision-governance.md
