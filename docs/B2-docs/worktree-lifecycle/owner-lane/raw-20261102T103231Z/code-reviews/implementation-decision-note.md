- issue_id: I-20261102T103231Z-A
- issue_path: docs/B2-docs/worktree-lifecycle/owner-lane/raw-20261102T103231Z/issues/I-20261102T103231Z-A.md

## Implementation Decision Note

- decision: 采用“显式认领”，而不是让解析器静默回退 manager_01。
- why_this: 身份只用于解析 `AGENT_AI_TOOL`，但“谁在这个工位跑”是该表的唯一事实来源。owner 自建的工位缺这一行，正确做法是补上它并留痕，而不是让解析函数在缺行时假装自己是 manager。前者可审计、可回收，后者会把“没有身份”变成永久的隐形例外。
- alternatives_considered:
  - wt-create 写 manager 行：wt-create 不区分 owner 自建与 manager 派工，会给 worker 工位写入 manager 身份，把最不该松的一层松掉。
  - 无状态回退：不落库，scan / watchdog 仍看不到工位归属，问题被掩盖。
- boundary_non_goals: 不改 `agent_working` 表结构；不恢复 `agent-id.env`；不给 worker/reviewer 自动认领；不做行级一致性巡检（C-B）。
- residual_risk:
  - 若 worker 工位的行被误删（DB 损坏），该工位 daemon 会以 manager 身份启动。守卫降为“路径零行 + 项目唯一 manager + 真实 worktree + 分支可解析”，并打印 `owner-lane claim` 日志；C-B 负责加巡检。
  - 认领会一直保留到 `wt-close`；当前没有 TTL。
  - `wt-create` 复制 `agent-table.toml` 到 test 工位是**拷贝**而非链接：root 改了 slot，已有工位不会自动跟随。这与 `freely.db` 的复制策略一致，但属于已知漂移点。

### 端到端暴露的三个断面（同属一个缺陷）

1. 工位没有 `agent-table.toml` → `manager_not_unique` → 改为从 `FREELY_HOME` 读。
2. test 车道分支没有 `raw-` 前缀 → `raw_key_unresolved` → 正则接受 `test-pre-merge-<KEY>`。
3. slot 解析仍读工位本地表 → `AGENT_AI_TOOL not set` → `wt-create` 复制 agent-table 到 test 工位。

三个都不是“顺手多改”，而是“daemon 能否在这个工位跑起来”的同一根因在不同层的表现。
