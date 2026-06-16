---
local_id: I-20260405-2358-C
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '116'
    url: https://github.com/chatterzhao/freely/issues/116
    synced_at: '2026-04-27T11:25:22Z'
  gitee:
    issue_id: IJFO8X
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8X
    synced_at: '2026-04-27T13:16:36Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/issues/cli-wrapper-packaging-and-regression-surface-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:25:22Z'
hash: ''
created_at: '2026-04-27T11:25:22Z'
updated_at: '2026-05-17T08:01:52Z'
platform_state: closed
---

本轮 `bin/` 全量命令审计已经证明，Freely 现在的 CLI 能力不只是 runtime 语义问题，还存在一层更前置的包装层回归：

1. 若干 `bin/` wrapper 与 test wrapper 文件存在，但默认 shell 不能直接执行。
2. `freely ai --help` 在输出 usage 前会先泄漏 shell 错误。
3. 至少一个 auth-change wake regression 在不同 worktree 上表现不稳定。

这类问题如果不先收束，会直接污染后续所有 CLI-first 验证，因为“命令存在”并不等于“命令入口契约稳定”。

canonical: docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/issues/cli-wrapper-packaging-and-regression-surface-governance.md
