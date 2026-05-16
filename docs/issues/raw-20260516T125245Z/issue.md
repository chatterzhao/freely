---
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: '2026-05-16T12:52:45Z'
title: worker-agent.md 导致 Worker 不执行任务而是模仿 Manager 做 patrol
platform_ids:
  github:
    issue_id: '369'
    url: https://github.com/chatterzhao/freely/issues/369
    synced_at: '2026-05-16T12:52:52Z'
updated_at: '2026-05-16T12:52:52Z'
primary_platform: github
platform_state: open
---

## 根因

`worker-agent.md` 第一句话就是"接到 raw issue 工位任务后，先审视 issue 是否过时、是否仍有价值、是否已被覆盖"。

Worker 将"审视"理解为：读 LAWS.md、跑 task-source-scan、查 handoff DB——完全变成了第二个 Manager，而不是执行者。

实测：Manager 委派的 Worker prompt 有具体的 Task 步骤（rm stale test-pre-merge → create new → merge → verify），但 Worker 不执行，反而做"宪法预检"、"scan"、"handoff 查询"，然后输出 `delegate_workers`（又委派给别人）。

## 修复

### 1. Worker 执行优先原则

```
Worker 的唯一职责是**执行 Manager 委派的具体任务**。

收到 prompt 后：
1. 先读 header（Worktree/Branch/rationale/intent_kind）
2. 再读 ## Task 部分——这是你要执行的步骤
3. 验证 rationale 格式：是否为"因为{X}，所以做{Y}"？理由是否仍成立？
   - 验证耗时 < 30 秒——不要为此做 scan、读 LAWS、查 handoff
   - 格式不对或理由不成立 → 立即输出 worker_handoff_needed
4. 验证通过 → 立即开始执行 Task 步骤
5. 完成后输出 worker_done

**Worker 不负责**：
- 重新 patrol——Manager 已经做了
- 运行 scan——Manager 已经看了
- 委派其他 worker——你不是 Manager
- 判断收口时机——那是 Manager 的工作
```

### 2. 禁止输出 delegate_workers

Worker 不能委派其他 worker。如果 Worker 认为需要进一步委派，应输出 `worker_handoff_needed` 说明原因，让 Manager 决定。

### 3. 执行即任务

- prompt 的 Task 部分有具体的 shell 命令 → 直接执行
- 不要先"浏览一遍看看有没有其他事"
- 不要先"确认当前舰队状态"

## 范围

只改 `docs/system/workspace/agents/worker-agent.md`。
