---
local_id: raw-20260517T093315Z15Z
kind: raw
priority: P2
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
source: chat-inbox
created_at: '2026-05-17T09:33:15Z'
title: session UUID 提取用 head -1 读到空行，导致 session 永不被持久化，cache 命中率为零
platform_ids:
  github:
    issue_id: '507'
    url: https://github.com/chatterzhao/freely/issues/507
    synced_at: '2026-05-17T09:33:21Z'
updated_at: '2026-05-17T09:33:21Z'
primary_platform: github
platform_state: closed
---

## 根因

cycle log 第 1 行是空行，第 2 行是 ACP 事件，第 3 行才是 UUID。两处提取都用 `head -1`：

```bash
# monitor-ai-acp.sh 行 279
session_id_clean=$(head -1 "$log_file" | grep -oE 'uuid-regex' | head -1)

# freely 行 18994
_line1_uuid=$(head -1 "$cycle_log" | grep -oE 'uuid-regex' | head -1)
```

`head -1` 读到空行 → 永远提取不到 UUID → session-store 从未写入 → `select_launch_kind` 每次都 `fresh` → 缓存命中率 0%。

## 修复

将 `head -1` 改为扫描更多行（如 `head -5`）或全文搜索：

```bash
session_id_clean=$(head -5 "$log_file" | grep -oE 'uuid-regex' | head -1)
```

## 影响

- session 持久化恢复 → resume 周期可复用会话 → prompt cache 命中（agent doc 等稳定前缀）
- `session_id=unavailable` 修复 → cache_metrics 记录真实的 token 级 cache 数据
- 每条 patrol cycle 节省 ~5KB+ token 成本

## 范围

- `docs/system/workspace/scripts/runtime/monitor-ai-acp.sh`：行 279
- `docs/system/workspace/scripts/runtime/freely`：行 18994
