---
local_id: I-20260320-0018
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '25'
    url: https://github.com/chatterzhao/freely/issues/25
    synced_at: '2026-04-27T11:14:16Z'
  gitee:
    issue_id: IJFO5K
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5K
    synced_at: '2026-04-27T13:14:14Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/default-project-resolution-and-authorized-project-memory/issues/default-project-resolution-and-authorized-project-memory.md
last_synced_comment_at:
  github: '2026-04-27T11:14:16Z'
hash: ''
created_at: '2026-04-27T11:14:16Z'
updated_at: '2026-04-27T11:14:16Z'
platform_state: closed
---

Freely 的 CLI-first 人类入口已经可用，但默认项目解析仍然需要被固定为：

- `--project` 是 override，不是日常默认必填。
- `chat` / `tui` / `intake status` / `status` 应优先解析当前项目。
- 只有一个已授权项目时，CLI 可以在外部目录回退到该项目。
- 解析逻辑不能把任意目录误判为项目。

canonical: docs/B2-docs/ibm/default-project-resolution-and-authorized-project-memory/issues/default-project-resolution-and-authorized-project-memory.md
