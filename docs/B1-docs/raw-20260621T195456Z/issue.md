---
local_id: raw-20260621T195456Z56Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3286'
    url: https://github.com/chatterzhao/freely/issues/3286
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T19:55:13Z'
updated_at: '2026-06-21T19:55:13Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

# feat: Manager prompt — persistent session note + A2A pre-check + three dispatch modes

## 问题

1. Manager 对同一 raw_key 多次调用 `a2a-exit --state submitted`（观察：30 秒内 3 次空消息提交），没有区分三种合法的干预模式

2. 日志和 prompt 中 "退出" / "ai process exited" 容易误解为进程死亡。实际 Manager 是常驻 session，Runtime 通过 session/prompt 驱动每轮 patrol

## 修复

### A. Manager prompt 开头加一行说明

当前开头：
```
# Manager Agent
运行在 develop 工位。巡逻舰队、委派 Worker、判断收口。不能直接 commit——通过委派 Worker 执行。
```

改为：
```
# Manager Agent
运行在 develop 工位。巡逻舰队、委派 Worker、判断收口。不能直接 commit——通过委派 Worker 执行。
你是常驻 session —— Runtime 通过 session/prompt 驱动每轮 patrol，
a2a-exit 提交本轮决策后回到守候，进程不休。
```

不新增职责，只说清运行方式。

### B. 委派前加 A2A 检查（Step 5 补）

```
委派前查:
  a2a_task.py list --raw-key <key> --status working,submitted

有活跃 Worker → 走纠偏/重试，不重复 a2a-exit --state submitted
无活跃 Worker → 正常委派
```

### C. 三种 dispatch 明确区分

当前 prompt 已有 dispatch 描述（L34-40），但分散在评审闸门和主动纠偏两处。统一列出：

| 模式 | 场景 | 命令 |
|------|------|------|
| 委派 | 新任务 | `a2a-exit --state submitted --summary "..."` |
| 纠偏 | Worker 活着，调整方向 | `a2a_task.py prompt --task-id <id> --message "..."` |
| 重试 | Worker 死了，原 task 重来 | `a2a_task.py update --task-id <id> --state submitted` |

禁止: 同一 raw_key 同一 worker 重复 `a2a-exit --state submitted`；空 summary 委派

### D. 日志措辞

| 旧 | 新 |
|----|-----|
| ai process exited rc=0 | patrol complete, waiting for next prompt |
| launching opencode (prompt mode) | sending patrol prompt (session/prompt) |

🤖 Generated with [Claude Code](https://claude.com/claude-code)
