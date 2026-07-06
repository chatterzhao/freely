---
local_id: I-20260319-1715
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260319-1715/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '23'
    url: https://github.com/chatterzhao/freely/issues/23
    synced_at: '2026-04-27T11:14:08Z'
  gitee:
    issue_id: IJFO5H
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5H
    synced_at: '2026-04-27T13:14:08Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/human/human-chat-intake-and-manager-delegation/issues/human-chat-intake-and-manager-delegation.md
last_synced_comment_at:
  github: '2026-04-27T11:14:08Z'
hash: ''
created_at: '2026-04-27T11:14:08Z'
updated_at: '2026-04-27T11:14:08Z'
platform_state: closed
---

Freely 已经有 human chat intake 的最小闭环，但要真正“用 Freely 开发 Freely”，还必须把这条链变成正式、可恢复、可监督的 canonical issue：

- human chat 必须先进入 durable intake，而不是只存在于当前聊天线程
- manager 必须能 notice / claim / delegate，而不是仅仅“看过”
- specialized AI 必须产出 resolution artifact，并把 absorption target 写回 canonical pool
- `claim/resolve`、`skill:human-interruption-handling` 与 manager contract 必须共用同一套语义

canonical: docs/B2-docs/human/human-chat-intake-and-manager-delegation/issues/human-chat-intake-and-manager-delegation.md
