# Brainstorms: owner lane 的 daemon 身份自举

## 1. 事实

- `freely daemon start` 在 `wt-create` 出来的 `test-pre-merge-*` 工位里启动即退出，报 `unable to resolve agent identity … agent_working has no entry`。
- 身份解析只有一条路：`_resolve_current_agent_id` 按 `pwd` 去 `agent_working` 找 `worker_id / manager_id / reviewer_id`；找不到就 fail-closed（注释明确写着“agent-id.env is retired，不允许静默回退 manager_01”）。
- `agent_working` 的行由 manager 派工时通过 `agent_assign` 写入。owner 直接开的工位没有这一行，于是永远解析不到身份——鸡生蛋。
- 身份只被用于一件事：查 `agent-table.toml` 的 slot，得到 `AGENT_AI_TOOL`。它不决定权限边界，但决定用哪个工具/凭证。

## 2. 三个 Option

### Option A：`wt-create` 写入 manager 行

- 做法：建工位时直接 `agent_assign(role=manager)`。
- 优点：身份解析保持单一路径，没有 fallback。
- 否决：`wt-create` 不区分“owner 自建”和“manager 为 worker 建”。给 worker 工位写 manager 行，会让该工位的 daemon 以 manager 身份运行——把最不该松的一层松掉了。

### Option B：解析时无状态回退到 manager

- 做法：`_resolve_current_agent_id` 找不到行时，直接返回 `manager_01`，不落库。
- 优点：改动最小。
- 否决：`agent_working` 会继续为空，任何依赖该表的路径（scan 的工位归属、watchdog 的存活判定）仍然看不到这个工位。问题被掩盖而不是解决，而且这正是原注释禁止的“静默回退”。

### Option C：显式 claim + 只对 manager 放行（选中）

- 做法：新增 `runtime/owner_lane.py`，提供 `claim(project, path)`：
  1. 若该路径在 `agent_working` 已有任意角色的行 → 原样返回（不覆盖，`created=false`）。
  2. 否则要求：路径确实是本项目的 git worktree、且项目只配置了一个 manager。
  3. 用 `agent_assign(role=manager, worktree=path, branch=<当前分支>)` 落库，raw_key 从分支名提取。
  4. 返回 `{agent_id, raw_key, branch, created}`。
  `_resolve_current_agent_id` 在原逻辑失败后调用它，并打印一条显式日志 `owner-lane claim: <path> → manager_01`。
- 优点：
  - 「单一事实来源」保持不变，仍以 `agent_working` 为准，只是补上它缺的那一行。
  - 只在“完全没有行”时生效，绝不覆盖已有绑定；有行的工位（正常 worker）行为不变。
  - 有审计痕迹：谁、什么时候、因为什么被认领。
- 代价：若某个 worker 工位的行被误删（DB 损坏），该工位的 daemon 会以 manager 身份启动。缓解：认领必须“项目只有一个 manager”才成立，并且日志可被 scan 抓到。

## 3. 决策

选 **Option C**。它把“owner lane 没有身份”从**例外**变成**可表达的常规状态**，而不是让解析器学会猜。

## 4. 不做什么

- 不给 worker 角色任何自动认领通道（`role != manager` 一律走原 fail-closed）。
- 不恢复 `agent-id.env`。
- 不改 `agent_working` 的表结构。
- 不在 `wt-create` 里写行（避免把 owner/worker 两种语义混在同一个命令里）。

## 5. 风险

| 风险 | 缓解 |
|---|---|
| DB 里 worker 行丢失后被误认领为 manager | 仅当“该路径零行”且“项目只有一个 manager”才认领；日志显式；C-B 负责加一致性巡检 |
| 一个项目配多个 manager | 认领直接失败（要求唯一），保持 fail-closed |
| 认领后 DB 与 git（worktree 被删）不一致 | claim 前校验 `git worktree list`，不做“凭路径猜” |
| `agent_assign` 写入失败 | 认领失败即返回原 fail-closed，不吞异常 |
