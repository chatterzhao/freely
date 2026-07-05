---
local_id: raw-20260622T000033Z33Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3303'
    url: https://github.com/chatterzhao/freely/issues/3303
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T00:00:50Z'
updated_at: '2026-06-22T00:00:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

`acp-bridge.py` 的 `ACP_IDLE_TIMEOUT` 默认 900 秒（15 分钟）。AI 完全无响应时（free tier exhausted、网络断），系统白白等 15 分钟才判定失败。

当前 activity tracking 机制正确——每次 AI 输出都重置计时器，只在完全没有流式输出时才累积计时。但：
1. 900s 太长了，真正不可用时应快速判定
2. 超时后 `run-acp-prompt.py` 走 session/resume → session/new 重试，又等一轮

## 关于 A2A 检测

A2A 协议中，session/prompt 是 request-response 模式。在 AI 完成响应之前（streaming 期间），没有 A2A 状态变更事件。ACP bridge 的 `last_activity_ts` 更新依赖于 opencode 的流式输出事件——这已经是当前可用的最快检测方式。

## 修复

### acp-bridge.py

```python
# 当前
ACP_IDLE_TIMEOUT = int(os.environ.get("ACP_BRIDGE_IDLE_TIMEOUT", "900"))

# 改为
ACP_IDLE_TIMEOUT = int(os.environ.get("ACP_BRIDGE_IDLE_TIMEOUT", "180"))
```

### run-acp-prompt.py

超时后不重试 session/resume → session/new，直接退出让 runtime 走 auto_recovery：

```
当前: idle timeout → session/resume → 失败 → session/new → 又超时
改为: idle timeout → 标记 failed → exit rc=1 → runtime Layer 1 检测 → 切号
```

### config.toml 可配置

```toml
# 按工具调整超时（秒）
ACP_BRIDGE_IDLE_TIMEOUT = 180   # 3 分钟无输出即判定不可用
```

## 验证

1. 设置 `ACP_BRIDGE_IDLE_TIMEOUT=10` → 10 秒无 AI 输出即 timeout
2. timeout 后 runtime Layer 1 检测到 `network_failure` → 触发 auto_recovery
3. 正常 AI 响应时 activity tracking 持续清零，不误判

🤖 Generated with [Claude Code](https://claude.com/claude-code)
