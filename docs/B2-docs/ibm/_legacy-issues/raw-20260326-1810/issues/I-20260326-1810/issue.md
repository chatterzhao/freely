---
local_id: I-20260326-1810
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260326-1810/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '56'
    url: https://github.com/chatterzhao/freely/issues/56
    synced_at: '2026-04-27T11:17:27Z'
  gitee:
    issue_id: IJFO6Q
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6Q
    synced_at: '2026-04-27T13:14:59Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/packaging/issues/freely-layered-architecture-and-tooling-topology.md
last_synced_comment_at:
  github: '2026-04-27T11:17:27Z'
hash: ''
created_at: '2026-04-27T11:17:27Z'
updated_at: '2026-04-27T11:17:27Z'
platform_state: closed
---

Freely 已经在多个局部真源里分别写对了部分边界，例如 `three-loop`、`tools.md`、CLI-first 与 contract/adaptor taxonomy，但仍缺一份统一的 Freely 自身产品/系统架构表达。这导致：

- `chat`、`init`、`start`、`status` family 容易和 `CLI shell / TUI shell / GUI app` 被错误并列
- 外部 AI tooling layer 缺少明确站位
- `AGENTS.md` 仍偏向“先想是不是能力”，而缺少“先判断这是 Freely 自身产品架构，还是可复用能力”的入口分流

本 issue 的目标不是扩写 `docs/system/workspace/**`，而是先把 Freely 自身架构收敛到开发期高层真源，再要求其他开发文档跟随对齐。

canonical: docs/B2-docs/config/packaging/issues/freely-layered-architecture-and-tooling-topology.md
