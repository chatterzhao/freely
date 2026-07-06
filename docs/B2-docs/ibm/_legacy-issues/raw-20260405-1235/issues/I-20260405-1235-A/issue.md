---
local_id: I-20260405-1235-A
kind: linked
phase_state: absorbed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260405-1235/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '107'
    url: https://github.com/chatterzhao/freely/issues/107
    synced_at: '2026-04-27T11:24:22Z'
  gitee:
    issue_id: IJFO8M
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8M
    synced_at: '2026-04-27T13:16:22Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/packaging/issues/tool-authorization-bootstrap-and-post-consent-materialization-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:24:22Z'
hash: ''
created_at: '2026-04-27T11:24:22Z'
updated_at: '2026-05-17T12:22:50Z'
platform_state: closed
---

Freely 已经冻结了 activation consent、默认自治 posture、以及一部分 per-tool materialization，但还缺一条独立 owner 来回答更具体的产品问题：

1. 用户在 `freely init`、`set-tool`、future settings mutation 中，是否显式同意了“为当前项目做 tool authorization bootstrap”。
2. Freely 对每个工具到底能自动做什么，不能自动做什么，哪些仍需 manual trust / CLI followthrough。
3. adapter 路径、tool trust、project authorization bootstrap 三者如何分层，避免 ACP 或 wrapper 被误写成“授权已完成”。
4. CLI、TUI、GUI 与 future settings 面板如何复用同一 backend contract，而不是各自发明一套同意/修复语义。

当前这层缺口已经不是 wording 问题，而是产品 contract 缺口。现有 runtim

canonical: docs/B2-docs/config/packaging/issues/tool-authorization-bootstrap-and-post-consent-materialization-governance.md
