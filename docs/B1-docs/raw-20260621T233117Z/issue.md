---
local_id: raw-20260621T233117Z17Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3300'
    url: https://github.com/chatterzhao/freely/issues/3300
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T23:31:33Z'
updated_at: '2026-06-21T23:31:33Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

freely 中有 11+ 处工具名/前缀硬编码，导致：

1. **故障检测失效**：`L21349` 只对 `codex*` 做网络故障检测，`opencode`/`claude`/`gemini` 等工具的 rc=1 和 idle timeout 不触发 `slot_switch_reason` → 永不切号
2. **新工具需要改代码**：添加新 AI CLI tool（如 `gemini-apikey-xxx`）需要修改多处 if/case 分支
3. **违背设计初衷**：slot 目录本就是"用户随便扩展"的机制，但扩展后故障检测、slot 切换都不生效

## 全部硬编码位置

### freely (主运行时，8 处)

| 行号 | 条件 | 影响 |
|------|------|------|
| L608 | `codex*` | slot_switch 支持检测 |
| L682 | `codex*` | auto_switch_slot 可用性 |
| L4427 | `codex` | slot 解析逻辑 |
| L4439 | `codex` | 活跃 slot 读取 |
| L7729 | `kiro-cli` | 订阅状态检测 |
| L7733 | `kiro-cli` | 月度限额检测 |
| L13892 | `codex*` | session handling |
| **L21349** | **`codex*`** | **故障检测 + slot_switch_reason 设置** ← 本次根因 |
| L21207 | `codex*` | session_id 写入 |
| L21225 | `codex*` | slot reset 逻辑 |
| L23541 | `codex*` | probe 模式 |

### start-lead-agent.sh（1 处）

| 行号 | 条件 | 影响 |
|------|------|------|
| L217 | `opencode-*\|codex-*\|claude-*` | 工具名前缀归一化 |
| L223 | 硬编码工具名列表 | 合法性校验 |

### tool-launchers.sh（1 处）

| 行号 | 条件 | 影响 |
|------|------|------|
| L71 | `$HOME/.codex/slot-switch.lock` | slot 锁路径硬编码 codex |

## 设计：基于 tool-registry.json5 的能力声明

`tool-registry.json5` 已是工具能力的单点注册（acp、permission、session 等）。应该扩展它来声明**故障检测能力**和**slot 切换策略**：

```json5
{
  "opencode": {
    "acp": { "binary": "opencode", "args": ["acp"] },
    "failure_detection": {
      "network_patterns": "universal",    // 使用通用网络故障检测
      "quota_patterns": "universal",      // 使用通用配额检测
      "slot_switch": "acp_same_tool"      // ACP 同工具切 slot
    },
    "slot": {
      "lock_path": "$HOME/.ai-auth/{tool}/slot.lock"  // 模板化路径，不硬编码
    }
  },
  "claude": { ... },
  "codex": {
    "failure_detection": {
      "rate_limit_from_usage": true,      // codex 专属: 从 usage 百分比算 rate limit
      "usage_limit_patterns": true,       // codex 专属: 日志中匹配 usage limit
      "auth_failure_patterns": true       // codex 专属: 认证失败检测
    }
  },
  "kiro-cli": {
    "failure_detection": {
      "monthly_limit_patterns": true,
      "subscription_error_patterns": true
    }
  }
}
```

### 重构后的故障检测流程

```
1. 读 tool-registry.json5 获取当前工具的 failure_detection 配置
2. Layer 1 (universal): 所有工具都执行
   - log_has_execution_network_failure (timeout, connection, TLS)
   - _acp_bridge_has_fatal_error
   - log_has_ai_quota_exhausted (free usage, quota, 429) ← NEW
3. Layer 2 (tool-specific): 按 registry 配置执行
   - rate_limit_from_usage → codex 专属
   - monthly_limit → kiro 专属
   - auth_failure → codex 专属
4. 设置 slot_switch_reason → 触发 auto_recovery
```

### 涉及文件

| 文件 | 改动 |
|------|------|
| `freely` | 重构 L21349 附近故障检测、L608/L682/L13892 等 codex 硬编码 |
| `start-lead-agent.sh` | L217/L223 改为读 registry |
| `tool-launchers.sh` | L71 slot 锁路径改为模板化 |
| `tool-registry.json5` | 新增 `failure_detection` 和 `slot.lock_path` 字段 |
| `acp-bridge.py` | idle timeout 后向 freely 报告原因 |

### 验证

1. `opencode-*` 工具遇到 idle timeout → `slot_switch_reason=network_failure` → 切号
2. 新工具只需在 registry 注册，故障检测自动生效
3. `AI_FALLBACK_TOOLS` 中的 fallback 工具按配置执行检测

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
