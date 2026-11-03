# Brainstorms: owner-lane 认领被守卫挡住

## 1. 事实

- `_resolve_current_agent_id` 在无绑定时调用 `owner_lane.py claim`，但调用被一层 bash 守卫包住：

      if [[ -z "$_my_id" && "$_current_path" != "$project" ]]; then

- daemon 在工位内启动时 `pwd` 与传入的 project 相同，条件恒假 → claim 从未执行。
- 上一轮的“验证通过”是因为先手工跑过一次 claim，把 `agent_working` 行写进去了；自动路径一次都没跑过。
- 失败表现与修复前完全一致（同一句 `agent_working has no entry`），所以很容易被误判为“还没修”。

## 2. 三个 Option

### Option A：删掉 `!=` 守卫，无条件调用

- 做法：`_my_id` 为空就调 claim，安全交给 claim 内部四条守卫。
- 优点：bash 里不再有“什么情况下该认领”的判断，只有“问一次”。
- 缺点：依赖 claim 内部守卫是否真的足够（需要逐条确认，见下）。

### Option B：保留守卫、改成“路径相等也要认领”

- 做法：`if [[ -z "$_my_id" ]]` 且再判断 `_current_path` 是本项目 worktree。
- 否决：这正是 claim 内部已经在做的事（`git worktree list`）。在 bash 里再实现一遍，等于把同一规则写两处，且 bash 侧仍然不可单测——这次的 bug 就是这样产生的。

### Option C：把“该不该认领”整体下沉到 owner_lane（选中）

- 做法：A + 让 bash 只做“调用 + 记录失败原因”，判定全部在 `owner_lane.claim`。
- 优点：`project == path` 变成普通输入，可以写单测；守卫逻辑集中一处；bash 里不再出现第二套规则。
- 代价：每次身份解析失败会多一次 Python 调用（约 50ms），可接受。

## 3. 为什么 claim 内部的守卫够用

| 场景 | claim 的行为 |
|---|---|
| 已有绑定 | `_bound_agent` 命中，原样返回，不写 |
| 项目根（分支 develop） | 解析不出 raw key → `raw_key_unresolved`，不写 |
| 普通分支（无时间戳） | 同上 |
| 多 manager | `manager_not_unique`，不写 |
| 不是本项目 worktree | `not_a_worktree`，不写 |
| 读不到 DB | `rows_unreadable`，不写 |

也就是说，“不该认领”的每一种情况都已经有对应返回，外层不需要再挡一次。

## 4. 不做什么

- 不改 claim 的四条守卫本身。
- 不改 `agent_working` 表结构。
- 不为 bash 再写一套 worktree 判断。

## 5. 风险

| 风险 | 缓解 |
|---|---|
| 项目根被误认领 | 根分支是 develop，`raw_key_unresolved` 拦住；补一条单测锁死 |
| 认领失败仍然静默 | 把 `2>/dev/null` 改为捕获 stderr，把 reason 写进日志 |
| 同一工位重复认领 | `existing` 分支早返回；补一条单测 |
