# Brainstorms — raw-20260506T1000Z: task_mode=wait 前置轮询门禁

## Discovery

### 问题陈述
`task_mode=wait` 启动 Freely 时仍会发射 AI 循环。门禁仅存在于 AI 结束后的 `manager_runtime_handle_exit_contract_after_ai_cycle`（stop_ai handler），缺少 supervisor 循环在 build prompt / launch AI 之前的前置轮询门禁。

### 时效性判断
- 提出时间：2026-05-06T10:00:00Z
- 当前时间：2026-05-19 — issue 仍处于 proposed 状态，未被其他工作覆盖
- 原始 task_mode 实现（commit 32243539）将 wait 门禁仅放在 stop_ai 后置处理器中，属于已知设计缺失
- 该项目功能（task_mode wait）是 Freely 的核心控制面基础能力，值得修复

结论：**值得投入**，该 issue 仍然有效且未被覆盖。

## Research

### 边界检查
- **CONSTITUTION.md**：无直接冲突。宪法要求 AI 自主管理闭环，但 wait 模式不违反该原则（wait 是用户显式要求暂停）。
- **LAWS.md**：无直接冲突。分支与工作树策略不涉及 task_mode 内部逻辑。
- **PROJECT_INTENT.md**：无直接冲突。项目意图要求 AI 持续运行"除非明确停止"，wait 正是明确停止方式。

### 当前实现分析
原始实现路径（commit 32243539）：
1. Supervisor 主循环 → `select_launch_kind` → build prompt → launch AI
2. AI 执行完毕 → `manager_runtime_handle_exit_contract_after_ai_cycle`（stop_ai handler）
3. stop_ai handler 检查 `read_task_mode`：
   - `wait` → sleep CHECK_INTERVAL → return continue
   - `auto` / `id:<scan-id>` → 正常继续

缺失环节：`select_launch_kind` 之前没有检查 task_mode。所以当 `task_mode=wait` 时，supervisor 仍然执行 build prompt + launch AI，只是 AI 执行完后立即被 stop。

### 依赖关系
- 本 issue 不依赖其他未合并的 feature 分支
- 改动范围：supervisor 主循环中 `select_launch_kind` 之前的入口
- 风险：低。新增一个前置读 + sleep + continue，不影响已有逻辑

## Decision

### 方案 A（推荐）：前置门禁
在 supervisor 主循环 `select_launch_kind` 之前，增加：
```
read_task_mode=wait → sleep CHECK_INTERVAL → continue
```
- 优点：最简洁，零侵入，完全可逆
- 缺点：无

### 其他考虑
- 不需要新增配置项，复用已有 `task_mode` 字段
- 不需要改 stop_ai handler 的逻辑（保留作为兜底）
- 建议 CHECK_INTERVAL 与现有 wait 间隔一致

### 结论
采用方案 A。这是一个修复而非新功能，改动边界清晰、风险极低。

## Next Step
进入 B2_IBM materialize，产出 I-* issue 并投入 dev-loop 实现。
