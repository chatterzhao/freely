---
local_id: I-20260319-2315
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260319-2315/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '24'
    url: https://github.com/chatterzhao/freely/issues/24
    synced_at: '2026-04-27T11:14:12Z'
  gitee:
    issue_id: IJFO5I
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5I
    synced_at: '2026-04-27T13:14:09Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/human/cli-tui-human-interruption-input/raw-20260319-2315issues/cli-tui-human-interruption-input.md
last_synced_comment_at:
  github: '2026-04-27T11:14:12Z'
hash: ''
created_at: '2026-04-27T11:14:12Z'
updated_at: '2026-04-27T11:14:12Z'
platform_state: closed
---

Freely 需要一个真正可用的 CLI 前台插话入口，但这个入口必须继续服从既有 human interruption 架构：

- 人类输入最终仍然进入 `.freely/intake/**`
- TUI 只是 `freely intake chat` / `freely intake status` / `freely status` 的 presentation shell
- 人类侧不直接 claim / resolve
- 中文输入与展示必须可用
- 输入框应支持多行内容，而不是只接受单行脚本式输入

canonical: docs/B2-docs/human/cli-tui-human-interruption-input/raw-20260319-2315issues/cli-tui-human-interruption-input.md
