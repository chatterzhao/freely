# Brainstorm: Manager keepalive 不扫描 stale PID + Worker ACP 初始化超时无自愈

## Discovery

### 来源

- Raw issue: `raw-20260521T012042Z` (GitHub #1519)
- 创建时间: 2026-05-21T01:20:55Z
- 来源渠道: GitHub issue (platform)
- 背景: 2026-05-20 Runtime Crash Postmortem 暴露的 worker 生命周期管理缺陷。该 postmortem 记录了 SIGTERM leak、error classification gap 与 stop path broken 三个失效模式，本 issue 是其衍生修复之一。

### 时效性与价值

1. **时效性高**: 昨天 postmortem 产出，问题仍存在，未修复
2. **影响面广**: Worker 死后 Manager 不感知 → 委派堵死 → 15+ 轮空等 → 整个 fleet 停摆
3. **修复边界清晰**: 子问题 1 （keepalive 扫描）有明确修复方向，改动范围小
4. **高风险**: ACP 初始化超时连续 3 次出现，说明不是偶发，是系统性过载或泄漏

**结论**: 值得投入，立即进入 brainstorm。

### 关联现有 pre-brainstorms

| 现有条目 | 关系 |
|---------|------|
| `C-20260519T015638Z-A` (systematic stale_pid, gh-601) | 研究 worker 进程在产出 handoff 前退出的根因。与本 issue 子问题 1 互补：gh-601 排查 worker 为何死，本 issue 修复 Manager 为何不检测到死。子问题 2（ACP init 超时）可能与 gh-601 的 ACP adapter 超时假设重叠。需协调。 |
| `M-20260519T145435Z-A` (consumed_by routing) | 不相关 |

---

## Research

### 子问题 1: stale_pid 只在 launch 时检查

**当前代码路径**:
- `launch_worker_from_manager_prompt_if_needed` 在派新 worker 前检查旧 worker 是否 stale（line 12109）
- Manager keepalive 主循环只做 prompt/build/launch 决策，不扫描已有 `launched` worker
- Worker 进程死后，handoff DB 中该 worker 的记录永远保持 `launched`
- Manager 每次检查只看到 "有 launched worker" → 等它完成 → 15+ 轮才最终 timeout

**影响范围**:
- Worker 进程异常退出（segfault、OOM、SIGKILL）后 Manager 无法快速发现
- 正在 closeout 的 worktree 被堵死
- Fleet cleanup 停摆

**建议修复**:
- Manager keepalive 每次扫描所有 `launched` worker
- 对每个 `launched` worker 的 PID 执行 `kill -0`（或等价的进程存在检测）
- `kill -0` 失败 → 标记 `stale_pid`
- 与 `mark_stale()` 的超时机制的关系：`kill -0` 检测的是"进程已死"（硬状态），`mark_stale()` 检测的是"超过 N 分钟无活动"（软超时）。二者应共存——`kill -0` 更快发现进程死亡，`mark_stale` 兜住进程挂起不响应的情况。

**风险**: 低。`kill -0` 是 POSIX 标准调用，无副作用。但需确保 Manager 有权限访问 Worker PID（同用户/同进程组）。

### 子问题 2: Worker ACP 初始化超时

**当前表现**:
- 最新 3 个 worker 全部在初始化阶段超时
- 日志: `[ERROR] timed out waiting for ACP response to initialize`
- Worker 进程启动了，但 Claude Agent 从未响应 initialize

**可能的根因**:
1. **ACP bridge 过载**: 并发 session 数超过 ACP bridge 容量，新的 initialize 请求被排队或丢弃
2. **API 限流**: Claude API 达到 rate limit，Agent 启动阶段就被限流
3. **Agent 启动失败**: Claude Code 进程启动后卡在认证/初始化阶段，未进入正常 session loop
4. **资源耗尽**: 系统 OOM、FD 耗尽等导致 worker 进程无法完成初始化

**建议修复方向**:
- ACP bridge 限制并发 session 数，超限时拒绝新连接（而非静默超时）
- Worker 初始化超时应自动重试或通知 Manager
- Manager 看到 worker 初始化超时不应继续等待，应主动标记失败并尝试新 worker

**与 C-20260519T015638Z-A 的关系**:
- 该 candidate 研究的 stale_pid 问题假设之一是 "ACP adapter 层面超时"
- 本 issue 的 ACP init 超时可能是该假设的具体证据
- 若 root cause 相同，子问题 2 应吸收到 C-20260519T015638Z-A 中统一处理

### 技术依赖与边界

- 修复涉及：Manager keepalive loop (`freely` runtime)、ACP bridge、handoff DB
- 不涉及：Worker prompt、Claude API 调用逻辑（Manager 本身）、前端、CLI 命令面
- 可能触及：`handoff.py mark_stale()`、`manager.py` keepalive 函数

---

## Decision

### Scope 评估

| 子问题 | 边界清晰度 | 修复可操作性 | 与现有条目重叠 |
|--------|-----------|------------|--------------|
| #1 keepalive 扫描 | 清晰 | 高，改动小 | 互补：gh-601 研究 worker 死因，本问题修复 Manager 检测 |
| #2 ACP init 超时 | 中 | 中，需先定根因 | 高：可能与 C-20260519T015638Z-A 的 ACP 超时假设重叠 |

### 结论

**用一个 candidate 覆盖两个子问题，但分离 acceptance criteria**。

理由：
1. 两个子问题共享同一代码域（Manager keepalive / worker 生命周期管理）
2. 修复链互补：只有 Manager 能检测到 dead worker（#1），Worker 才能被替换；只有 ACP 初始化能完成（#2），Worker 才有存活可能
3. 子问题 2 与 C-20260519T015638Z-A 重叠，应在 research 阶段先确定根因是否相同，再做合并决策

### 推荐下一跳

1. 创建 candidate `C-20260521T012042Z-A`，状态 `needs_research`
2. 子问题 1（keepalive 扫描）可立即进入 B2 materialize：边界明确，改动风险低
3. 子问题 2（ACP init 超时）需与 C-20260519T015638Z-A 协调研究，确认根因后决定是自己 B2 还是吸收到现有 candidate
4. 进入 M-20260521T012042Z-A milestone
