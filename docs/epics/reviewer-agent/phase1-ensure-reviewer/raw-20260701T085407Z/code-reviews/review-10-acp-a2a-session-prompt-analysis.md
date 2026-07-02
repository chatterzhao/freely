# Review 10: ACP/A2A 职责边界 + Session 启停 + 消息投递 — 最终确认

- date: 2026-07-02
- 状态: confirmed (与用户充分讨论达成一致)

## 最终确认的架构理解

### ACP 和 A2A 分工

```
A2A = 信号系统（门铃 + 留言板）      ACP = 对话系统（电话线）
──────────────────────────────      ──────────────────────────
PATCH task state                    session/new    启动新对话
SSE push 实时通知                    session/fork   从父对话分叉（继承缓存）
a2a_tasks 表持久落盘                 session/resume 复活旧对话
                                     session/prompt 往活对话发消息←核心
                                     session/close  挂电话

串联：A2A SSE 发出信号 → watchdog 消费 → ACP 启停 session + 投递消息
```

### Agent 交接闭环

```
Agent 自己的 Skill 指令里写死何时交接:
  "完成后调 a2a-exit --state input-required --reason needs-review:b1"
  "等待。对方结论会追加到你的对话里。"

watchdog 不告诉 agent 何时交接——agent 按 Skill 自己决定。
watchdog 只负责: 收到信号 → 路由 → 启动/投递到目标 agent 的 ACP session。
```

### Session 存活模型

- ACP bridge 的 180s idle timeout **只在 session/prompt 调用期间检查 AI 响应性**
- 两次 session/prompt 之间，session 持久存活，不会被杀
- Worker 做完 B1 → session 空闲等待 Review 结果 → session 活着
- Reviewer 结论回来 → session/prompt 直接投递到同一段对话

## 1. ACP 和 A2A 各自做什么

```
         ACP (纵向)                          A2A (横向)
    Agent ↔ AI CLI Tool                  Agent ↔ Agent
    ─────────────────────                ─────────────────
    
    session/new    启动新对话              task state machine  状态协调
    session/fork   从父对话分叉             SSE push            事件通知  
    session/resume 复活旧对话              Agent Card          角色声明
    session/prompt 发消息→收回复           input-required      路由信号
    session/close  关闭对话
    
    管: Agent 的"大脑"                    管: Agent 之间的"握手"
```

**串联方式**：

```
Worker 完成阶段
  │
  ├─ A2A: PATCH task → state=input-required, reason=needs-review:b1
  │     "我完成了 B1，需要 Reviewer"
  │
  ├─ A2A SSE: 推送事件到 watchdog
  │     "叮！Worker 需要 Reviewer"
  │
  ├─ ACP: session/fork from Manager → 创建 Reviewer session
  │     "从 Manager 的对话分叉一个新对话给 Reviewer"
  │
  ├─ ACP: session/prompt → 投入审查任务
  │     "这是 B1 产物路径: docs/epics/.../brainstorms.md，请审查"
  │
  └─ Reviewer 审查 → 产出 verdict
       │
       ├─ A2A: PATCH task → state=input-required, reason=needs-worker-retry
       │     "审查完毕，需要 Worker 修"
       │
       ├─ A2A SSE: 推送事件到 watchdog
       │     "叮！Reviewer 有结论给 Worker"
       │
       └─ ACP: session/prompt → 投入 verdict
             "Reviewer 说 fail: 根因分析不充分，请修复"
```

**ACP session/prompt 是消息体，A2A SSE 是通知铃。**

## 2. Session 启停决策树（修正后）

### 启动 session

```
需要给某个 agent 发消息
  │
  ├─ agent_working 表里有 session_id？
  │   ├─ YES → 用 session/resume 试一下（会话可能被 stop_ai 关了）
  │   │   ├─ resume 成功 → ✅ 会话恢复，继续用
  │   │   └─ resume 失败 → 往下走
  │   │
  │   └─ NO → 往下走
  │
  ├─ 可以从 Manager fork？
  │   ├─ YES + 同 tool → session/fork
  │   │   └─ 继承 Manager 的 CLAUDE.md/CONSTITUTION/代码库理解
  │   │
  │   └─ NO 或跨 tool → session/new
  │       └─ 冷启动，加载全部上下文
  │
  └─ Gate 审查 (needs-review:gate) → session/new 强制
      └─ 公正性 > 缓存
```

### 投递消息

```
session 已就绪（无论 new/fork/resume 哪种方式启动的）
  │
  └─ ACP: session/prompt(sessionId, message)
       │
       ├─ message 内容:
       │   "你的角色: Reviewer
       │    审查阶段: B1
       │    产物路径: docs/epics/.../brainstorms.md
       │    验收标准: 根因分析是否充分，candidate 格式是否完备"
       │
       └─ AI 收到后 → 在**同一段对话里**继续处理
           → 产出结果 → A2A PATCH 状态
```

### 关闭 session

```
wt-close 时：
  ├─ ACP: session/close(sessionId) → 正常关闭
  └─ agent_working: agent_release_all(raw_key)

freely stop 时：
  └─ supervisor 清理所有 managed processes → bridge 关闭 → session 结束

特殊情况：
  └─ stop_ai（Manager 无事可做）
      └─ session/close → 等下一轮 scan 重新 session/new
```

## 3. 当前代码需要改什么

### 3.1 watchdog_sse.py：新增 `_acp_session_prompt()`

```python
def _acp_session_prompt(project: str, session_id: str, prompt_text: str) -> Optional[dict]:
    """Send a prompt to an ALIVE ACP session.
    
    This is the PRIMARY mechanism for agent-to-agent communication.
    session/prompt sends a message and waits for the AI's response.
    """
    params = {"sessionId": session_id, "prompt": prompt_text}
    return _acp_rpc(project, "session/prompt", params)
```

当前缺失。ACP bridge 已经有 `session_prompt()` 方法（L525），只需要 watchdog 封装。

### 3.2 watchdog_sse.py：修改三个 handler

**`_handle_needs_reviewer`** — 当前：resume → fork → new。改为：

```
1. agent_get_session(reviewer) → session_id
   ├─ session 存活 → session/prompt(sid, review_task)  ← 改这里
   └─ session 死了 → session/resume → 成功? prompt : 往下

2. 没有 session → session/fork from Manager → prompt
3. fork 失败 → session/new → prompt
```

**`_handle_needs_worker`** — 当前：resume → fork → new。改为同上。

**`_handle_needs_manager`** — 当前：resume。改为：
```
1. agent_get_session(manager) → session_id
   ├─ session 存活 → session/prompt(sid, message)
   └─ session 死了 → session/resume → prompt
```

### 3.3 agent_working 表：记录 session 存活状态

当前 `agent_id:session_id` 格式无法区分"session 活着"还是"session 死了但记录还在"。

改为 `agent_id:session_id[:mode]`：
```
manager_01:ses_abc        → session 存活
worker_03:ses_def:fork     → forked session，存活
reviewer_05:ses_ghi:new    → new session，存活
reviewer_05               → 已分配但无 session（未启动）
```

实际不需要额外字段——ACP bridge 的 `session/resume` 调用本身就是存活检测：成功=活着，失败=死了。

### 3.4 ACP bridge：不需要改

`session/prompt` 已经在 bridge 原生的 `_send_request("session/prompt", params)` 路径里（L426）。

新加的 `session/fork` 已经在 L650 处理。

## 4. 更新后的完整时序

```
Worker B1 完成
  │
  ├─ A2A: PATCH {state: input-required, reason: needs-review:b1, raw_key, from_agent}
  │
  ├─ A2A SSE → watchdog
  │
  ├─ watchdog: agent_get_session(reviewer) → None (首次)
  ├─ watchdog: agent_next_free(reviewer) → reviewer_05
  ├─ watchdog: session/fork from Manager → "ses_rev_001"
  │   (Manager 有 CONSTITUTION/LAWS/代码库 → 缓存命中 ~80%)
  │
  ├─ watchdog: agent_assign(raw_key, reviewer, "reviewer_05:ses_rev_001")
  │
  ├─ watchdog: session/prompt(ses_rev_001,
  │     "你是 Reviewer。Worker B1 完成了 raw_key=xxx。
  │      产物: docs/epics/.../brainstorms.md。请审查根因分析是否充分。")
  │
  ├─ Reviewer AI 处理 → 审查 brainstorms.md → 产出 verdict
  │
  ├─ Reviewer: A2A PATCH {state: input-required, reason: needs-worker-retry,
  │     verdict: fail, required_fixes: ["根因分析缺少数据支撑"]}
  │
  ├─ A2A SSE → watchdog
  │
  ├─ watchdog: agent_get_session(worker) → "ses_wrk_def" (还活着!)
  │
  ├─ watchdog: session/prompt(ses_wrk_def,
  │     "Reviewer 结论: fail。原因: 根因分析缺少数据支撑。请修复 B1。")
  │
  └─ Worker AI 收到 → 在同一段对话里 → "好的，让我补充数据..."
       → 修改 brainstorms.md → 重新 a2a-exit
```

**关键**：Worker 的 session `ses_wrk_def` 从 B1 完成到收到 Reviewer 结论，一直活着，没有被杀。`session/prompt` 把 Reviewer 的结论追加到同一段对话里。

## 5. 实现优先级

| 优先级 | 改动 | 文件 | 影响 |
|--------|------|------|------|
| **P0** | 新增 `_acp_session_prompt()` | watchdog_sse.py | 打通消息投递路径 |
| **P0** | 改 `_handle_needs_reviewer` | watchdog_sse.py | prompt 替代 resume |
| **P0** | 改 `_handle_needs_worker` | watchdog_sse.py | prompt 替代 resume |
| **P0** | 改 `_handle_needs_manager` | watchdog_sse.py | prompt 替代 resume |
| **P1** | 更新 brainstorms.md §18/§19 | brainstorms.md | 文档同步 |
| **P2** | 更新测试 | test_watchdog_sse.py | 覆盖 prompt 路径 |
