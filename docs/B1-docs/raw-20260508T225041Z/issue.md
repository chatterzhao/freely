---
local_id: raw-20260508T225041Z41Z
kind: raw
phase_state: completed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '261'
    url: https://github.com/chatterzhao/freely/issues/261
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-08T22:50:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 根因分析

ACP bridge 架构：
```
daemon → Unix socket → bridge(Python) → stdin/stdout → claude-agent-acp
```

`claude-agent-acp` 在每次 `end_turn` 后退出，bridge 检测到后重启：
- 正常 cycle：prompt → AI 处理(3-8s) → end_turn → server 退出 → bridge 检测 → 重启
- 3 次重启/30s 触发 restart storm 保护

## 关键发现

1. **`claude-agent-acp` 被 bridge 以 `--permission-mode bypassPermissions` 启动**——不走 alias，`-p` 修复不完全对症
2. **socket 没丢**——bridge 进程持续运行，socket 一直存在
3. **storm 是设计行为**——bridge 的 `_ensure_server_alive()` 正确检测到 server 退出并重启，但快速 cycle 累积超过阈值

## 修复方向

- 让 `claude-agent-acp` 在 `end_turn` 后保持存活（等待下一个 prompt）
- 或在 bridge 重启间加 cooldown
- 或提高 storm 阈值/改为基于实际 crash 而非重启次数

- pre_tests_path: docs/B2-docs/acp-bridge-restart-storm/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/acp-bridge-restart-storm/code-reviews
