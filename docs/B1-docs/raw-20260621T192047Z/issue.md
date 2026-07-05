---
local_id: raw-20260621T192047Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3282'
    url: https://github.com/chatterzhao/freely/issues/3282
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T19:21:04Z'
updated_at: '2026-06-21T19:21:04Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

`wt-close` 当前在 Phase 5 删除工位前，不检查也不停止该 raw-key 下的活跃 Worker 进程。导致：

1. Worker 进程变成僵尸（工位已删，进程仍存活，cwd 指向不存在目录）
2. 同一 raw-key 被 Manager 重复委派时，累积多个僵尸进程（观察：每个 raw-key 有 2-3 个 zombie run-acp-prompt.py）
3. `auto-consume` 只标记 A2A 任务，不清理实际进程

## 设计

### 插入位置

在 Phase 4（远程分支删除）之后、Phase 5（本地工位删除）之前，插入 Phase 4.5 Worker 安全下线：

```
Phase 1: 检查 phase_state
Phase 2: 关闭平台 issue
Phase 3: Force-close trace
Phase 4: 删除远程分支
Phase 4.5: [NEW] Worker 安全下线    ← 停进程
Phase 5: auto-consume → git worktree remove → git branch -d
```

理由：Phase 1-4 是外部操作可能失败，失败时 Worker 还在可重试。Phase 4 成功后远程已干净，停 Worker 立刻删本地，窗口极小。

### Worker 安全下线流程

```
1. 查询活跃 Worker:
   a2a_task.py list --raw-key <key> --status working,submitted,launched

2. 对每个 task:
   ├─ worker_pid 为空? → skip（Worker 没启动成功）
   ├─ kill -0 $pid? → 不存在 → 标记 consumed
   ├─ 存在 → 优雅退出:
   │   ├─ 有 session_id? → session/prompt 通知
   │   ├─ 轮询状态 (每 2s，最多 10s)
   │   └─ completed/failed? → 正常退出 ✅
   ├─ 超时 → kill -TERM → 等 3s → kill -9
   └─ 标记 A2A: state → consumed

3. 安全网: 扫描该 worktree 路径的残余 run-acp-prompt 进程并 kill
```

### 防引入新 bug

| 场景 | 处理 |
|------|------|
| worker_pid 为空 | 跳过，不阻塞 |
| 进程已自然死亡 | kill -0 检测，跳过 |
| 无 session_id（旧版 Worker） | 跳过优雅退出，直接 kill |
| kill 权限不足 | 记录 error，继续执行 |
| 同一 raw-key 多个 A2A task | 逐个处理 |
| 工位已被删（orphaned branch） | 照常执行进程清理 |
| 残余子进程 | worktree 路径 grep 扫描杀残余 |

## 验证

1. 创建工位 → 委派 Worker → Worker running 时执行 wt-close
2. wt-close 日志显示: `worker shutdown: pid=<pid> method=<graceful|force>`
3. Worker 进程已退出（ps aux 确认）
4. A2A task state = consumed
5. 无僵尸 run-acp-prompt.py 残留

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
