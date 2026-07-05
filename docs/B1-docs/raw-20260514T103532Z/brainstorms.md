# Brainstorm: Agent Handoff Protocol

- 来源: raw-20260514T103532Z (#344)
- 日期: 2026-05-14
- 基于: #343 handoff pipeline disconnect 根因分析、handoffs 表实际使用情况审视

## 成功标准

Manager 和 Worker 协作良好的样子：**双方不直接通信，以 handoffs 表为唯一共享媒介，经由 Runtime 完成所有状态推进。**

具体而言——

- Manager 按 `manager-agent.md` 的表格规范，在回复末尾产出 ` ```handoff ` JSON 块。Runtime 解析、验证、合并字段后写入 DB，按 `exit_kind` 分发到对应的 `consume_*` 方法执行状态转换。Manager 无需关心 Worker 是否在线、如何启动——Runtime 替它完成。
- Worker 按 `worker-agent.md` 的表格规范产出 JSON。Worker 不知道 Manager 的 patrol 周期、不知道舰队全局——它只管执行 Task 并汇报。Worker 的完成、受阻、请求决策，全部通过 Runtime 转为 handoffs 表的状态变更，Manager 下一轮 patrol 自然可见。
- 同一 raw_key 下的所有 Manager/Worker 记录构成一条完整线程，`parent_handoff_id` 串联因果，`previous_worker_handoff_id` 串联前序。任何时候查询线程历史，能看到完整的"谁委派了谁、谁完成了什么、谁消费了谁"。
- 任何一端的 JSON 不合格，Runtime 插入结构化修复 handoff（`repair_target_role` + `validation_errors_json`），Manager 下一轮 patrol 定位并重拉，不依赖人类推断。
- Worker 持续慢但 log/PID/socket 有活跃信号 → 不超时。真正不响应时，`last_activity_at` 触发 `mark_stale → blocked`，Manager 介入重新委派或收口。
- 所有状态推进由 Runtime 的乐观锁 WHERE 子句保证——两个并发操作只有一个成功，不会出现"上一个状态被下一个覆盖"。

**一句话**：Manager 和 Worker 各写各的 JSON，Runtime 保证每条 JSON 变成一个确定性的状态转换，双方在 handoffs 表里看见彼此的工作。

## 会话模型

Manager 和 Worker 都是**多轮连续会话**，共同规律是：`fork` 创建 → `prompt`（delta turn）继续 → 上下文满或异常时 `fresh_with_handoff` 重建。

**关于 fork 的澄清**：`fork` 生成全新的 session UUID，Worker 写入自己的会话文件，与 Manager 会话完全隔离。`SESSION_PARENT_ID` 只记录谱系——Worker 知道自己"从哪来"。Worker 看到的是 `worker-agent.md`，不是 `manager-agent.md`。fork 继承的是 ACP 层面的 prompt 缓存（KV cache），不是会话内容。Worker 不会误以为自己是主管。

**Manager：一个跨 patrol 的连续会话，管理所有 issue 和所有 Worker。** 首次启动 `fresh`/`fresh_with_handoff`。后续每轮 patrol 复用同一个 ACP 会话（`prompt`，delta 模式），只注入本轮变化（fleet 更新、scan 新增、handoffs 表新记录）。一个 Manager 会话同时面对多个 issue 的多个 Worker——它不需要在会话里记住每个 issue 的细节，因为 handoffs 表是它的外部记忆。每轮 patrol 从 handoffs 表查询所有 issue 的最新状态，按 `raw_key` 线程逐个处理。上下文接近上限或异常退出时 `fresh_with_handoff`——开新会话，handoff 连续性工件恢复状态。

为什么不按 issue 拆分 Manager 会话？因为 patrol 本身就是跨 issue 的全局决策——哪些 issue 应该排队、哪些可以并行委派、哪个 Worker 的结果影响哪个 issue 的下一步——这些判断需要知道全局。按 issue 拆分会把全局视野切成碎片，每个"子 Manager"只看到自己的 issue，无法做跨 issue 的优先级和资源决策。handoffs 表承担了 per-issue 的状态存储，Manager 会话承担了跨 issue 的编排决策，各司其职。

**Worker：每个 worktree 一个持续会话。** 首次委派时 Runtime 以 `fork` 模式从 Manager 会话分出（`SESSION_PARENT_ID` 指向 Manager），Worker 获得独立的会话但继承 Manager 的上下文缓存。Worker 在 worktree 上工作——
- 做完输出 `worker_done` → 会话暂停，但**不关闭**
- 受阻输出 `worker_blocked` → 会话暂停，Manager 介入
- 需要请示输出 `worker_handoff_needed` → Runtime 生成 followthrough prompt，Manager 下一轮 patrol 读 handoffs 看到后，以 **delta turn（`prompt`）** 向同一个 Worker 会话发送纠正/澄清/继续的指令。Worker 在同一会话里继续，保留之前的代码理解和对话历史
- Worker 真正死了（PID 不存活、log 不更新、socket 无心跳）→ 会话失效，Manager 可重新委派（新的 `fork` 会话）

**一个 worktree 上的多轮对话**是常态：Manager 委派 → Worker 请示 → Manager 在 delta turn 里澄清 → Worker 继续 → Worker 说完成 → Manager 审查后追加要求 → Worker 在同一会话里补充。这就像两个人持续聊天，Manager 发消息（delta turn），Worker 回消息（handoff JSON），直到 Manager 判定这个 worktree 的工作完成，调用 `wt-close` 关闭 worktree 和 Worker 会话。

**Worker 数量与 worktree 的关系：** 一个 Worker 绑定一个 worktree，一个 worktree 同时最多一个活跃 Worker（`worktree_has_active_worker` 检查 `status=launched`）。Manager 可同时委派多个 Worker 到不同 worktree 并行工作，每个 Worker 有自己独立的持续会话。

**Manager 如何同时管理多个 Worker：** Manager 不记忆每个 Worker 的会话细节——它每轮 patrol 从 handoffs 表查询所有未消费 Worker 的状态（completed/blocked/rejected），这是 Manager 的唯一 Worker 信息源。Manager 不需要 track "Worker X 在聊什么"，只需要看到"completed 的读完做决策、blocked 的判断是重试还是收口、launched 的检查活跃度"。所有 Worker 的产出最终汇入 handoffs 表，Manager 按 raw_key 线程逐个处理。

**会话何时结束：** Worker 会话在 worktree 被 close（合并到 develop 或废弃删除）时结束。Manager 调用 `wt-close`，Runtime 关闭 Worker 进程和 ACP 会话。Worker 不是自己"做完就关"——它做完汇报后会话保持，等待 Manager 确认收口或追加指令。Manager 是唯一有权结束 Worker 会话的角色。

## Manager 的信息双通道：handoffs + scan

Manager 有两个信息源，职责不同——

**handoffs 表（监督通道）**：告诉 Manager"已经委派了什么、进展如何"。每轮 patrol 必查：completed 的需要消费决策、blocked 的需要判断重试或收口、launched 的需要检查活跃度、pending 的可能是崩溃残留。

**scan（发现通道）**：告诉 Manager"项目里还有什么没做的"。扫描 issue 生命周期（raw→I→B1→B2→merge），但**排除已有活跃 Worker 的条目**。过滤逻辑：

1. scan 条目有 `worktree_path` → 用 worktree 路径查 handoffs：`WHERE worktree=? AND role='worker' AND status='launched'`。worktree 路径本身就包含 raw_key，且 `idx_handoffs_worktree_status` 索引保证记录多也不慢。
2. scan 条目无 worktree（如 chat 条目尚未创建工位）→ 用 `raw_key` 查：`WHERE raw_key=? AND role='worker' AND status='launched'`。

任一命中 → 该条目被排除。Manager 拿到的 scan 已经是过滤后的，不需要自己交叉验证。

**Worker 一旦不活跃，缺口就重新出现**：Worker 完成（completed）、受阻（blocked）、被拒（rejected）、或会话死亡后——handoffs 表不再有 `status=launched` 的记录，该 issue 对应的条目在下一轮 scan 中重新浮出。Manager 看到它时，需要结合 handoffs 线程历史判断：是继续推进（followthrough）、收口关闭、还是重新委派。

**时序门控**：当有活跃 Worker 时，Runtime 跳过 scan 注入——Manager 应该先专注监督已有 Worker，处理完它们的汇报再找新任务。没有活跃 Worker 时才注入 scan，此时 scan 结果必然全是"尚无 Worker 在跑"的条目。

## 可视化参考

| 图 | 内容 |
|----|------|
| [handoff-architecture.svg](handoff-architecture.svg) | 整体架构与数据流：Agent Docs → AI → Runtime → DB → Worker Launch 五层结构 |
| [handoff-state-machine.svg](handoff-state-machine.svg) | 完整状态机：6 个 status 值、10 个合法转换、每个的触发条件与守卫 |
| [handoff-sequence.svg](handoff-sequence.svg) | 完整时序泳道图：Manager AI / Runtime / Worker AI / DB / Prompt File 五泳道，25 个标注步骤 |
| [handoff-thread-model.svg](handoff-thread-model.svg) | 线程模型：3 轮 Manager-Worker 对话中 raw_key / parent_handoff_id / previous_worker_handoff_id 的关联关系 |

## 数据库重建

handoffs 表是 manager 和 worker 的唯一共享交接媒介。当前已投入使用（manager 125 条、worker 301 条），但在字段语义上存在冗余——5 个原因字段语义完全重叠。重构后削为 1 个 `reason`，同时启用 `consumed` 状态。

### 新表

直接更新 `handoff.py` 的 `init_db()` 中的建表语句（本地数据删除重建，未对外发布）：

```sql
CREATE TABLE handoffs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  handoff_id TEXT NOT NULL UNIQUE,
  role TEXT NOT NULL CHECK(role IN ('manager','worker')),
  raw_key TEXT NOT NULL,
  worktree TEXT DEFAULT '',
  branch TEXT DEFAULT '',
  prompt_file TEXT NOT NULL,
  parent_handoff_id TEXT DEFAULT '',
  previous_worker_handoff_id TEXT DEFAULT '',
  intent_kind TEXT DEFAULT '',
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK(status IN ('pending','launched','completed','rejected','blocked','consumed')),
  exit_kind TEXT DEFAULT '',
  reason TEXT DEFAULT '',
  restart_point TEXT DEFAULT '',
  next_action TEXT DEFAULT '',
  completion_summary TEXT DEFAULT '',
  evidence_paths TEXT DEFAULT '',
  worker_prompts_csv TEXT DEFAULT '',
  session_id TEXT DEFAULT '',
  created_by TEXT DEFAULT '',
  consumed_by TEXT DEFAULT '',
  launched_at TEXT DEFAULT '',
  last_activity_at TEXT DEFAULT '',
  completed_at TEXT DEFAULT '',
  created_at TEXT NOT NULL DEFAULT '',
  updated_at TEXT NOT NULL DEFAULT ''
);

CREATE INDEX idx_handoffs_role_status ON handoffs(role, status);
CREATE INDEX idx_handoffs_raw_key ON handoffs(raw_key);
CREATE INDEX idx_handoffs_worktree ON handoffs(worktree);
CREATE INDEX idx_handoffs_parent ON handoffs(parent_handoff_id);
CREATE INDEX idx_handoffs_prev_worker ON handoffs(previous_worker_handoff_id);
CREATE INDEX idx_handoffs_worktree_status ON handoffs(worktree, status);
```

### 字段变更说明

**删除的字段（5→1）：**

| 旧字段 | 旧含义 | 合并到 |
|--------|--------|--------|
| `stop_reason` | Manager: 为什么停止 | `reason` |
| `why_not_stop` | Manager: 为什么不能停 | `reason` |
| `why_not_delegate` | Manager: 为什么不能委派 | `reason` |
| `blocked_reason` | Worker: 为什么受阻 | `reason` |
| `handoff_reason` | Worker: 为什么请示主管 | `reason` |

`reason` 字段语义：本轮 exit 的原因说明。不同角色/场景填不同内容——看 JSON 输出格式章节的表格。

**新增的 status 值：**

`consumed` — 记录已被消费（manager 读了 worker 的完成并做了后续决策）。配合已有的 `consumed_by` 字段。

**其他保留的字段：**

`restart_point` 和 `next_action` 语义不同不做合并——前者给 Runtime 指明续接阶段（pre_brainstorm / IBM / dev / verification / recovery / cleanup），后者给对端 Agent 指明建议动作（delegate / freeze / merge / cleanup）。

### 线程模型 (图: [handoff-thread-model.svg](handoff-thread-model.svg))

**不新增 `thread_id` 字段。`raw_key` 就是线程分组键。**

一个 raw issue = 一个 manager-worker 对话线程。同一 raw_key 下的所有 manager/worker 记录构成该线程的完整历史。`idx_handoffs_raw_key` 已支持按线程查询。

同一 raw_key 内的并行委派（同一 `delegate_workers` 批次多个 worker）共享同一个 `parent_handoff_id`，已可区分批次归属。

**`previous_worker_handoff_id`：串联同线程的多轮 worker**

同一线程内，当 manager 对同一个 worktree 发起第 N+1 轮交互时（followthrough prompt），`previous_worker_handoff_id` 指向第 N 轮的 worker handoff 记录。Worker 的 ACP 会话持续存在，新 handoff 记录标记新一轮工作。

并行委派场景（同一 delegate_workers 批次多个 worker）：它们共享同一个 `parent_handoff_id`，各自独立完成。下一轮 worker 的 `previous_worker_handoff_id` 取最近一条 completed worker。多个并行 worker 的整合由 Manager 负责——Manager 在下一轮 prompt 的 Task 中综合前序产出。

`previous_worker_handoff_id` 由 Runtime 在 `consume_delegate_workers` 中自动填充：查询同 `raw_key` 下最近一条 `role=worker AND status=completed` 的记录，将其 `handoff_id` 写入。无前序 worker 则为 `""`。

## JSON 输出格式

AI 不再执行 `handoff.py update` / `handoff.py insert` 直接写数据库。改为在回复末尾输出纯 JSON，由 Runtime 解析后统一写入。

**AI 只输出它负责的 7 个字段。** Runtime 管理的字段（handoff_id、role、raw_key、worktree、branch、prompt_file、parent_handoff_id、previous_worker_handoff_id、intent_kind、status、session_id、created_by、consumed_by、launched_at、completed_at、created_at、updated_at）不在 JSON 中输出——Runtime 解析后自动填充。

AI 不会填的字段直接省略——不存在的键 = Runtime 填默认值 `""`。

### Manager 交接 JSON (`freely-agent-manager.md`)

| 字段 | delegate_workers | resume_manager | stop_ai |
|------|-----------------|----------------|---------|
| exit_kind | `"delegate_workers"` | `"resume_manager"` | `"stop_ai"` |
| reason | 为什么委派这些 worker。例: `"issue #344 需要实现 agent handoff protocol"` | 为什么不能停也不能委派。例: `"等待3个worker完成，2个已完成1个仍在执行中"` | 为什么停止。例: `"舰队无待推进项，所有 issue 已收口"` |
| worker_prompts_csv | prompt 文件绝对路径，逗号分隔。例: `"/abs/path/w1.txt,/abs/path/w2.txt"` | 省略 | 省略 |
| restart_point | 省略 | 下次重入起点。`"pre_brainstorm"` / `"IBM"` / `"dev"` / `"verification"` / `"recovery"` / `"cleanup"` | 省略 |
| next_action | 省略 | 建议下一步。例: `"等worker完成后判断是否收口"` | 省略 |
| completion_summary | 省略 | 省略 | 省略 |
| evidence_paths | 省略 | 省略 | 省略 |

### Worker 交接 JSON (`freely-agent-worker.md`)

| 字段 | worker_done | worker_handoff_needed | worker_blocked |
|------|------------|---------------------|----------------|
| exit_kind | `"worker_done"` | `"worker_handoff_needed"` | `"worker_blocked"` |
| reason | 省略 | 为什么需要主管决策。例: `"方案A与模块X冲突，需要主管决定是否改用方案B"` | 为什么受阻。例: `"worktree权限不足，无法写入 .freely/run/ 目录"` |
| completion_summary | 具体完成了什么。例: `"修改 handoff.py 新增 reason 字段，删除5个旧字段，通过现有测试"` | 省略 | 省略 |
| evidence_paths | 证据文件，逗号分隔。例: `"/abs/path/test-output.log"` | 省略 | 省略 |
| next_action | 省略 | 建议主管做什么。例: `"确认是否改用方案B，或提供替代方案"` | 建议主管做什么。例: `"检查 worktree 权限配置"` |
| worker_prompts_csv | 省略 | 省略 | 省略 |
| restart_point | 省略 | 省略 | 省略 |

### JSON 完整示例

Manager 委派:

```handoff
{
  "exit_kind": "delegate_workers",
  "reason": "issue #344 需要创建预研工位并完成B1_IBM",
  "worker_prompts_csv": "/path/to/.freely/run/worker-prompts/w1.txt"
}
```

Worker 完成:

```handoff
{
  "exit_kind": "worker_done",
  "completion_summary": "修改 handoff.py 新增 reason 字段，删除5个旧字段，通过现有测试",
  "evidence_paths": "/abs/path/test-output.log"
}
```

### Runtime 端解析与合并

```python
def parse_handoff_json(ai_reply, context):
    """从 AI 回复中提取 handoff JSON，验证，合并 Runtime 字段后写入。"""
    block = extract_fenced_block(ai_reply, "handoff")
    ai_fields = json.loads(block)
    validate(ai_fields)  # 按 exit_kind 检查必填字段

    # Runtime 填充
    record = {
        "handoff_id": generate_id(),
        "role": context.role,
        "raw_key": context.raw_key,
        "worktree": context.worktree,
        "branch": context.branch,
        "prompt_file": context.prompt_file,
        "parent_handoff_id": context.parent_handoff_id,
        "previous_worker_handoff_id": context.previous_worker_handoff_id,
        "intent_kind": context.intent_kind,
        "status": "pending",
        "session_id": context.session_id,
        "created_by": "runtime",
        "consumed_by": "",
        "launched_at": "",
        "completed_at": "",
        "created_at": now_utc(),
        "updated_at": now_utc(),
        # AI 字段覆盖
        **ai_fields
    }
    insert(record)
    dispatch_consume(record)
```

## Runtime 消费 (图: [handoff-sequence.svg](handoff-sequence.svg))

Runtime 解析 ` ```handoff ` 块 → `json.loads()` → 按 `exit_kind` 分发给解耦的消费方法。

### parse_handoff_json

```bash
# 从 AI 回复中提取 handoff JSON
# 输入: AI 回复文本
# 输出: 验证后的 JSON → 分发消费 / 不达标 → 插入修复 handoff
```

### consume_delegate_workers(json)

```
1. 读 worker_prompts_csv ← 单一权威源
2. for each prompt_file:
   a. 去重: 同 prompt_file + 同 raw_key + status IN (launched,pending) → 跳过
   b. 解析 worktree / branch / intent_kind from prompt headers
   c. INSERT worker 记录:
      - parent_handoff_id = 当前 manager handoff_id
      - previous_worker_handoff_id = 同 raw_key 最近一条 completed worker 的 handoff_id
      - status = pending
      - created_by = runtime
   d. 判断启动模式:
      - worktree 已有 ACP 会话（session-store.get-active 返回有效 session_id）
        → LAUNCH_KIND_SELECTED="prompt"（delta turn, 同一 Worker 会话继续）
      - worktree 无会话或会话已失效
        → LAUNCH_KIND_SELECTED="fork"（从 Manager 会话继承缓存, 首次或重建）
   e. launch worker → UPDATE status = launched
```

### consume_resume_manager(json)

```
1. UPDATE manager 记录: status = completed
2. 自动消费同 raw_key 下所有未消费的 worker：
   UPDATE handoffs SET status='consumed', consumed_by='manager'
   WHERE raw_key=<当前raw_key> AND role='worker'
   AND status IN ('completed','blocked','rejected') AND consumed_by=''
3. 不创建 worker。原 supervisor loop 继续下轮 patrol。
```

### consume_stop_ai(json)

```
1. UPDATE manager 记录: status = completed
2. 自动消费同 raw_key 下所有未消费的 worker（同 consume_resume_manager 步骤 2）
3. 通知 supervisor 退出。
```

### consume_worker_done(json)

```
1. UPDATE worker 记录: status = completed
2. 不自动标记 consumed。等待 manager 下一条 handoff 创建时自动消费。
```

### consume_worker_handoff_needed(json)

```
1. UPDATE worker 记录: status = completed（Worker 会话保持活跃，不关闭）
2. Runtime 生成 followthrough prompt：从 worker 的 reason/next_action 提取上下文
3. 不自动标记 consumed。Manager 下轮 patrol 看到 handoff_needed → 以 delta turn（prompt）向同一 Worker 会话发送 followthrough → 新 handoff 创建时自动消费本轮记录。
```

### consume_worker_blocked(json)

```
1. UPDATE worker 记录: status = blocked
2. 不自动标记 consumed。等待 manager 决策后自动消费。
```

### 消费时自动推进 consumed

**统一的消费触发规则：** 当 Runtime 为 manager 创建新的 handoff 记录时（无论是 delegate_workers、resume_manager 还是 stop_ai），自动将当前 raw_key 下所有 `status IN ('completed','blocked','rejected') AND consumed_by=''` 的 worker 记录标记为 `status='consumed', consumed_by='manager'`。

manager 新 handoff 创建时，当前 raw_key 下尚未 launch 的 worker 还不存在（正在 INSERT），已存在的 completed/blocked/rejected worker 必然是上一轮遗留的。时序天然正确：创建新 → 消费旧。

如果 Runtime 崩溃在 INSERT manager 和 INSERT worker 之间：manager 记录已写入（含 worker_prompts_csv），Manager 下轮 patrol 读出 → 对比 handoffs 表发现 workers 缺失 → 重新创建。不丢数据。

## 验证与修复闭环

Runtime 消费 JSON 前先验证字段完整性。验证是兜底——主路径是 AI 按 agent doc 表格产出达标 JSON。

### 验证规则

| 检查项 | 不达标时 |
|--------|---------|
| ` ```handoff ` 块缺失或 parse 失败 | 插入修复 handoff |
| `exit_kind` 不是 6 个合法值之一 | 插入修复 handoff |
| delegate_workers 缺少 `worker_prompts_csv` 或字段为 `""` | 插入修复 handoff |
| `worker_prompts_csv` 中的路径不存在 | 插入修复 handoff |
| resume_manager 缺少 `restart_point` 或 `next_action` | 插入修复 handoff |
| worker_done 缺少 `completion_summary` | 插入修复 handoff |
| worker_blocked 缺少 `reason` 或 `next_action` | 插入修复 handoff |
| worker_handoff_needed 缺少 `reason` 或 `next_action` | 插入修复 handoff |

AI 省略的字段（non-required for that exit_kind）默认为 `""`，不触发验证失败。

### 修复 handoff

Runtime 验证失败 → 插入一条 `role=manager` 的修复 handoff 记录，携带结构化字段：

```
exit_kind=resume_manager
restart_point=recovery
repair_target_role: "manager" | "worker"  ← 谁产出了不合格的 JSON
repair_target_handoff_id: <hid>  ← 出问题的 handoff 记录
validation_errors_json: [{"field":"worker_prompts_csv","error":"required for delegate_workers"}]  ← 具体哪些字段不达标
reason: 自动生成，简述验证失败原因
next_action: 自动生成，根据 repair_target_role 给出操作指引
```

修复 handoff 是一条普通 handoff 记录，走统一的 Manager patrol 消费路径。Manager 看到结构化字段后：
- `repair_target_role=worker`：检查对应 worker 的 prompt 是否完整，agent doc 的 JSON 说明是否清晰，然后以 delta turn 向同一 Worker 会话发送修正指令（Worker 会话持续存在，不重建）
- `repair_target_role=manager`：知道自己上一轮输出的 JSON 格式有问题，按 validation_errors_json 修正后重新输出

改进点：原文的修复 handoff 用自然语言描述错误（"请找到该角色，告诉它..."），Manager 需要从散文里推断信息。现在改为结构化字段——`repair_target_role`、`repair_target_handoff_id`、`validation_errors_json`——Manager 直接读取字段值即可定位问题，不需要推断。

## 字段所有权

| 字段 | 写入者 | 说明 |
|------|--------|------|
| `handoff_id` | Runtime | insert 时自动生成 |
| `role` | Runtime | manager / worker |
| `raw_key` | Runtime | 从 prompt file 或当前上下文提取 |
| `worktree` | Runtime | worker: 从 prompt headers 解析 |
| `branch` | Runtime | worker: 从 prompt headers 解析 |
| `prompt_file` | Runtime | 当前 prompt 文件路径 |
| `parent_handoff_id` | Runtime | 触发本记录的父记录 |
| `previous_worker_handoff_id` | Runtime | 同线程上一轮 worker 的 handoff_id |
| `intent_kind` | Runtime | worker: 从 prompt headers 解析 |
| `status` | Runtime | 状态机全程由 runtime 驱动 |
| `exit_kind` | **AI** | 6 种合法值 |
| `reason` | **AI** | 本轮 exit 原因 |
| `restart_point` | **AI** | resume_manager 必填 |
| `next_action` | **AI** | resume_manager / worker_blocked / worker_handoff_needed 必填 |
| `completion_summary` | **AI** | worker_done 必填 |
| `evidence_paths` | **AI** | worker_done 可选 |
| `worker_prompts_csv` | **AI** | delegate_workers 必填 |
| `session_id` | Runtime | ACP session ID |
| `created_by` | Runtime | 谁创建 |
| `consumed_by` | Runtime | 谁消费（自动标记） |
| `launched_at` | Runtime | worker 启动时 |
| `last_activity_at` | Runtime | worker 最近一次可观测活跃时间（log mtime / socket heartbeat / PID 存活），用于不活跃检测而非总运行时长判断 |
| `completed_at` | Runtime | completed/blocked/rejected/consumed 时 |
| `created_at` | Runtime | insert 时 |
| `updated_at` | Runtime | 每次 update 时 |

## 状态机 (图: [handoff-state-machine.svg](handoff-state-machine.svg))

### Worker 状态转换

```
                    ┌──────────┐
                    │ pending  │
                    └────┬─────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         ┌────────┐ ┌──────────┐ ┌──────────┐
         │launched│ │ rejected │ │ consumed │ (直接消费：工位不存在等)
         └───┬──┬─┘ └────┬─────┘ └──────────┘
             │  │        │
        ┌────┘  │        │
        ▼       ▼        │
   ┌─────────┐ ┌──────┐  │
   │completed│ │blocked│  │
   └────┬────┘ └──┬───┘  │
        │         │      │
        └────┬────┘      │
             │           │
             ▼           ▼
        ┌──────────┐
        │ consumed │
        └──────────┘
```

### Manager 状态转换

```
  pending ──→ completed
```

### 合法转换表

| 当前状态 | 合法目标状态 | 触发条件 |
|---------|-------------|---------|
| `pending` | `launched` | worker 启动成功 |
| `pending` | `rejected` | launch 失败 / worktree 不存在 |
| `pending` | `consumed` | worker 记录已无意义（工位已删、issue 已关等） |
| `launched` | `completed` | worker_done / worker_handoff_needed |
| `launched` | `blocked` | worker_blocked / 不活跃超时 (mark_stale: last_activity_at 超过阈值) |
| `launched` | `rejected` | pid 检查发现死进程 |
| `completed` | `consumed` | manager 创建新 handoff → 自动消费 |
| `blocked` | `consumed` | manager 创建新 handoff → 自动消费 |
| `rejected` | `consumed` | manager 创建新 handoff → 自动消费 |

### 守卫条件

- `pending → launched` 仅当 worktree 存在且 worker prompt 可读取
- `pending → rejected` 仅当 worktree 不存在或 launch 失败
- `launched → completed` 仅当 worker AI 正常退出
- `launched → blocked` 仅当 worker AI 明确受阻（worker_blocked JSON），或 `last_activity_at` 超过不活跃阈值（Runtime 无法检测到任何活跃信号：log 不更新、PID 不响应、socket 无心跳）。Worker 持续慢但 log 在更新 → 不触发，AI 慢是可接受的
- `→ consumed` 是终态。consumed 不可再转换为任何其他状态
- manager 记录只有 `pending → completed`，不需要 consumed（manager 不被他者消费）

### 乐观锁（状态更新竞态防御）

`consume_worker_done` 和 `mark_stale` 可能对同一条 launched 记录并发执行。所有 Runtime 执行的状态 UPDATE 必须加 `WHERE status='<期望的当前状态>'` 条件，并检查 affected rows：

```sql
-- consume_worker_done: 只有 launched 状态的 worker 才能标记为 completed
UPDATE handoffs SET status='completed', completion_summary=?, evidence_paths=?, updated_at=?
WHERE handoff_id=? AND status='launched'

-- mark_stale: launched 但 last_activity_at 超过不活跃阈值（不是总运行时长）才标记为 blocked
-- Runtime 在每次检测到 Worker 活跃（log 更新/PID 存活/socket 心跳）时更新 last_activity_at
UPDATE handoffs SET status='blocked', exit_kind='worker_blocked',
  reason='Worker 不活跃超过阈值: last_activity_at=' || last_activity_at, updated_at=?
WHERE role='worker' AND status='launched' AND last_activity_at < ?

-- auto-consume: 只有非 consumed 终态的 worker 才能消费
UPDATE handoffs SET status='consumed', consumed_by='manager', updated_at=?
WHERE raw_key=? AND role='worker'
AND status IN ('completed','blocked','rejected') AND consumed_by=''
```

两个并发操作中只有第一个到达的会成功（affected_rows=1），第二个 affected_rows=0 → 记录 warning 日志但不报错。所有状态变更都有明确的当前状态前提——"completed" 不会凭空变成 "blocked"。

## 与 #343 的关系

#343 的根因是 AI 直接执行 `handoff.py update`/`handoff.py insert` 写数据库，validator 读 `worker_prompts_csv`、launcher 读 `pending worker`——两个读者读 AI 分步产出的两个独立数据源。

本设计下：

- **单一数据源**：AI 输出一个 JSON。Runtime 做唯一一次解析写入。不存在"Step B 做了 Step C 没做"的可能性。
- **launcher 和 validator 合一**：`consume_delegate_workers` 自己读 `worker_prompts_csv`、自己验证字段、自己 insert worker 记录、自己 launch。全在一个函数里，不存在读错字段的问题。
- **worktree_has_active_worker 不会误伤 pending**：消费方法创建 worker 记录时传 `status=pending`，去重检查只查 `launched`。
- **结构字段不会漏**：`worktree`/`branch`/`parent_handoff_id` 由 Runtime 统一填充，不是 AI 逐条 insert 时可能遗漏的参数。

#343 四个 bug 在新协议下不是"修好了"——是**结构上不存在了**。

## 实现路径

| 文件 | 改动 |
|------|------|
| `handoff.py` | 旧表 DROP，新表 CREATE。`reason` 替代 5 个旧字段，新增 `previous_worker_handoff_id`、`last_activity_at`。`status` CHECK 增加 `consumed`。所有 UPDATE 加 `WHERE status='<期望当前状态>'` 乐观锁。`mark_stale` 改为检查 `last_activity_at`。新增 `handoff.py parse` 子命令。 |
| `freely-agent-manager.md` | 替换旧"交接"章节为新"交接 JSON"章节：3 列表格，AI 只输出它负责的字段 |
| `freely-agent-worker.md` | 替换旧"交接"章节为新"交接 JSON"章节：3 列表格，AI 只输出它负责的字段 |
| `freely` — `build_prompt` | Manager 注入：线程历史（同 raw_key 最近 10 条摘要）+ 未消费 worker 列表 + fleet/scan。Worker 注入：仅 Task + agent doc + WORKER_HANDOFF_INJECT。删除旧 `handoff.py update` CLI 指令。 |
| `freely` — `WORKER_HANDOFF_INJECT` | 仅在 fork（首次启动或会话重建）时注入：handoff_id + parent_handoff_id + previous_worker_handoff_id + 上一轮 completion_summary（截断 80 字）。delta turn 不注入——会话已有上下文。 |
| `freely` — exit contract handler | 替换为 `parse_handoff_json` + `consume_*` 方法 + 乐观锁 WHERE 子句。auto-consume 在 manager 新 handoff 创建时自动触发。修复 handoff 携带 `repair_target_role` + `repair_target_handoff_id` + `validation_errors_json` 结构化字段。 |
| `freely` — `worktree_has_active_worker` | 只查 `status=launched`；检测到活跃信号时 UPDATE `last_activity_at` |

## 上下文注入策略（Manager vs Worker 职责分离）

Manager 和 Worker 的职责不同，注入的上下文也应不同。Manager 需要全局视野做编排决策，Worker 只需知道自己的任务和前序产出。

### Manager Prompt 注入（全量上下文）

```
build_prompt() 为 Manager 注入:
  1. manager-agent.md（角色定义 + JSON 输出规范表格）
  2. 线程历史：同 raw_key 最近 10 条 handoff 记录摘要
     - 每条摘要: handoff_id, role, exit_kind, reason(截断50字), status, created_at
     - Manager 需要全线程视野来做 patrol 决策
  3. 未消费 worker 列表: handoff_id, exit_kind, completion_summary, reason, next_action
  4. 当前 fleet 状态 + scan 数据
  5. Manager exit contract directive（JSON 输出格式 + 3 种 exit_kind 表格）
```

### Worker Prompt 注入（区分 fork 与 delta）

**fork（首次启动或会话重建）：**

```
build_prompt() 为 Worker 注入:
  1. worker-agent.md（角色定义 + JSON 输出规范表格）
  2. Task 内容（从 prompt 文件读取）
  3. WORKER_HANDOFF_INJECT（结构化字段注入）:
     - handoff_id: <自己的>
     - parent_handoff_id: <Manager 委派记录，含 reason 字段>
     - previous_worker_handoff_id: <上一轮 completion_summary（截断 80 字）>
     // 不注入: 完整线程历史、同 raw_key 最近 N 条摘要
```

**delta turn（同一 Worker 会话继续，followthrough/纠正/澄清）：**

```
Runtime 只发送 followthrough prompt 内容（Manager 在 handoff 里写的 next_action/reason）。
Worker 的 ACP 会话已记住 agent doc + Task + 历史对话，不需重新注入。
```

**Token 预算对比：**

| | Manager | Worker |
|--|---------|--------|
| Agent doc | ~800 tokens | ~500 tokens |
| 线程历史 | ~500 tokens (10 条摘要) | 0 |
| 前序 Worker 上下文 | 0 (从 handoffs 表查) | ~200 tokens |
| Fleet/Scan | ~2000 tokens | 0 |
| Task | 0 | ~1000 tokens |
| **合计** | ~3500 tokens | ~1800 tokens |

Worker 不读线程历史、不读 fleet、不读 scan——只读自己的 Task + 前序 Worker 的产出摘要。Worker 不需要理解全局态势来做决策，它只执行 Manager 分配的一个原子任务。

1. **JSON 块格式**：` ```handoff `。不与普通 ` ```json ` 代码块混淆，grep 精准提取。编辑器高亮不是问题——块内容就是合法 JSON。

2. **AI 只输出 7 个字段**。Runtime 管理的 17 个字段不在 JSON 中输出。AI 不需要看到完整 schema——agent doc 里的表格已告诉它每个场景该填什么字段。省略字段 = Runtime 填默认值，不会遗漏。

3. **`consumed` 迁移**：不需要。应用未发布，DB 直接 DROP 旧表 → CREATE 新表。旧数据不迁移。
