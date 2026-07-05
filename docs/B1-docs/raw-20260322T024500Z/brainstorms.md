# 预研：runtime worker launch linkage and stall recovery

## 背景

真实 dogfood 已经证明：

- 主管能够通过 `freely chat` 接住项目级监督请求
- 主管能够 patrol 剩余 worktree，并稳定产出 `retire-only / continue-dev`
- 主管能够写出 manager continuity，并生成具体 worker prompt 文件

但最新集成观察暴露出两个 runtime 级缺口：

1. `worker prompt` 只生成不消费  
   当前 `manager continuity` 已经给出 worker launch order 和 prompt 文件，但 runtime 没有把这些 handoff 真正转成 worker worktree 的执行。

2. 长时间无输出的 AI 进程不会被 runtime 识别成 stall  
   当前 manager `codex exec` 进程在 `cycle log` 长时间不更新、CPU 为零且有新 intake 堆积时，仍被视为 `ai_active`，导致新的主管任务无法进入下一轮 prompt。

## 现有真源

- 已完成 `I-20260320T194500Z`
  - `watchdog live-status surface and manager supervision`
  - 明确把 `stall scoring` / 更强 runtime 评分留给未来 lifecycle
- 已完成 `I-20260322T022800Z`
  - `manager delegation after sufficient patrol evidence governance`
  - 已要求主管在证据充分后必须切到 worker delegation
  - 但 issue 明确说：如果后续仍观察到“主管已委派但 runtime 没进入 worker execution”，应通过新的 lifecycle 进入 runtime / delegation mechanism 层修复

所以这次不是回写历史 issue，而是进入一条新的 runtime lifecycle。

## 问题收敛

### A. delegation artifact 已存在，但 launch linkage 缺失

当前事实：

- manager continuity 已包含：
  - worker launch order
  - 每个 worker 对应的 prompt 文件
- `manager_runtime_recover_workers_if_needed()` 只会恢复已经被标记为 `DESIRED_RUNTIME_STATE=running` 的 worker
- 当前没有任何地方把 manager 产出的 worker handoff 变成：
  - 目标 worker 的 delegated continuation intake
  - 或 target worker 的 expected-running 状态

所以问题不在 patrol，也不在 worker recover，而在：

`manager continuity artifact -> runtime worker launch linkage`

### B. stalled AI recovery 缺口

当前 facts：

- ai pid 存活
- 当前 cycle log 在数分钟内无更新
- CPU 接近 0
- 新 intake 已 classified / delegated
- supervisor 仍认为当前 workcell `ai_active`

这说明当前 runtime 还缺：

- 对“长时间无输出且有待处理新 signal”的 stall 判断
- runtime-owned graceful preemption / restart

## 方向

### 1. worker handoff canonical path

正式方案不应依赖：

- 操作外部 TUI 输入框
- 手工再复制 manager continuity 内容

更合理的是：

- manager 产出 worker prompt artifact
- runtime 将其转译为目标 worker worktree 的 delegated continuation intake
- target worker runtime 按已有 prompt build / continuation absorption 机制消费

这使 Freely 保持：

- `Freely chat/tui` 是唯一人类入口
- 外部工具仍是 headless / non-interactive
- 会话编排和 handoff 由 Freely 控制面承担

### 2. stalled AI recovery

当前更像 `runtime watchdog` 范畴，而非 manager prompt 语义。

建议最小检测信号：

- AI pid 仍在
- 当前 cycle log / debug log 在阈值窗口内无更新
- 有更晚的新 intake 或 delegated continuation 待消费

命中后：

- 先尝试 graceful termination
- 超时后 hard-kill fallback
- 留下 runtime-owned recovery evidence
- 让 supervisor 起下一轮 prompt

## 生命周期判断

这条线是实现型 runtime governance，不是纯研究。

因此应继续：

- candidate
- milestone
- IBM
- dev
- verification

之后才能合并到上一层。

## 初步范围

1. 定义 manager-generated worker handoff 的 runtime ingestion contract
2. 把 manager handoff 转成 target worker intake / expected-running linkage
3. 为 manager runtime 增加最小 stall detection + recovery
4. 补最小集成测试：
   - manager 生成 worker prompt 后，runtime 真正把 worker 拉起
   - stalled AI + pending intake 时，runtime 触发 recovery

## 非目标

- 不重写整套 supervisor 架构
- 不发明新的外部 AI 工具
- 不把主方案切换到操纵外部工具 TUI
- 不在本 issue 内扩成完整 event stream / stall scoring 平台
