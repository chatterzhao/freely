# Brainstorm: Agent Handoff Protocol

- 来源: raw-20260514T103532Z (#344)
- 日期: 2026-05-14
- 基于: #343 handoff pipeline disconnect 根因分析、handoffs 表实际使用情况审视

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
  completed_at TEXT DEFAULT '',
  created_at TEXT NOT NULL DEFAULT '',
  updated_at TEXT NOT NULL DEFAULT ''
);

CREATE INDEX idx_handoffs_role_status ON handoffs(role, status);
CREATE INDEX idx_handoffs_raw_key ON handoffs(raw_key);
CREATE INDEX idx_handoffs_worktree ON handoffs(worktree);
CREATE INDEX idx_handoffs_parent ON handoffs(parent_handoff_id);
CREATE INDEX idx_handoffs_prev_worker ON handoffs(previous_worker_handoff_id);
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

### 线程模型

**不新增 `thread_id` 字段。`raw_key` 就是线程分组键。**

一个 raw issue = 一个 manager-worker 对话线程。同一 raw_key 下的所有 manager/worker 记录构成该线程的完整历史。`idx_handoffs_raw_key` 已支持按线程查询。

同一 raw_key 内的并行委派（同一 `delegate_workers` 批次多个 worker）共享同一个 `parent_handoff_id`，已可区分批次归属。

**`previous_worker_handoff_id`：串联同线程的多轮 worker**

同一线程内，当 manager 创建第 N+1 个 worker 时，`previous_worker_handoff_id` 指向第 N 个 worker 的 `handoff_id`。新 worker 的 WORKER_HANDOFF_INJECT 注入上一轮 worker 的 `completion_summary` + `evidence_paths`，使后续 worker 了解前序工作的产出。

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

## Runtime 消费

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
      - status = pending
      - created_by = runtime
   d. launch worker → UPDATE status = launched
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
1. UPDATE worker 记录: status = completed
2. 不自动标记 consumed。manager 下轮 patrol 看到 → 决策 → 创建新 handoff → 自动消费。
```

### consume_worker_blocked(json)

```
1. UPDATE worker 记录: status = blocked
2. 不自动标记 consumed。等待 manager 决策后自动消费。
```

### 消费时自动推进 consumed

**统一的消费触发规则：** 当 Runtime 为 manager 创建新的 handoff 记录时（无论是 delegate_workers、resume_manager 还是 stop_ai），自动将当前 raw_key 下所有 `status IN ('completed','blocked','rejected') AND consumed_by=''` 的 worker 记录标记为 `status='consumed', consumed_by='manager'`。

这意味着：manager 的每一次 patrol → exit → 新 handoff 创建动作，自动"签收"了上一轮所有未消费的 worker 产出。不依赖 AI 逐条标记 consumed。

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

Runtime 插入一条 `role=manager` 的 handoff 记录（Reason + Next Action 直接写在 `reason` 和 `next_action` 中，Manager 下轮 patrol 自然消费）:

```
exit_kind=resume_manager
reason=上一轮 [manager/worker] 的 handoff JSON 不达标: [具体字段]。请定位该角色，要求其根据 agent doc 表格重新生成。
restart_point=recovery
next_action=定位产出不合格 JSON 的角色，按对应场景表格补全字段后重新输出
```

Manager 下轮 patrol 消费这条修复 handoff → 定位问题角色 → 重新拉起该角色 → 角色带着 repair context 重新判断场景、按表格规范重新产出 JSON。

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
| `completed_at` | Runtime | completed/blocked/rejected/consumed 时 |
| `created_at` | Runtime | insert 时 |
| `updated_at` | Runtime | 每次 update 时 |

## 状态机

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
| `launched` | `blocked` | worker_blocked / stale timeout (mark_stale) |
| `launched` | `rejected` | pid 检查发现死进程 |
| `completed` | `consumed` | manager 创建新 handoff → 自动消费 |
| `blocked` | `consumed` | manager 创建新 handoff → 自动消费 |
| `rejected` | `consumed` | manager 创建新 handoff → 自动消费 |

### 守卫条件

- `pending → launched` 仅当 worktree 存在且 worker prompt 可读取
- `pending → rejected` 仅当 worktree 不存在或 launch 失败
- `launched → completed` 仅当 worker AI 正常退出
- `launched → blocked` 仅当 worker AI 受阻或超时
- `→ consumed` 是终态。consumed 不可再转换为任何其他状态
- manager 记录只有 `pending → completed`，不需要 consumed（manager 不被他者消费）

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
| `handoff.py` | 旧表 DROP，新表 CREATE。`reason` 替代 5 个旧字段，新增 `previous_worker_handoff_id`。`status` CHECK 增加 `consumed`。新增 `handoff.py parse` 子命令（提取 ` ```handoff ` 块，验证，合并 Runtime 字段，dispatch consume_*）。 |
| `freely-agent-manager.md` | 替换旧"交接"章节为新"交接 JSON"章节：3 列表格（delegate_workers / resume_manager / stop_ai），AI 只输出它负责的字段，省略 = Runtime 填默认值 |
| `freely-agent-worker.md` | 替换旧"交接"章节为新"交接 JSON"章节：3 列表格（worker_done / worker_handoff_needed / worker_blocked），AI 只输出它负责的字段 |
| `freely` — `build_prompt` | 注入当前 handoff 上下文：线程历史（同 raw_key 最近 5 条记录摘要）、上一轮 worker 的 completion_summary + evidence_paths（如有 `previous_worker_handoff_id`）、未消费 worker 列表。删除 `append_*_exit_contract_directive_if_needed` 中的 `handoff.py update` 指令，替换为 JSON 输出指令。 |
| `freely` — `WORKER_HANDOFF_INJECT` | 注入 handoff_id + parent_handoff_id + previous_worker_handoff_id + 上一轮 worker 的 completion_summary。不再注入 `handoff.py update` bash 命令——worker 改输出 JSON。 |
| `freely` — exit contract handler | 替换为 `parse_handoff_json` + `consume_*` 方法。移除 `validate_manager_exit_contract_for_project` 对旧字段的检查。所有 `consume_*` 方法统一在创建新 manager handoff 时自动消费 unconsumed worker。 |
| `freely` — `worktree_has_active_worker` | 只查 `status=launched` |

## 设计决策记录

1. **JSON 块格式**：` ```handoff `。不与普通 ` ```json ` 代码块混淆，grep 精准提取。编辑器高亮不是问题——块内容就是合法 JSON。

2. **AI 只输出 7 个字段**。Runtime 管理的 17 个字段不在 JSON 中输出。AI 不需要看到完整 schema——agent doc 里的表格已告诉它每个场景该填什么字段。省略字段 = Runtime 填默认值，不会遗漏。

3. **`consumed` 迁移**：不需要。应用未发布，DB 直接 DROP 旧表 → CREATE 新表。旧数据不迁移。
