# B1_IBM Brainstorm: Worker Fork A2A Socket + JSON Parse + Scan Filter

## Discovery

启动 freely daemon 观察运行时行为后，发现 worker 重复分配问题：4 个 worker fork session 产出了完全相同的 B1_IBM 文档。

排查发现三个相互叠加的根因：
1. Worker fork session 的 `a2a_task.py` 无法连接 A2A server（socket 路径基于 worktree CWD 而非 manager project）
2. 8 处 `json.load(sys.stdin)` 内联 Python 代码错误解析了 `a2a_task.py list` 的 `{"rows": [...]}` 输出格式
3. Manager 对 worker 任务状态缺乏感知——scan filter 只检查 `working` 状态，不检查 `submitted`/`launched`

这三个问题叠加：A2A 不可达 → worker 无法 report completion → 任务永远停在 submitted → busy-guard JSON bug 使其全部通过 → 无去重使每轮 cycle 累加新任务。

## Research

现有保护机制：
- `worktree_has_active_worker`: 本应拦截重复 worker，但因 JSON bug 永远返回 false
- `manager_exit_contract_kind`: 本应只在真正有 pending worker 时返回 delegate_workers，但因 JSON bug 永远返回 delegate_workers
- Scan filter (L16438): 已正确使用 `has-active-worker` 命令，但 fallback 路径只检查 `working` 状态

`a2a_task.py prompt` 子命令（L725-736）已实现但从未被调用——它是为 Manager steer 模式准备的基础设施。

`SESSION_PARENT_PROJECT` 已写入 worker session state file（L12454）但未导出到环境变量。

## Decision

三个 fix 按依赖顺序实施：
1. #3201: Export `SESSION_PARENT_PROJECT` + `_resolve_project()` 检查 env var（3 行）
2. #3200: 修复所有 JSON 解析站点 → `data.get("rows", [])`（~15 行）
3. #3202: Scan filter 增加 `submitted`/`launched` 状态检查（1 行）

均为 bug fix，改动量小（~23 行），无需架构变更。
