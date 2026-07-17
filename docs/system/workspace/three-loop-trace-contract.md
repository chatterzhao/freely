# Three-Loop Trace Contract

Freely 的主链 trace 不是普通 debug 文本，而是三 loop 执行链的 machine-readable handoff 记录。

目标：
- 让人和 AI 都能低成本看出当前在哪个逻辑点
- 看出当前节点从哪里进来
- 看出当前节点出去后应该交给哪里
- 一旦后继没出现，或实际进入点不符合上游声明，能直接定位断链点

## 1. 适用范围

本合同适用于：
- `auto-loop`
- `doc-loop`
- `dev-loop`

不允许用零散自然语言日志替代主链 trace。

普通运行日志可以继续存在，但主链判断一律看 lifecycle trace。

## 2. 节点命名

每个可判定逻辑节点必须有稳定 checkpoint 编号。

当前 loop 前缀约定：
- `A` = `auto-loop`
- `D` = `doc-loop`
- `V` = `dev-loop`

主链显示 ID 规则：
- auto 侧 `L310` 记为 `A-L310`
- doc 侧 `DOC-120` 记为 `D-DOC-120`
- dev 侧 `DEV-220` 记为 `V-DEV-220`

编号要求：
- 编号稳定，不因日志文案变化而漂移
- 新增节点时，必须同时定义它的上游入口和下游交接
- 如果一个节点可能分支到多个下游，要在不同分支出口分别打印不同的 `OUT to=...`

## 3. 一节点两条主链日志

每个节点至少输出两条主链日志：
- `ph=IN`
- `ph=OUT`

含义：
- `IN` 表示逻辑已进入该节点
- `OUT` 表示该节点本轮执行完成，并声明下一跳应交给谁

这两条日志都属于同一个 `me=` 节点。

## 4. 主字段

主链字段固定顺序如下。

`IN`：
- `seq`
- `ph=IN`
- `me=<current checkpoint>`
- `fr=<upstream checkpoint | ENTRY | UNSET>`
- `ok=<1|0>`，仅当当前节点已知上游声明时打印
- `checkpoint=<raw checkpoint>`
- `stage=<stable stage name>`

`OUT`：
- `seq`
- `ph=OUT`
- `me=<current checkpoint>`
- `to=<actual next checkpoint | TERM | UNSET>`
- `ok=<1|0>`
- `checkpoint=<raw checkpoint>`
- `stage=<stable stage name>`

辅助字段只允许放在主字段之后，例如：
- `intake_id`
- `status`
- `classification`
- `session_id`
- `prompt_file`
- `cycle_log`

## 5. 特殊值

- `ENTRY`: 合法外部入口，没有上游 checkpoint
- `TERM`: 当前链路在这里结束
- `UNSET`: 该节点没有正确声明上游或下游，属于 trace 设计缺口，必须尽快补齐

要求：
- 真正入口只能写 `ENTRY`
- 真正结束只能写 `TERM`
- `UNSET` 不是正常设计，只是显式暴露缺口，避免静默失真

## 6. ok 的判定

`IN` 上的 `ok=`：
- `1`: 实际进入点符合上游节点声明的下一跳
- `0`: 实际进入点不符合上游声明，属于断链或错链

`OUT` 上的 `ok=`：
- `1`: 当前节点已明确写出实际下一跳 `to=`
- `0`: 当前节点没有声明下一跳，属于可观测性缺口

## 7. 断链判定

以下任一情况都可判定为链路异常：
- 某节点只有 `IN` 没有 `OUT`
- 某节点 `OUT to=...` 后，应到的下游长期未出现
- 下游节点 `IN ok=0`
- 节点 `OUT ok=0`，说明没有定义下一跳
- 非入口节点的 `IN fr=UNSET`

因此调试时先看：
1. 最后一个 `OUT`
2. 它声明的 `to=`
3. 目标节点是否出现对应 `IN`
4. 目标节点 `IN ok` 是否为 `1`

## 8. 设计原则

- 主链字段要短，固定顺序，方便 grep 和 AI 解析
- `stage=` 保留简短稳定语义，不能写成长段自然语言
- 业务细节放辅助字段，不污染主链
- 任何新增 loop 节点，都必须同时补：
  - 节点编号
  - `IN`
  - `OUT`
  - 上游 `fr`
  - 下游 `to`
- `to` 的打印权归“真正决定下一跳的那一层”所有；不要让纯 helper 硬凑假的下一跳
- 不需要把所有底层函数都变成 lifecycle 节点。只给真正的逻辑节点 / 路由节点编号，避免日志和参数污染

## 9. 示例

```text
2026-04-17T12:00:00Z seq=101 ph=IN me=A-L300 fr=ENTRY checkpoint=L300 stage=intake_recorded intake_id=i-123
2026-04-17T12:00:00Z seq=102 ph=OUT me=A-L300 to=A-L310 ok=1 checkpoint=L300 stage=intake_recorded intake_id=i-123
2026-04-17T12:00:01Z seq=103 ph=IN me=A-L310 fr=A-L300 ok=1 checkpoint=L310 stage=intake_claimed intake_id=i-123
2026-04-17T12:00:01Z seq=104 ph=OUT me=A-L310 to=A-L330 ok=1 checkpoint=L310 stage=intake_claimed intake_id=i-123
```

如果真实逻辑错进了别的节点，应该出现：

```text
... ph=IN me=A-L320 fr=A-L300 ok=0 ...
```

这表示：
- 实际从 `A-L300` 进入了 `A-L320`
- 但 `A-L300` 声明的下一跳并不接受这个进入

## 10. 维护要求

未来修改三 loop 执行逻辑时：
- 先改逻辑，再同步改 trace 编号和 handoff
- 不允许新增匿名跳转
- 不允许只打进入不打出去
- 不允许只写自然语言”下一步做什么”，而不写 `to=<checkpoint>`

## 11. 已注册的 auto-loop 检查点

以下是当前 Freely Runtime 中已实现的 auto-loop 检查点（基于生命周期 trace 实际观测验证）：

### Daemon 启动链
| 检查点 | Stage | 说明 |
|--------|-------|------|
| `A-L001` | `start_requested` | 用户发出 daemon start 命令 |
| `A-L010` | `supervisor_started` | Supervisor 进程已启动，进入 daemon-run 主循环 |
| `A-L240` | `manager_launch_requested` | Supervisor 请求启动 Manager AI session（下一跳 `A-L010`） |

### 监督与恢复链（ensure-manager / watchdog 侧）
| 检查点 | Stage | 说明 |
|--------|-------|------|
| `A-L090` | `supervisor_cleanup_begin` | Supervisor 退出清理开始 |
| `A-L091` | `supervisor_cleanup_superseded` | 清理让位于更新的活跃 supervisor |
| `A-L092` | `supervisor_cleanup_complete` | 清理完成（desired=running 时下一跳为重拉控制面） |
| `A-L201` | `manager_waiting_for_supervisor_teardown` | Watchdog 等待旧 supervisor 退出 |
| `A-L202` | `manager_supervisor_teardown_observed` | Watchdog 观测到 teardown 完成 |
| `A-L210` | `manager_bootstrap_paused` | 网络恢复门控暂停 bootstrap |
| `A-L211` | `manager_same_tool_recovery_blocked` | 同工具 slot 耗尽阻塞 |
| `A-L212` | `manager_same_tool_recovery_blocked` | 当前 slot 入口不可用阻塞 |
| `A-L225` | `manager_stale_pid_scan` | Worker stale pid 扫描 |
| `A-L230` | `manager_recovery_waiting` | 全部恢复路径不可用，等待 |
| `A-L231` | `manager_bootstrap_skipped` | 无可用恢复工具，跳过本轮 |
| `A-L232` | `manager_supervisor_already_running` | 已有活跃 supervisor，保持现状 |

### Prompt 构建链
| 检查点 | Stage | 说明 |
|--------|-------|------|
| `A-L020` | `prompt_build_begin` | 开始构建 AI prompt（含 scan、handoff、continuity 注入） |
| `A-L021` | `prompt_build_complete` | Prompt 构建完成 |
| `A-L022` | `manager_startup_continuity_stub_checked` | Manager 启动连续性检查完成 |

### AI 执行链
| 检查点 | Stage | 说明 |
|--------|-------|------|
| `A-L040` | `ai_launch_begin` | AI 进程已启动（ACP Bridge → AI CLI Tool） |
| `A-L041` | `ai_launch_observed` | AI 进程存活确认（当前于 cycle 收尾阶段发出，见 §12） |
| `A-L042` | `ai_cycle_finished` | AI 周期结束（exit_reason=ai_exit_rc_0 / ...） |

### Intake 链（human interruption / chat）
| 检查点 | Stage | 说明 |
|--------|-------|------|
| `A-L300` | `intake_recorded` | 插话已记录 |
| `A-L310` | `intake_claimed` | 插话已被 claim |
| `A-L320` | `intake_resolved` | 插话已 resolve |
| `A-L330` | `intake_handler_started` | dispatcher 处理开始 |
| `A-L331` | `intake_handler_decision_parsed` | 处理决策已解析 |
| `A-L332` | `intake_handler_path_unavailable` | 处理路径不可用 |
| `A-L333` | `intake_handler_failed` | 处理失败 |
| `A-L334` | `intake_handler_stderr_without_decision` | 处理有 stderr 无决策 |
| `A-L335` | `intake_handler_stderr_with_decision` | 处理有 stderr 有决策 |
| `A-L336` | `intake_handler_no_decision` | 处理无决策 |

### L042 出口路由

```
A-L042 to=A-L020    → prompt 模式继续下一轮 (acp_multi_turn)
A-L042 to=A-L090    → Worker 委派消费
A-L042 to=A-L201    → 连续性 handoff
A-L042 to=A-L210    → closeout gate
A-L042 to=A-L230    → recovery 恢复
A-L042 to=TERM      → 终止（stop_ai）
```

### A2A Worker Launch 事件

当 Manager exit contract = delegate_workers 时：

```text
event=manager_exit_contract_delegate_workers worker_prompts_csv=<路径或none>
event=worker_task_launched task_id=<id> worktree=<path>
event=worker_launch_failed task_id=<id> reason=<reason>
```

`worker_prompts_csv=none` 表示 Runtime 未发现任何 submitted worker task。常见原因：
1. Manager 使用了 `--agent-id worker` 而非 `--role worker`（task 创建为 agent_id=manager）
2. a2a-exit 命令未被实际执行（AI 仅在文本中讨论了它）
3. a2a_tasks 表不可用（freely-db 未运行或 crash）

## 12. Known gaps（显式暴露，按 §5 UNSET 精神登记）

以下为已确认但尚未修复的契约偏差。修复它们的 lane 必须同步更新本表。

| 缺口 | 现状 | 契约条款 | 状态 |
|------|------|---------|------|
| `A-L041` 发出时机 | 后台观察者于 monitor pid-file 首活时发出（≤60s 观察窗，超时显式缺席） | §8 | resolved (raw-20260717T062449Z) |
| `A-L042` OUT `to=` | 拆相：原位仅 IN，六个真实出口分支各打 OUT（continue→`A-L020`，exit→`TERM`）。语义修订：接力型下游由 `fr=A-L042` 的 IN 记录（L201/L210/L230/L240 属外部进程决策，supervisor 不代打） | §4/§8 | resolved (raw-20260717T062449Z) |
| `A-L090`/`A-L092` OUT `to=UNSET` | L090 拆相（分支出口 to=L091/L092）；L092 按 desired_state 声明 to=L240/TERM；L091 to=TERM | §5 | resolved (raw-20260717T062449Z) |
