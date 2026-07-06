---
local_id: I-20260322-0115
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260322-0115/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '44'
    url: https://github.com/chatterzhao/freely/issues/44
    synced_at: '2026-04-27T11:16:20Z'
  gitee:
    issue_id: IJFO68
    url: https://gitee.com/zhaoquan/freely/issues/IJFO68
    synced_at: '2026-04-27T13:14:42Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/human/cli-first-entrypoint-and-observability-surface-unification/raw-20260322-0115issues/cli-first-entrypoint-and-observability-surface-unification.md
last_synced_comment_at:
  github: '2026-04-27T11:16:20Z'
hash: ''
created_at: '2026-04-27T11:16:20Z'
updated_at: '2026-04-27T11:16:20Z'
platform_state: closed
---

Freely 已经有：

- `freely start`
- `freely chat`
- `freely tui`
- `freely live-status / baseline-status / fleet-status`

但当前仍缺少一条明确的 canonical contract：

1. 用户应只把 `freely` 当作正式前台命令，而不是在外部 AI 工具 TUI 与 Freely 之间切换。
2. `chat` 是高层 human entrypoint，但 `tui` 还没有严格复用同一条 post-submit runtime chain。
3. CLI status family 已形成 backend 可观测面，但尚未被明确为未来 TUI/GUI 的 canonical backend interface。

canonical: docs/B2-docs/human/cli-first-entrypoint-and-observability-surface-unification/raw-20260322-0115issues/cli-first-entrypoint-and-observability-surface-unification.md
