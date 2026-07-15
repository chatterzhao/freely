---
b1_id: B1-20260714T021808Z
phase_state: completed
source_raw: raw-20260714T021808Z
source_url: https://github.com/chatterzhao/freely/issues/3900
created_at: 2026-07-14
---

# B1_IBM: task_mode 传递链修复 + AI_MODE 守卫

## Input
- raw-20260714T021808Z: 4 项设计缺陷导致 daemon 无法按预期模式启动
- 来源：daemon 启动观察 + 代码审查

## Problem

### 现状：task_mode 状态机

| 模式 | 含义 | 进入方式 |
|------|------|---------|
| `wait` | 默认。sleep poll，不启动 AI | `daemon start` 无 `--task-mode`；stop_ai 重试超限 |
| `auto` | AI 全自主运行 | `daemon start --task-mode auto`；listen scan 发现任务 |
| `listen` | 定期扫描（300s 间隔），发现 ready 任务自动切 auto | stop_ai 无 ready 任务时自动切换 |
| `id:<scan-id>` | 按指定 scan 驱动 | task-scan 触发 |

### 设计意图 vs 实现差距

#### 缺陷 1: `daemon start --task-mode auto` 不生效

调用链：
```
cmd_daemon_start (L23529)
  → 解析 --task-mode ✓, write_task_mode DB ✓
  → launch_project_runtime_daemon_or_fail "$project"  ← ❌ 不传 task_mode
    → Python subprocess: daemon-run --project <path>  ← ❌ 无 --task-mode
      → cmd_daemon_run (L23701): task_mode 解析到空
        → start_project_runtime "$project" "daemon"  ← ❌ 不传 task_mode
          → ensure_task_mode_gate "$project" "wait"  ← ❌ hardcode wait
```

根因：`launch_project_runtime_daemon_or_fail` (L23480) 签名只接受 `$1`(project)，不接受 task_mode。Python spawn 固定不带 `--task-mode`。`start_project_runtime` (L22003) hardcode `"wait"`。

`ensure_task_mode_gate` 调用 `task-mode.init --default`（SQLite INSERT OR IGNORE），本身是合理的 fallback 机制——DB 无值时才初始化。问题在于：即使上层传了 task_mode，这一层也不接收。

#### 缺陷 2: `launch_manager_supervisor` (watchdog 重启) 不认 `listen`

L18253-18254：
```bash
local _restart_mode; _restart_mode="$(read_task_mode "$project")"
[[ "$_restart_mode" == "auto" || "$_restart_mode" == "wait" || "$_restart_mode" == id:* ]] || _restart_mode="auto"
```

允许列表缺 `listen`。DB 有 `listen` 时，fallback 到 `auto`——severity 反而升级了（从被动监听到全自主）。应加入 `listen`。

`read_task_mode` (L8773-8774) DB query 失败时返回 `wait`——正确。`ensure_task_mode_gate` 的 init default 也是 `wait`——正确。

#### 缺陷 3: fallback 值错误

L18254: `|| _restart_mode="auto"` —— fallback 应为 `wait`，与以下保持一致：
- `read_task_mode` DB 失败返回 `wait` (L8774)
- `ensure_task_mode_gate` default `wait` (L8753)
- `write_task_mode` 无 `--task-mode` 时写 `wait` (L23585)

#### 缺陷 4: AI_MODE 裸引用 crash

L22697/22719/24994 三处 `$AI_MODE` 无守卫。`freely init` 不初始化 `AI_MODE` 环境变量。`set -euo pipefail` (L2) 下触发 unbound variable crash。L22697 在 AI launch 前，crash 导致 supervisor 在 L022→L040 之间静默死亡（stdout/stderr 被 `>/dev/null 2>&1` 丢弃），watchdog 检测 stale 后重启。表现为 supervisor 每 ~21s 重启一次，AI 永远无法启动。

### listen 模式行为分析（已确认正确）

L22557-22580：
1. 读取 task_mode
2. 若 `listen`：运行 `task_source_scan` → 检查 ready items
   - ready > 0 → `write_task_mode "auto"`，continue（进入 AI 循环）
   - ready = 0 → sleep `LISTEN_INTERVAL`（默认 300s），continue
3. 若 `wait`：sleep `CHECK_INTERVAL`（默认 10s），continue

**listen 模式有完整的 scan 机制**。stop_ai 时若 scan 无 ready items (L16097-16107)，切换到 `listen`。`listen` 定期 scan，发现任务后自动切 `auto`。这个设计是正确的，无需修改。

## Brainstorm

### Option A: 打通全链路 task_mode 传递

修改 4 处：
1. `launch_project_runtime_daemon_or_fail` 增加 `$2` task_mode 参数
2. Python spawn 增加 `--task-mode` 
3. `cmd_daemon_run` 将 task_mode 传给 `start_project_runtime`
4. `start_project_runtime` 增加 `$3` task_mode 参数，替换 hardcode `wait`

优点：彻底打通，语义清晰
缺点：改动面较大（4 个函数签名），增加参数传递复杂度

### Option B: 仅靠 DB，不传递 task_mode

`cmd_daemon_start` 写 DB → `ensure_task_mode_gate` 改为从 DB 读而非 hardcode → daemon-run 启动时读 DB。

优点：改动最小
缺点：违背设计意图——"手工启动不准读数据库"。用户明确要求：手工启动以传参为准，默认 wait。

### Option C: 最小链路修复

只修两处关键断裂：
1. `launch_project_runtime_daemon_or_fail` + Python spawn：接受并传递 task_mode
2. `start_project_runtime`：接受 task_mode 参数，替换 hardcode

其他函数签名不变（`cmd_daemon_run` 已解析 task_mode，只需传给 `start_project_runtime`）。

优点：在 Option A 和 B 之间取平衡，不改动不必要的函数签名
缺点：仍需改 3 处

## Decision: Option C — 最小链路修复

理由：
1. 设计意图明确：手工启动以传参为准。Option B 违背此原则。
2. Option A 和 C 本质相同，但 C 更克制——`cmd_daemon_run` 已解析 task_mode，只需加一行传参。
3. `listen` 模式已有完整 scan 机制，只需修 `launch_manager_supervisor` 的识别+fallback。

### 具体改动

**A. task_mode 传递链：**
- `launch_project_runtime_daemon_or_fail`: 增加 `$2` task_mode → Python spawn 加 `--task-mode`
- `cmd_daemon_start` L23642: 传 `$task_mode`
- `start_project_runtime`: 增加 `$3` task_mode → L22003 改用 `${3:-wait}`
- `cmd_daemon_run`: L23711 传 `$task_mode`

**B. watchdog 重启：**
- `launch_manager_supervisor` L18254: 允许列表加 `listen`，fallback 改为 `wait`

**C. AI_MODE 守卫：**
- L22697: `$AI_MODE` → `${AI_MODE:-none}`
- L22719: `$AI_MODE` → `${AI_MODE:-none}`
- L24994: `${AI_MODE}` → `${AI_MODE:-none}`

## Candidate
- candidate_id: C-20260714T021808Z-A
- status: promoted
- milestone: M-20260714T021808Z-A
