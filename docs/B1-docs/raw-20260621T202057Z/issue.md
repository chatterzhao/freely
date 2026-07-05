---
local_id: raw-20260621T202057Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T202057Z-A
platform_ids:
  github:
    issue_id: '3290'
    url: https://github.com/chatterzhao/freely/issues/3290
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T20:21:13Z'
updated_at: '2026-06-22T02:19:11Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

`manager_runtime_launch_workers_after_ai_cycle_if_needed` 启动 Worker 前只检查 worktree 是否存在，不检查该 raw_key 对应的 raw issue 是否有效。导致：

1. raw issue 已被关闭（absorbed/completed/dropped）→ Worker 仍被反复委派和重试
2. raw issue 不存在 → Worker 拿到空 raw_key 也能 submitted，反复失败
3. Manager 和 Runtime 之间没有"该不该委派"的最后一道检查

## 设计

在 Runtime 启动 Worker 之前（worktree 检查之后），加一道 raw issue 有效性闸门：

```
对每个 submitted worker task:
  │
  ├─ 1. 查 worktree 是否存在（已有）
  │
  ├─ 2. [NEW] 查 raw issue 是否存在且 open
  │   raw_file="docs/issues/raw-${raw_key}/issue.md"
  │   phase=$(grep "phase_state:" "$raw_file")
  │
  ├─ raw issue 不存在:
  │   → 标记 failed
  │     原因: "raw-${raw_key} 没有对应的 raw issue，请检查 raw_key 是否正确"
  │
  ├─ raw issue 已关闭 (absorbed/completed/dropped):
  │   → 标记 failed
  │     原因: "raw-${raw_key} 已关闭 (phase_state=${phase})，请检查是否过时或有替代 issue"
  │
  ├─ raw issue open + worktree 不存在:
  │   → 标记 input-required
  │     原因: "raw issue open 但工位不存在，请 Manager wt-create"
  │
  └─ raw issue open + worktree 存在:
     → 正常启动 Worker
```

## 阻塞提示示例

```
[GATE] Worker launch blocked: raw-20260621T123324Z

  raw issue 不存在: docs/issues/raw-20260621T123324Z/issue.md
  请仔细检查该任务是否有对应的 raw issue。
  按 raw_key 查找: gh issue list --search "raw-20260621T123324Z in:title"
  或语义搜索: gh issue list --search "关键词 in:title" --state open
```

```
[GATE] Worker launch blocked: raw-20260522T053702Z

  raw issue 已关闭: phase_state=absorbed
  请检查为什么是关闭的:
  - 应该 open? → 重新打开 raw issue，再委派
  - 已经过时? → 用 a2a_task.py update --state failed 标记
  - 有替代 issue? → 用新的 raw_key 委派
```

## 验证

- 已关闭 raw issue 的 task → 不会被反复 launch，直接标记 failed
- 无 raw issue 的 task → 同上
- open raw issue + 无工位 → input-required，Manager 下次 patrol 建工位
- 日志显示清晰的阻塞原因

🤖 Generated with [Claude Code](https://claude.com/claude-code)
