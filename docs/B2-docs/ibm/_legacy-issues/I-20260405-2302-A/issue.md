---
local_id: I-20260405-2302-A
kind: linked
phase_state: absorbed
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '114'
    url: https://github.com/chatterzhao/freely/issues/114
    synced_at: '2026-04-27T11:25:11Z'
  gitee:
    issue_id: IJFO8U
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8U
    synced_at: '2026-04-27T13:16:33Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/packaging/issues/worktree-helper-shell-source-compatibility-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:25:11Z'
hash: ''
created_at: '2026-04-27T11:25:11Z'
updated_at: '2026-05-17T12:23:11Z'
platform_state: closed
---

Freely 已经把 worktree boundary、`wt-create`、`sync-tooling` 与 `post-checkout` auto-bootstrap 冻结为 canonical contract，但当前 dogfood 又暴露出一个新的 CLI-first regression：

1. 文档和 `AGENTS.md` 指导用户执行 `source ./bin/wt-add ...`
2. 文档和 worktree guidance 也保留了 `source ./bin/wt-enter ...`
3. 默认 shell 环境是 `zsh`
4. 现有 `bin/wt-add` / `bin/wt-enter` wrapper 直接读取 `BASH_SOURCE`，因此在默认 `zsh` 的 source 路径上立即失败

这意味着实际 user-facing command path 已经偏离仓库真源：内部脚本仍可在 `bash` 测试里通过，但文档教给用户的正式命令在默认 shell 下坏掉。

canonical: docs/B2-docs/config/packaging/issues/worktree-helper-shell-source-compatibility-governance.md
