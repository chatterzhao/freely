---
local_id: raw-20260622T000649Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260622T000649Z-A
platform_ids:
  github:
    issue_id: '3304'
    url: https://github.com/chatterzhao/freely/issues/3304
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T00:07:06Z'
updated_at: '2026-06-22T00:07:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

#3281（全面门禁）已修了硬拦截部分（pre-push git push --delete），但软拦截部分（封装命令的 --force/--skip 必须带 --reason）未实现即被 merge 自动关闭。

## 剩余需修

| 命令 | Flag | 当前 | 应改 |
|------|------|------|------|
| `wt-close` | `--force` | --reason 可选 | 无则阻塞 |
| `wt-close` | `--skip-platform` | 无 --reason | 必须带 |
| `wt-close` | `--discard-unmerged` | 无 --reason | 必须带 |
| `freely init` | `--force` | 无 --reason | 必须带 |
| `freely start` | `--force` | 无 --reason | 必须带 |
| `freely daemon start` | `--force` | 无 --reason | 必须带 |
| `freely task-mode set` | `--force` | 无 --reason | 必须带 |
| `pr-review-guarded` | `--verdict` | 无 --reason | 必须带 --reviewer |

## 阻塞提示格式

```
[GATE] 你在违规绕过门禁: <门禁名称>

  请严格执行门禁。如果确实满足绕过条件（不是偷奸耍滑），
  请加上绕过理由参数：
    --reason "具体绕过原因"

  示例: ./bin/wt-close --force --reason "emergency: worktree corrupted" <branch>
```

## 涉及文件

| 文件 | 改动 |
|------|------|
| `wt-close` | --force/--skip-platform/--discard-unmerged 强制 --reason |
| `freely` | init/start/daemon start/task-mode set 强制 --reason |
| `pr-review-guarded` | --verdict 强制 --reviewer |

🤖 Generated with [Claude Code](https://claude.com/claude-code)
