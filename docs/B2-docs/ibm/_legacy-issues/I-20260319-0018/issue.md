---
local_id: I-20260319-0018
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '21'
    url: https://github.com/chatterzhao/freely/issues/21
    synced_at: '2026-04-27T11:13:59Z'
  gitee:
    issue_id: IJFO5F
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5F
    synced_at: '2026-04-27T13:14:05Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:13:59Z'
hash: ''
created_at: '2026-04-27T11:13:59Z'
updated_at: '2026-04-27T11:13:59Z'
platform_state: closed
---

Freely 现在已经有：
- `context_ratio` 预警
- `context compacted` 触发
- `fresh_with_handoff`
- session handoff
- manager bootstrap handoff

但这些能力还没有收敛成“自动、低 token、统一边界”的上下文管理控制面。

当前缺口：
1. `context warn` 与 `fresh_with_handoff` 之间缺少统一的主动 continuity 策略。
2. 旧会话证据（`session_id` / `jsonl_path` / `cycle_log`）还没有形成“按需引用而不是默认重喂”的正式规则。
3. manager continuity 与 worker continuity 的目标对象不同，但当前还没有一套明确的正式口径。
4. 在官方未公开非交互压缩参数前，Freely 需要有明确 fallback；若官方未来支持，应优先重构采用。

canonical: docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md
