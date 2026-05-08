# Brainstorm: ACP Bridge Restart Storm

- 来源: raw-20260508T225041Z (#261)
- 日期: 2026-05-08

## 成功标准

Freely auto-loop 的正常工作流程：

```
scan(找任务) → manager patrol(写 continuity + worker prompt)
  → worker 读 prompt 执行
    → worker 产出 handoff 交还 manager
      → 循环
```

### 主管-worker 交互模式

主管和 worker 通过**交接文档**交互，不是直接 IPC：

1. manager 写 `manager-continuity-{ts}.md`（分析结论、委派决策）
2. manager 写 `worker-prompts/{ts}-worker-{task}-{tool}.txt`（具体任务、工位、分支）
3. runtime 读取 worker prompt，启动 `claude-agent-acp` session 执行
4. worker 完成后写 handoff artifact
5. manager 下一轮 patrol 消费 handoff，更新 continuity

### ACP 的用途：缓存命中

ACP bridge 保持 `claude-agent-acp` 进程存活，目的是 **session resume** 而非 fresh start：
- resume → 上次 session 的 prompt cache 命中 → 快、便宜
- fresh start → 无 cache → 慢、贵
- 当前：每次 `end_turn` 后 `claude-agent-acp` 退出 → session 丢失 → 下次只能 fresh start
- 期望：`claude-agent-acp` 在 `end_turn` 后保持存活，等待下一个 prompt

## Discovery

daemon 运行 3 小时内触发 6 次 restart storm。三个症状指向同一根因：

### 症状 1：storm 频繁

30s 内 3+ 次 `claude-agent-acp` 重启触发 storm 保护。

### 症状 2：缓存命中率为 0

所有 cycle log 显示 `CACHE: input=0 cache_hit=0 output=0`——session 从来没能 resume，每次都是 fresh start。

### 症状 3：worker 产出无法完成

17 个 worker prompt 被生成，但 storm 在 runtime dispatch 前就中断了 session。worker prompt 停留在文件系统，从未被实际执行。

## Research

### claude-agent-acp 生命周期

```
bridge Popen claude-agent-acp --permission-mode bypassPermissions
  → initialize handshake
  → session/new 或 session/resume
  → session/prompt
  → AI 处理（tool calls 多轮）
  → end_turn（stop_reason=end_turn）
  → claude-agent-acp 进程退出（stdout 关闭）
  → bridge _ensure_server_alive() 检测 poll() != None
  → 重新 Popen + initialize
```

`claude-agent-acp` 在 `end_turn` 后**必然退出**。这是 ACP 协议设计——每个 session 结束进程即退出。

### 为何进程退出是问题

不是 "crash" 问题，是 **session 连续性** 问题：

| | 当前（进程退出） | 期望（进程存活） |
|---|---------------|---------------|
| 下一个 prompt | 新 Popen → initialize → session/new | session/prompt |
| 缓存 | cold start，cache miss | warm，cache hit |
| 延迟 | +2-5s initialize overhead | 即时响应 |
| storm 风险 | 快速 cycle 累积重启计数 | 无进程 churn |

### Storm 触发路径

1. `claude-agent-acp` 启动后立即退出（空转，`CACHE: input=0 output=0`）
2. bridge 检测到死进程，立即重启
3. 新进程同样立即退出
4. 3 次/30s → daemon storm 保护触发
5. supervised hold → 等待 cooldown → bootstrap handoff

空转原因可能是 `claude-agent-acp` 初始化阶段的问题（API key、model、session 状态），不是 bridge 问题。

## Decision

目标：让 `claude-agent-acp` 在 `end_turn` 后保持存活，等待下一个 prompt。

### 首选：bridge 保持 server 存活

如果 ACP 协议支持 "一个进程多个 session"——在 `end_turn` 后不退出，等待新的 `session/new`。bridge 在 `_ensure_server_alive()` 中检测到进程存活即复用，不重启。

**风险**：`claude-agent-acp` 可能不支持多 session 模式。需要验证。

### 备选 A：bridge cooldown（降级方案）

如果 `claude-agent-acp` 必须退出，bridge 在重启间加入指数退避 cooldown（10s → 20s → 40s，max 120s），避免触发 daemon storm。不解决缓存命中问题，但至少消除 storm。

### 备选 B：daemon 层区分退出原因

daemon 区分 "正常 end_turn 退出" vs "异常空转退出"。正常退出不计入 storm 计数。需要 bridge 向 daemon 报告退出原因。

### 不做

- 不修改 `claude-agent-acp` 源码（外部依赖）
- 不改变 manager-worker handoff 模式
- 不削弱 daemon storm 保护参数
