# Session Lifecycle Protocol

本文件定义 Freely 的 AI session 管理协议。session ID 的生成、分叉（fork）、续接（resume）、记录（record）必须严格遵循本协议，不得有歧义或宽松回退。

## 动机

- DeepSeek/Anthropic prompt cache 的命中与不命中价格差 40-120 倍
- Session 管理直接决定 token 成本
- 多 manager/worker 场景下，session 混乱会导致上下文污染或并发写入冲突

## 核心概念

```
Session = 一次 AI 工具调用的完整对话历史
  - 存储为 <工具-session-dir>/<session-id>.jsonl
  - 每个 session 有唯一的 UUID
  - Session 之间通过 fork 继承上下文，但写入独立文件

Agent = 一个持续工作的 AI 角色（manager 或 worker）
  - 每个 agent 在整个生命周期中使用**同一个 session ID**
  - Agent 重启时 resume 自己的 session（不换 ID）
  - Agent 委派新 agent 时，新 agent fork 父 agent 的 session（换新 ID）
```

## Session ID 生命周期

```
Agent 首次启动
  │
  ├─ session-state.env 无记录 → 生成新 UUID → fresh launch
  │   └─ 立即记录: _persist_session_anchor_early
  │
  ├─ session-state.env 有记录 → resume 自己的 session
  │   ├─ JSONL 存在 → 正常 resume
  │   └─ JSONL 不存在 → AI_RESUME_ON_RESTART=true → ERROR
  │
Agent 委派新 Worker
  │
  └─ 新 agent fork 父 agent 的 session
      ├─ 父 UUID = parent_id
      ├─ 子 UUID = 新生成
      ├─ --resume <parent_id> --fork-session --session-id <child_id>
      └─ 子 agent 记录自己的 session ID
```

## 严格规则

### 规则 1: Session ID 一旦生成，永久不换

Agent 的首次 fresh launch 生成 UUID 后，该 UUID 在此 agent 的整个生命周期中保持不变。每次重启都 resume 同一个 UUID。只有 `freely new-session` 命令可以清除记录、强制换新。

**禁止**：AI_RESUME_ON_RESTART=true 时降级为 fresh（这是最高优先级错误）。

### 规则 2: 记录必须先于 launch

Session ID 必须在 launch AI 工具**之前**写入 session-state.env。`_persist_session_anchor_early` 在 launch 前调用，确保即使 AI 被 SIGKILL，session ID 也不丢失。

### 规则 3: 记录不可被覆盖

- `write_live_session_state_if_possible` 只能写入**非空**值
- 已存在的 CLAUDE_SESSION_ID_CURRENT 不可被空字符串覆盖
- Session state 文件的写入必须原子（先写 tmp，再 rename）

### 规则 4: Resume 必须验证证据

Resume 前必须验证：
1. `CLAUDE_SESSION_ID_CURRENT` 非空
2. 对应的 JSONL 文件存在
3. 如果 AI_RESUME_ON_RESTART=true 且任一条不满足 → 硬错误，不继续

### 规则 5: Fork 产生独立 session

Worker fork 自 manager 的 session：
- Worker 继承 manager 的上下文（cache hit）
- Worker 写入自己的 JSONL 文件（不污染 manager）
- Worker 后续循环 resume 自己的 session（不知道 manager 的存在）
- Worker 的 session-state.env 记录自己的 UUID，不记录 parent_id

### 规则 6: 工具差异封装

不同 AI 工具的 fork/resume 参数不同，通过 `_tool_session_fork_args()` 统一封装：

| 工具 | 首次 launch | resume | fork |
|------|------------|--------|------|
| Claude | `--session-id <id>` | `--resume <id>` | `--resume <parent> --fork-session --session-id <new>` |
| Codex | `exec --session-id <id>` | `exec resume <id>` | `exec resume <parent>` + 后续 fork 为新 ID |
| OpenCode | `--session <id>` | `--session <id> --continue` | `--session <parent> --fork --new-session-id <new>` |
| 不支持 fork | `--session-id <id>` | 读 JSONL 前置到 prompt | 读父 JSONL → 前置到新 prompt → `--session-id <new>` |

## 并发安全

- Manager 和 worker 使用**不同的 project 路径**（不同 worktree）
- Session 目录按 project slug 隔离
- 任何两个 agent 不会写入同一个 JSONL 文件
- 不存在"共享 session"的概念；上下文共享通过 fork 实现

## 记录追踪

每个 agent 维护以下 session 元数据：

```
CLAUDE_SESSION_ID_CURRENT    # 当前 agent 的 session UUID（权威）
CLAUDE_SESSION_ID_PREVIOUS   # 上一轮的 session UUID（用于调试）
LAST_TOOL_RESUME_TARGET       # 下次 launch 的 resume target
LAST_LAUNCH_KIND              # 上次 launch 类型（fresh/resume/fork）
SESSION_PARENT_ID             # fork 来源（首次为自身 UUID）
```

这些数据写入 `<project>/.freely/run/session-state.env`，**不依赖**工具自身的 session 管理。
