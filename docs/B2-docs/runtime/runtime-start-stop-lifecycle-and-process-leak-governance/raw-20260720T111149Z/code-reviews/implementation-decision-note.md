---
issue_id: I-20260720T111149Z-A
issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260720T111149Z/issues/I-20260720T111149Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260720T111149Z-A
- issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260720T111149Z/issues/I-20260720T111149Z-A.md

## Implementation Decision Note

- decision: 采用 Option A（查询层加固 + Supervisor 健康检查回路），四改动点：read_task_mode 错误语义（exit 1）、Supervisor 主循环 DB health gate、ensure_freely_db stale PID 清理、DB daemon 崩溃日志防御。总计 ~30 行改动，2 文件，零新依赖。
- why_this: 复用现有 ensure_freely_db(db.ping + restart) 机制，最小侵入。read_task_mode 有 6 个调用方，`error:db_unavailable` 不匹配任何现有 case 分支（auto/wait/listen/id:），安全降级而不破坏兼容。不需要独立 watchdog 进程（Option B 过度设计）。不修改 Supervisor 的架构假设。
- alternatives_considered: Option B（独立 DB watchdog 子进程）— 过度设计，增加常驻进程和复杂度，与现有 heartbeat 子进程功能重叠。Option C（仅加固 DB daemon 进程）— 不修根因，Supervisor 仍然盲飞，不可接受。
- boundary_non_goals: 不做 DB daemon 自动重启的熔断机制（连续失败 N 次后放弃）；不修改 A2A server 的 DB 依赖逻辑；不改变 task-mode gate 的 auto→listen 迁移逻辑；不引入 systemd/launchd 集成。
- residual_risk: DB daemon 如果因 OOM killer 被 SIGKILL，SIGKILL 不可捕获 → FATAL traceback 无法写入（但 signal handler 至少会写 SIGTERM/SIGINT 的退出日志，且 Supervisor 的 health gate 会检测到 DB 不可用并写 db_unavailable）。极端场景下（DB 文件系统满），daemon 可能反复 crash-loop，需后续迭代加熔断。
