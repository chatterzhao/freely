---
b1_id: B1-20260719T071858Z
phase_state: completed
source_raw: raw-20260719T071858Z
source_url: https://github.com/chatterzhao/freely/issues/4003
produced_candidate: C-20260719T071858Z-A
created_at: '2026-07-19'
---

# B1_IBM: Manager a2a-exit prompt 模板缺 --role worker 致 worker task 全部错误创建

## Input

- raw issue: raw-20260719T071858Z
- 症状: daemon running, Manager AI cycles normally, but workers never launch — agent_dead
- 发现方式: 重启 freely daemon，观察真实运行 → 分析 A2A DB、runtime-events、lifecycle-trace → 逐段追踪完整链路

## Problem

### 证据链（全部来自实际观察，非猜测）

**证据 1: A2A DB 中本轮 task 的 agent_id 是 manager**

```
sqlite3 .freely/freely.db "SELECT task_id, agent_id, state, raw_key, substr(message,1,60)
FROM a2a_tasks WHERE agent_id='manager' AND state='submitted' ORDER BY created_at DESC LIMIT 3"

→ 63cbeda4 | manager | submitted | 20260719T070107Z | "# Worker: Fix merged_develop phase_state..."
→ 70a6d3aa | manager | submitted | 20260719T070409Z | "# Worker: Fix I-* non-terminal phase_state..."
```

这两个 task 的 message 明确是 Worker 内容（"# Worker: Fix..."），但 agent_id=manager。

**证据 2: Runtime 找不到 worker task**

`runtime-events.log`:
```
event=manager_exit_contract_delegate_workers worker_prompts_csv=none
```

**证据 3: Worker bridge 从未启动**

```
循环日志中无 [bridge] starting: base_tool=opencode 或 base_tool=cline
/tmp/ 下只有 claude bridge 的 pid/sock，无 opencode bridge
```

**证据 4: lifecycle-trace 显示 Worker 委派后直接回到下一轮**

```
L042 → ai_cycle_finished → exit_reason=manager_worker_launch_after_ai_cycle
→ 立刻回到 L020 → prompt_build_begin（下一轮 Manager patrol）
中间无 worker bridge 启动
```

### 代码层根因追踪

**追踪 1: Manager prompt 模板**（`freely` L15528-15536）：

```bash
python3 docs/system/workspace/scripts/runtime/a2a_task.py a2a-exit \
  --state submitted|completed|failed \
  --summary "本轮做了什么" \
  --workers "worker-prompt.csv路径（委派时填写）" \
  --next "下一步建议"
```

模板里**没有 `--role worker`**。

**追踪 2: a2a_task.py 默认值**（L830）：

```python
p_exit.add_argument("--role", default="manager", help="Role: manager|worker")
```

`--role` 默认值是 `manager`。Manager AI 按模板调用 → agent_id 永远是 `manager`。

**追踪 3: Runtime 查询条件**：

Runtime 用 `list --role worker --status submitted` 查询 → A2A Server 的 SQL 是 `WHERE agent_id = 'worker' AND state = 'submitted'`。agent_id=manager 的 task 永远查不到。

### 完整故障链

```
1. Manager AI 按 prompt 模板调用 a2a-exit
   a2a-exit --state submitted --summary "Fix: ..."
   ↑ 模板缺 --role worker, --role 默认 manager

2. a2a_task.py: agent_id=manager
   A2A DB: INSERT INTO a2a_tasks (agent_id, ...) VALUES ('manager', ...)

3. Runtime: list --role worker --status submitted
   SELECT * FROM a2a_tasks WHERE agent_id = 'worker' AND state = 'submitted'
   → 0 results (agent_id=manager 不匹配)

4. worker_prompts_csv=none → worker bridge 不启动 → agent_dead

5. Manager 下一轮 patrol 看到 agent_dead → 创建 raw issue "worker launch verification blocked"
   → 形成自我延续的诊断循环：Manager 每次 patrol 都诊断"worker 无法启动"，
   但不知道根因是自己创建 task 时 agent_id 错了
```

## Brainstorm

### 为什么之前没发现

Manager prompt 模板在 `_manager_exit_contract_instructions()` 函数中，这个函数和相关模板引用 `--role worker` 的指令分散在多处（agent 文档、three-loop 文档），但模板本身的命令示例就是没有。AI 按示例调用，不会凭空加参数。

### Option A: 只在 prompt 模板加 --role worker

修改 L15528-15536，在模板和示例中显式加上 `--role worker`。

- 优点: 最小改动，直接解除阻塞
- 风险: 如果未来有其他调用方（reviewer dispatch 等）也需要指定 role，同样会踩坑

### Option B: 模板 + a2a_task.py --role 改为 required

把 `default="manager"` 改为 `required=True`（或移除默认值），强制所有调用方显式指定 role。

- 优点: 从协议层消除静默误用的可能
- 风险: 需检查所有现有 `a2a-exit` 调用方（Manager prompt、Manager 直接调用、Reviewer dispatch、Worker exit 等）是否都已正确传 `--role`

### 检查现有调用方

搜索全仓所有 `a2a-exit` 调用：
- Manager prompt 模板 → **此处修复**
- `three-loop-capability-lifecycle.md` L156: `a2a-exit --state submitted --role worker --worktree ...` → ✅ 文档中已有正确示范
- `manager-agent.md` L83: `a2a-exit --state submitted --role worker ...` → ✅ agent 文档中已有正确示范
- Worker 退出时: `a2a-exit --state completed` → 需确认 Worker 侧是否也受影响

**Worker exit 场景**: Worker 完成后调用 `a2a-exit --state completed`。按当前默认值 → agent_id=manager → task 属于 Manager 而不是 Worker。这也会导致状态更新失败。

### Decision

**采纳 Option B**（模板 + 默认值改为 required）。

理由:
1. `--role` 是 A2A 协议的核心路由字段，role 错了整个 task 就在错误的 agent 名下
2. 当前 `default="manager"` 是危险的 silent failure —— 本应报错的调用静默成功但路由到了错误的目标
3. Worker 侧也受益：Worker 退出时若忘传 `--role worker`，task 同样路由到 manager

需要 fix 的两处:
1. `freely` L15528-15536: prompt 模板加 `--role worker`
2. `a2a_task.py` L830: `--role` 默认值移除（或改为 required）
3. 验证所有现有 `a2a-exit` 调用点都已传 `--role`
