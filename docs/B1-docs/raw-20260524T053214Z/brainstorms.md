# Brainstorms — 20260524T053214Z--acp-tool-switch-integration

## Discovery

### 问题审视

raw-20260524T053214Z 诊断发现：`tool_switch_events` 表及配套函数已实现但从未在 ACP 路径中集成。项目从 May 21 起全部使用 ACP 模式（direct 废弃），导致 session 切换、bridge 重启场景下 session 生命周期管理完全失效。

**价值与时效性**：当前 Freely 运行时正处于死锁状态——stale session ID `3e21494d` 被反复使用，所有 AI cycle 因 "Session not found" 故障无法产出。这是阻塞级问题，必须立即修复。

**是否已被覆盖**：无其他 issue/candidate 覆盖此问题。`tool_switch_events` 的原始实现（d3c22910, a4befca9, ca422fed）是解决此问题的正确方向，但实现不完整。

### 实现方法

已选择：在现有 `tool_switch_events` 框架内补齐 ACP 路径集成，不引入新机制。4 个修复点全部在已有代码路径内。

### 深度根因

**为什么实现会遗漏？**

`select_launch_kind()` 的 ACP 路径（line 15874-15912，commit `0e4923c1`）和 `_tool_switch_launch_kind()` 的集成（line 15959+，commit `ca422fed`）是两个独立提交，从未在同一代码路径中测试过。ACP 路径的早期 return 使 `_ts_launch` 成为死代码。

`ca422fed` 的 commit message 声称 "runs before all launch kind paths" 但代码审查未验证 ACP 路径。缺少集成测试（pre-tests 中只有单元测试，所有关键函数被 mock）导致此问题未被发现。

**为什么 session 会在 bridge 重启后丢失？**

`claude-agent-acp` 进程将 session 保存在内存中。Bridge/backend 重启后所有 session 丢失。但 `session-store` 中 session 仍为 `active`，`FREELY_ACP_FIRST_LAUNCH_DONE=1` 不变，导致无限循环使用已丢失的 session。

## Convergence

### 决策

**修复策略**：在 ACP 路径中接入 `tool_switch_events`，补上 4 个集成断点 + 2 个兜底。

| 修复 | 位置 | 作用 |
|------|------|------|
| ACP 路径接入 `_tool_switch_launch_kind()` | `freely:select_launch_kind()` | cross_tool → 强制 fresh |
| `new_session_id` 回写 | `monitor-ai-acp.sh` | 下一轮可 resume |
| `_detect_acp_failure` 查 bridge log | `monitor-ai-acp.sh` | 检测 Session not found |
| `_acp_bridge_has_fatal_error` 补模式 | `freely` | 识别 Internal error |
| prompt 模式 fallback `session/new` | `run-acp-prompt.py` | 兜底恢复 |
| DB 必填字段校验 | `session-store.py` | 防止脏数据 |

**不改的**：`tool_switch_events` 表结构、`_tool_switch_launch_kind()` 核心逻辑、session-store API 语义、非 ACP 路径。

**实现已在 commit `4c146655` 完成。**

### 替代方案评估

1. **在 `select_launch_kind()` ACP 路径中完全重写 session 管理** — 否决，增加复杂度，重复实现
2. **仅在 `run-acp-prompt.py` 中兜底** — 不完整，上游仍会拿到错误 session
3. **清除所有 session-store 数据重新开始** — 治标不治本，下次 bridge 重启仍会复现
4. **当前方案** — 最小改动，补齐缺失的集成，利用已有框架

## Session Refs

- 分析 session: `0b9b64a4-7d37-4840-af5d-52194f4d3c23`
