---
owner_issue: I-20260521T012042Z-A
issue_id: I-20260521T012042Z-A
---
## Implementation Decision Note

- issue_id: I-20260521T012042Z-A

- decision: `在 keepalive supervisor 循环中增加 manager_scan_stale_worker_pids，对 launched worker PID 执行 kill -0 检测；handoff DB 加 worker_pid 字段，launch 时记录 PID，kill -0 失败标记 stale_pid`
- why_this: `现有 mark_stale() 仅靠 last_activity_at 墙钟超时（15min），worker 进程无声死亡后 keepalive 无法及时检测。直接杀掉管理后台进程，用 os.kill(pid, 0) 做进程存在检测是最小侵入方案——不依赖 /proc、不增加 IPC、不修改 worker 侧代码。集成点选 supervisor while-loop 无条件调用而非 keepalive 链 guard，确保任意分支都能触发扫描。`
- alternatives_considered:
  - `worker 侧主动心跳 → 改动大、要改 worker prompt/ACP bridge，且增加 worker 崩溃后仍可能漏报`
  - `/proc 文件系统检查 → process_inspection_available 只在部分场景可用，降级路径不适用`
  - `manager_supervisor_waiting_on_active_workers 内部集成 → 导致扫描只在该分支触发，其他 keepalive 分支无法受益`
- boundary_non_goals:
  - `worker ACP init 超时自愈（子问题 2，由 C-20260519T015638Z-A 协调）`
  - `跨容器 kill -0 权限问题（当前同用户场景已满足，跨容器走 OSError 回落）`
  - `不是要替代 mark_stale()——它们互补：kill -0 检测硬死亡，mark_stale() 检测进程活着但卡住`
- residual_risk:
  - `handoff_id 解析依赖 prompt_file 匹配，若 worker worktree 有多个历史 handoff 可能错配——用 status IN ('pending','launched') + ORDER BY created_at DESC LIMIT 1 缩小歧义`
  - `worker_pid 为空（T-4 失败或 legacy 记录）→ 扫描跳过，回退到现有 mark_stale() 超时`
  - `launch_worker_from_manager_prompt_if_needed 的 agent_fallback 和 bridge 两条路径都已覆盖 PID 记录`
