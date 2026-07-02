# TODO: session/prompt 最优方案实现

- owner_issue: raw-20260701T085407Z

- date: 2026-07-02
- 基于: review-10 最终确认架构 + 用户讨论
- 原则: 每完成一个 Phase → subagent 评审 → pass 继续 / fail 修

## 核心发现

Bridge 的 `session/resume` 接收了 watchdog 传来的 `prompt` 参数但**丢弃了**：
- watchdog: `_acp_session_resume(sid, prompt="Reviewer 结论:...")`
- bridge handle_client: `bridge.session_resume(session_id=..., cwd=...)` ← prompt 没传
- bridge session_resume: `params = {sessionId, cwd, mcpServers}` ← 不含 prompt

**修复**: bridge 透传 prompt → `session/resume` + prompt = **一次性: 唤醒 session + 投递消息**

---

## Phase 1: 消息投递通路 (P0 — 核心断点)

- [ ] **T1.1** bridge `handle_client`: session/resume 路由时透传 `prompt` 参数
  - 文件: `acp-bridge.py` L647-651
  - 改: `bridge.session_resume(session_id=..., cwd=..., prompt=params.get("prompt"))`

- [ ] **T1.2** bridge `session_resume()`: 接受 `prompt` 参数并放入 `_send_request` params
  - 文件: `acp-bridge.py` L503-515
  - 改: `def session_resume(self, session_id, cwd=None, prompt=None):`
  - 改: `if prompt: params["prompt"] = prompt`

- [ ] **T1.3** 验证: watchdog `_acp_session_resume` 的 prompt 参数现在能送达 AI

- [ ] **T1.4** watchdog 新增 `_acp_session_prompt()` 封装函数
  - 文件: `watchdog_sse.py`
  - 作用: 语义明确的 "往活 session 发消息" 接口
  - 实现: 内部调 `_acp_session_resume(sid, prompt=msg)` (因为 resume+prompt = 投递)

---

## Phase 2: 三个 handler 决策树修正 (P0)

每个 handler 统一改为: **先试活 session prompt → 再试 resume → 最后 fork/new**

- [ ] **T2.1** `_handle_needs_reviewer` 重构
  - 文件: `watchdog_sse.py`
  - 逻辑:
    ```
    1. agent_get_session(reviewer) → sid
       ├─ sid 存在 → _acp_session_prompt(sid, task_msg) → 成功? return
       └─ sid 不存在或 prompt 失败 → 往下
    2. agent_next_free(reviewer) → rid
    3. 非 gate + Manager 活跃 → _acp_session_fork(manager→reviewer)
       ├─ 成功 → agent_assign → _acp_session_prompt → return
       └─ 失败 → 往下
    4. _acp_session_new(reviewer, rid)
       → agent_assign → _acp_session_prompt(new_sid, task_msg)
    ```

- [ ] **T2.2** `_handle_needs_worker` 重构
  - 文件: `watchdog_sse.py`
  - 逻辑: 同 T2.1 模式（fork from Manager → 安全，Manager 是中立角色）

- [ ] **T2.3** `_handle_needs_manager` 重构
  - 文件: `watchdog_sse.py`
  - 逻辑:
    ```
    1. agent_get_session(manager) → sid
       ├─ sid 存在 → _acp_session_prompt(sid, msg) → 成功? return
       └─ 失败 → 往下
    2. _acp_session_new(manager, "manager_01")
       → agent_assign → _acp_session_prompt(new_sid, msg)
    ```

---

## Phase 3: Session 生命周期完善 (P1)

- [ ] **T3.1** 确认 ACP bridge idle timeout 不会误杀空闲 session
  - 文件: `acp-bridge.py` L426-440
  - 确认: idle timeout 仅在 `session/prompt` 调用期间检测 AI 响应性
  - 确认: 两次调用的间隔期不会触发
  - 动作: 在代码注释中说明

- [ ] **T3.2** wt-close: 确认 `session/close` 路径完整
  - 文件: `wt-close`
  - 确认: Phase 4.5 和 Phase 6b 都有 ACP session close
  - 确认: agent_working.release_all 清掉绑定

- [ ] **T3.3** freely stop: 确认 session 清理路径
  - 文件: `freely`
  - 确认: supervisor 停掉 managed processes 时 bridge 关闭 → session 结束

- [ ] **T3.4** 确认 `_acp_agent_session_close` 通过 bridge 正确关闭 session
  - 文件: `freely`
  - 确认: 发送 `session/close` RPC → bridge 转发 → AI CLI tool 关闭

---

## Phase 4: a2a-exit 与 session 状态一致性 (P1)

- [ ] **T4.1** 确认 Worker 调 `a2a-exit --state input-required` 后 session 不关闭
  - Worker 的 AI CLI tool 返回 stop_reason=end_turn
  - Bridge 保持 session 存活（persistent sessions 设计）
  - 验证: bridge 日志中无 session/close

- [ ] **T4.2** a2a_tasks state 与 agent_working session 状态对齐
  - a2a_tasks state=input-required → agent_working 中 session_id 仍存在
  - a2a_tasks state=completed → wt-close 时 session/close + agent_release

- [ ] **T4.3** Skill 指令中明确 agent 交接规范
  - 文件: agent-roles.toml 或各 Skill SKILL.md
  - worker: "完成后调 a2a-exit --state input-required --reason needs-review:*。等待。对方结论会追加到你的对话里。"
  - reviewer: "审查完调 a2a-exit --state input-required --reason needs-worker-retry 或 --state completed"

---

## Phase 5: 测试 (P1)

- [ ] **T5.1** 新增 `test_session_prompt_delivery`
  - 文件: `tests/test_watchdog_sse.py`
  - 验证: prompt 参数经 bridge 送达到 session/resume RPC

- [ ] **T5.2** 更新 handler 测试覆盖新决策树
  - T5.2a: reviewer prompt 优先于 fork
  - T5.2b: worker prompt 优先于 fork  
  - T5.2c: manager prompt → resume → new 降级
  - T5.2d: gate 强制 new（不用 prompt，因为之前无 session）

- [ ] **T5.3** 新增 session lifecycle 集成测试
  - 文件: `tests/test_integration_lifecycle.py`
  - 验证: session 在 input-required 后仍存活
  - 验证: session/prompt 能投递消息到活 session

---

## Phase 6: 文档同步 (P2)

- [ ] **T6.1** 更新 brainstorms.md §19
  - session 存活模型修正（idle timeout 只检查 AI 响应性）
  - session/resume + prompt = 一次性投递机制
  - ACP/A2A 分工最终确认

- [ ] **T6.2** 更新 reviewer-agent.md
  - session/prompt 替代 session/resume 作为主要投递方式

- [ ] **T6.3** 更新 three-loop-capability-lifecycle.md
  - 补充 session 持久存活说明
  - 补充 ACP session/prompt 投递路径

- [ ] **T6.4** 更新 TODO-FINAL.md
  - 标记本 TODO 完成状态

---

## 实现顺序

```
Phase 1 (T1.1-T1.4) → 消息通路打通
  ↓ subagent review
Phase 2 (T2.1-T2.3) → handler 决策树修正
  ↓ subagent review  
Phase 3 (T3.1-T3.4) → 生命周期完善
  ↓ subagent review
Phase 4 (T4.1-T4.3) → a2a-exit 一致性
  ↓ subagent review
Phase 5 (T5.1-T5.3) → 测试覆盖
  ↓ subagent review
Phase 6 (T6.1-T6.4) → 文档同步
  ↓ final review → PR
```

## 预期效果

| 场景 | 当前 | 修复后 |
|------|------|--------|
| Worker→Reviewer 消息 | session/resume 无 prompt | session/fork + resume+prompt |
| Reviewer→Worker 消息 | session/resume 无 prompt (消息丢失!) | session/resume+prompt 到活 session |
| Reviewer→Manager 消息 | session/resume 无 prompt | session/resume+prompt 到活 session |
| 跨阶段 session 存活 | 不明确（prompt 被丢弃） | 明确：session 活着，resume+prompt 投递 |
| 同阶段多轮 review | 每次 session/new | 首次 fork，后续 resume+prompt |
