---
b1_id: B1-20260717T004620Z
phase_state: completed
source_raw: raw-20260717T004620Z
source_url: https://github.com/chatterzhao/freely/issues/3945
produced_candidate: C-20260717T004620Z-A
created_at: 2026-07-16
---

# B1_IBM: ensure-manager 秒杀新生 supervisor 引发 restart storm（附 TERM 语义矛盾与 storm 检测盲区）

## Input

- 来源：2026-07-16 全天 runtime 故障排查（人类主导会话），`freely feedback` 建 raw issue raw-20260717T004620Z
- 现象：当日 493 次 supervisor_cleanup；三次 restart storm（06:12–06:25、15:28–15:56 等）；runtime 不可用约 9 小时；`restart_storm_signal_*` 全程 unavailable
- 证据锚点：`.freely/logs/runtime-events.log`（25378 行前）、`.freely/logs/lifecycle-trace.log`（L010→L090 直跳、无 L020）、受控实验 2026-07-17T00:01:57Z 与 00:16:27Z `daemon_signal_ignored`

## Problem

三个耦合缺陷，同属「watchdog↔supervisor 生死判定」域：

### C1 — heartbeat-stale kill 无新生宽限（storm 主因）

`ensure_manager_once`（`docs/system/workspace/scripts/runtime/freely` ~L19219-19255）heartbeat 活性检查：

- heartbeat 文件**缺失**分支：以 `sup_pid_file` mtime 为基准给 15s 宽限 ✓
- heartbeat 文件**存在但 stale >120s** 分支：**立即 `kill`，无任何宽限** ✗

而 heartbeat touch 子进程要到 supervisor 启动流程末段（bridge init 之后，~L22491）才启动。实测新生 supervisor 从 `supervisor_started`（L010）到 heartbeat 子进程就位有 10–15 秒裸奔窗口（doc gate ~7s + bridge init ~10s）。只要磁盘上遗留一个 stale heartbeat 文件（任何 AI 崩溃 / supervisor 非正常退出都会遗留），每个新生 supervisor 都会在裸奔窗口内被 ensure-manager 处决。

时序证据（storm 每周期规律完全一致）：
```
22:31:15Z supervisor_started pid=78082          (L010)
22:31:16Z ensure-manager tick（self-heal 事件为锚）
22:31:17Z supervisor_cleanup pid=78082          (L090, stop_requested=0)
22:31:19Z 下一轮 start_project_runtime_enter
```

### C2 — kill 通道语义矛盾（双 supervisor 帮凶）

daemon supervisor 有意忽略无 stop-marker 的裸 TERM（`request_stop` ~L22199-22210，`daemon_signal_ignored` 事件）。但 `ensure_manager_once` 的 heartbeat-kill 恰好就是裸 `kill`（TERM，~L19253）。两种结局都错误：

- TERM 落在 trap 安装前的窗口 → 杀死新生儿 → storm（C1 场景）
- TERM 落在 trap 安装后 → 被忽略 → ensure-manager 误信已杀死（`current_pid=""`）→ 拉起第二个 daemon → **双 supervisor 并存**

双 supervisor 后果实测（2026-07-17T00:16 与 00:33 两次重启均复现）：`daemon_signal_ignored` 3 秒后出现第二个 `start_project_runtime_enter`；两个主循环并存互踢 bridge 健康检查（与 raw-20260717T004654Z 的 bridge 泄漏叠加放大）。

### C4 — storm 检测盲区（设计承诺未兑现）

`skill:freely-watchdog-control-plane` 第 47 行契约：detect restart storms / rapid relaunch churn → escalate 给 manager-owned auto-loop 判断。实际：

1. `update_restart_storm_window` 仅在 **AI 周期完成后**调用（~L23069）。storm 中 supervisor 根本活不到 AI 启动，窗口计数恒为零 → 493 次 cleanup 零检出
2. `runtime_active_process_count_for_project`（~L14830-14843）仅统计 supervisor+dispatcher+ai 三种，上限 3，而 `PROCESS_CHURN_PEAK` 默认 10 → 该条件数学上不可触发
3. 阈值口径不一致：函数后备值 `RESTART_STORM_COUNT:-4`（L14902）vs config init `RESTART_STORM_COUNT=10`（L4397）

## Brainstorm

### Option A：只修 C1（heartbeat 宽限）

给 stale-heartbeat 分支加新生宽限。改动最小。
- 反对：C2 未修则「stale 且真死」场景下 kill 被忽略仍会拉双 daemon；C4 未修则下次同类故障依旧零检出、零升级。三者是同一判定域的三个面，拆开修会留下已知病理。

### Option B：C1+C2+C4 一体收口（本 lane 全修）

1. **C1**：stale-heartbeat 分支比较 `sup_pid_file` mtime 与 heartbeat mtime——若 supervisor 比 heartbeat 新（新生），按缺失分支逻辑给启动宽限（复用 15s 基准，可配 `SUPERVISOR_STARTUP_HEARTBEAT_GRACE_SECS`）；同时把 heartbeat touch 子进程**提前到 supervisor_started 之后立即启动**（把 ~L22491 的心跳块上移到 trap 安装后），把裸奔窗口从 10–15s 压缩到 <1s，双保险。
2. **C2**：ensure-manager 需要重启 supervisor 时走既有正规通道 `restart_manager_supervisor_preserving_handoff`（其 `terminate_pid_with_graceful_wait` 有 TERM→等待→KILL 兜底并清理 pid/identity），且 kill 后**验证进程确实退出**再置 `current_pid=""`；绝不在进程仍存活时启动第二个 daemon。
3. **C4**：(a) 在 `cleanup_supervisor`（L090/L092 路径）追加 storm window 记录（事件粒度 = supervisor 生命周期终止）；(b) `PROCESS_CHURN_PEAK` 默认降到可达域（与计数器口径匹配，取 3）或扩大计数口径——选降默认值，改动面小且语义清晰；(c) 统一 `RESTART_STORM_COUNT` 后备值与 config init 一致（10→函数后备同为 10，或都改 4——取 config 为准，函数后备改 10）。

### Option C：重构整个 watchdog 判定层（把 ensure-manager 的活性判定挪进独立 watchdog 模块）

符合 watchdog-control-plane「可复用脚本优先落 skill」的长期方向。
- 反对：改动面大、回归风险高，当前 runtime 处于脆弱期，先止血；重构方向留给 watchdog-control-plane 既有治理线。

## Decision: Option B

- 三缺陷同域同因（生死判定的输入、动作、观测三个面），一体修才能消除病理闭环：stale heartbeat（输入失真）→ 误杀/误信（动作错误）→ 零检出（观测失明）
- 改动收敛在 `runtime/freely` 的 4 个函数与 1 处代码块搬移，无接口变更、无跨模块迁移，不触发 Option C 级别的架构评审
- 每个子缺陷都可独立写出 RED 测试（见 acceptance_criteria），GREEN 可判定

## 边界与依赖

- 只改 `docs/system/workspace/scripts/runtime/freely`（已知历史债务大文件，本 lane 不做拆分，不新增超行数模块）
- 不改 bridge 生命周期（raw-20260717T004654Z 的 scope）、不改 sse pid 校验（raw-20260717T004721Z）、不改 stall 判定（raw-20260716T114802Z）
- 不依赖未合并分支，base = develop

## Candidate

- candidate_id: C-20260717T004620Z-A
- status: promoted
- milestone: M-20260717T004620Z-A
