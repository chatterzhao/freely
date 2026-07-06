---
local_id: I-20260321-2010
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260321-2010/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '42'
    url: https://github.com/chatterzhao/freely/issues/42
    synced_at: '2026-04-27T11:16:07Z'
  gitee:
    issue_id: IJFO66
    url: https://gitee.com/zhaoquan/freely/issues/IJFO66
    synced_at: '2026-04-27T13:14:39Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/explicit-session-addressed-resume-governance/issues/explicit-session-addressed-resume-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:16:07Z'
hash: ''
created_at: '2026-04-27T11:16:07Z'
updated_at: '2026-04-27T11:16:07Z'
platform_state: closed
---

Freely 现在对不同工具的会话续接模型不一致：

- `cc` 已经使用显式 `--session-id`
- `codex` 仍默认使用 `resume --last`
- `iflow` / `kiro-cli` 也没有显式 workcell-scoped session addressing

在多进程并行下，`--last` 与弱 resume 语义都不足以表达“当前 workcell 应接哪一个会话”。

与此同时，本机研究已确认：

- `codex exec resume [SESSION_ID] [PROMPT]`

是正式 CLI primitive，并支持从 stdin 读取续发 prompt。

因此 Freely 应把：

- `explicit session-addressed resume`

定义为 canonical continuity model，而不是把：

- `resume --last`
- PTY 输入框注入

当作默认 supervisor/runtime 路径。

canonical: docs/B2-docs/ibm/explicit-session-addressed-resume-governance/issues/explicit-session-addressed-resume-governance.md
