---
local_id: raw-20260720T111149Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260720T111149Z-A
platform_ids:
  gitee:
    issue_id: IK2DZE
    url: https://gitee.com/zhaoquan/freely/issues/IK2DZE
    synced_at: ''
primary_platform: gitee
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-20T19:12:13+08:00'
updated_at: '2026-07-20T19:12:13+08:00'
intake_id: ''
author: platform
channel: gitee
session_refs: []
---

\n\n## 复现环境\n项目：/Users/zhaoyu/Downloads/code/my-freely/freely\n入口：./bin/freely daemon start --project <project> --task-mode auto\n\n## 稳定复现步骤\n1. 正式 daemon stop，确认 workcell-state.env 为 stopped、Supervisor/AI=down。\n2. 执行 daemon start --task-mode auto。\n3. 启动初期 task-mode get 成功返回 task_mode: auto，daemon status 返回 running；daemon-launch.log 同时记录 freely-db ready、A2A ready、Supervisor started。\n4. 等待约 10-15 秒，再执行 task-mode get 与 daemon status。\n\n## 预期\n- freely-db daemon 在 Runtime/Supervisor 生命周期内持续可用；\n- task-mode get 查询失败时不得把 wait 降级值伪装成数据库权威值；\n- Supervisor 应识别 DB 控制面失效并进入明确故障状态或停止，不应保持 running/starting 并继续驱动 AI。\n\n## 实际\n- 2026-07-20 11:06:20Z：db-daemon.log 记录 all tables ensured、listening on /tmp/freely-db-80d307e1394435e3.sock；启动入口记录 DB ready PID 51801。\n- 11:06:31Z：workcell-state.env 为 desired=running、supervisor=up、ai=down、reason=starting；daemon status 为 running；task-mode get 权威返回 auto。\n- 约 13 秒后 task-mode get 返回 task_mode: wait 且退出码为 0，同时错误为 DB query failed after 3 retries (freely-db daemon not ready or crashed)。\n- db-daemon.log 没有对应 daemon stopped 或异常 traceback；PID 51801 已消失，socket 无监听者；freely-db-cli 多次收到 ConnectionRefusedError: [Errno 61] Connection refused。\n- Supervisor PID 52333、manager_watchdog PID 53648、interruption_dispatcher PID 53565 仍存活；随后 daemon status 仅输出 control_plane: daemon 并退出 1。\n- 相同链路在 10:47、10:52、11:02、11:06 四次启动批次均出现 DB 查询失败/WAIT 降级；11:01 和 11:07 的正式 daemon stop 才最终收敛，且需要 forced hard-kill fallback 修复 Supervisor。\n\n## 责任边界\n不主张 task-mode auto 被合法迁移为 wait，也不主张启动参数未传递。启动后的成功查询已证明 auto 被写入并可读取；缺陷位于 DB daemon 存活/监控/故障投影链路，以及查询失败仍返回成功并输出 wait 的语义。\n\n## 非重复依据\n- raw-20260714T021808Z / issue #3900 处理 daemon start 的 task-mode 参数未贯穿、listen fallback 和 AI_MODE；本复现中 auto 已成功写库并被权威读取。\n- raw-MIGRATED-wait-restart-fix 处理 wait 模式跳过 AI restart；本复现发生在 DB daemon 消失后仍以 running/starting 运行。\n- raw-20260717T203109Z / issue #3983 处理 wt-close gate 输入与 DB 缺席韧性，不覆盖运行中 DB daemon 无声退出与 task-mode 查询降级。\n\n## 证据\n.freely/run/db-daemon.log\n.freely/logs/daemon-launch.log\n.freely/logs/lifecycle-trace.log\n.freely/run/workcell-state.env\ndocs/system/workspace/scripts/runtime/freely\ndocs/system/workspace/scripts/runtime/freely_db_manager.py\n\n复现结束后已执行正式 daemon stop，workcell-state.env 收敛为 stopped/Supervisor down/AI down。
