---
local_id: raw-20260717T004620Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260717T004620Z-A
platform_ids:
  github:
    issue_id: '3947'
    url: https://github.com/chatterzhao/freely/issues/3947
    synced_at: ''
  gitee:
    issue_id: IK1L7Q
    url: https://gitee.com/zhaoquan/freely/issues/IK1L7Q
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-17T00:46:43Z'
updated_at: '2026-07-17T00:46:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 现象（2026-07-16 全天 493 次 supervisor_cleanup，storm 三次，runtime 不可用 9 小时）
supervisor 启动 1-2 秒即被杀，ensure-manager 每 ~11s 重拉，restart_storm_signal 全程 unavailable。

## 根因（三个耦合缺陷，同属 watchdog↔supervisor 生死判定域）
1. **heartbeat-stale kill 无新生宽限**：runtime/freely ensure_manager_once（~L19219-19255）在 heartbeat 文件「存在但 stale>120s」时立即 kill supervisor；15s 宽限只覆盖文件缺失分支。heartbeat touch 子进程要到 bridge init 之后（~L22491）才启动，新生 supervisor 有 10-15s 裸奔窗口。任何 AI 崩溃遗留 stale heartbeat 后，每个新 supervisor 都在窗口内被处决。
2. **kill 语义矛盾**：daemon supervisor 故意忽略无 stop-marker 的裸 TERM（request_stop ~L22199），而 ensure_manager_once 的 heartbeat-kill 恰是裸 TERM。结果两态皆错：打中裸奔窗口=杀新生儿（storm）；被忽略=ensure-manager 误信已杀死→拉起第二个 daemon→双 supervisor 并存互踢 bridge（2026-07-17T00:16 与 00:33 重启实验均复现：daemon_signal_ignored 后 3 秒出现第二个 start_project_runtime_enter）。
3. **storm 检测盲区**：update_restart_storm_window 仅在 AI 周期完成后调用（~L23069），supervisor 进程死亡不计数；runtime_active_process_count 上限 3（~L14830-14843）而 PROCESS_CHURN_PEAK=10 永不可达；RESTART_STORM_COUNT 函数后备值 4 与 config init 10 不一致（L14902 vs L4397）。违反 watchdog-control-plane SKILL 第 47 行 escalate 契约。

## 修复方向
- heartbeat 检查对「sup_pid_file 比 heartbeat 新」的新生 supervisor 给宽限（比对 sup pid mtime 而非仅文件存在）；heartbeat toucher 提前到 supervisor_started 后立即启动
- ensure-manager 杀 supervisor 改用带 stop-marker/teardown 语义的正规通道，或杀前确认死亡再拉新
- storm window 记录 supervisor_cleanup 事件；修正 PEAK 与 COUNT 阈值口径

## 证据
.freely/logs/runtime-events.log 25378 行前后；lifecycle-trace L010→L090 直跳（无 L020）；受控实验 2026-07-17T00:01:57Z daemon_signal_ignored pid=88621
