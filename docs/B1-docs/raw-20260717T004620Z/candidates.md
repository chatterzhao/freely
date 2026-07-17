---
candidate_id: C-20260717T004620Z-A
status: promoted
source_raw: raw-20260717T004620Z
created_at: 2026-07-16
milestone: M-20260717T004620Z-A
---

# Candidates

## C-20260717T004620Z-A: supervisor 生死判定一体收口（heartbeat 宽限 + teardown 语义 + storm 观测）

- candidate_format_version: v2
- title: ensure-manager 秒杀新生 supervisor 引发 restart storm 的一体修复
- status: promoted
- decision_reason: C1（heartbeat stale 分支无新生宽限）、C2（裸 TERM 被 daemon 忽略→误信已杀→双 supervisor）、C4（storm 检测只计 AI 周期，supervisor 死亡零检出）同属生死判定域的输入/动作/观测三面，拆开修留病理闭环；一体修改动收敛在 runtime/freely 4 个函数+1 处代码块搬移。详见 brainstorms.md Decision: Option B
- next_action: B2_IBM 物化 I-* issue + prd/pre-tests/tasks → RED → dev → GREEN → PR
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - C1a: 存在 stale heartbeat 文件（mtime 早于 sup_pid_file）时，ensure_manager_once 对新生 supervisor（启动 < 宽限期）不发出 kill，不重拉 daemon
  - C1b: heartbeat touch 子进程在 supervisor_started 后 ≤3s 开始更新 heartbeat（裸奔窗口从 10-15s 压缩到 <3s）
  - C2a: heartbeat 判死路径使用带验证的 teardown（terminate→确认进程退出→清 pid/identity），不再使用会被 daemon 忽略的裸 TERM
  - C2b: 被判死 supervisor 进程仍存活时，ensure-manager 不启动第二个 daemon（同一时刻 daemon-run 进程数恒 ≤1）
  - C4a: supervisor_cleanup（L090/L092 路径）计入 restart storm window；窗口内 cleanup 次数达阈值时 restart_storm_signal_* 置位并产生 escalation 记录
  - C4b: PROCESS_CHURN_PEAK 默认值落在计数口径可达域；RESTART_STORM_COUNT 函数后备值与 config init 一致
  - 回归: 正常启动链 A-L001→L010→L020→L021→L022→L040 在修复后完整走通（task_mode=auto）
- promotion_gate: 根因证据链完整（runtime-events/lifecycle-trace/受控实验三源交叉）；scope 与相邻 lane（raw-20260717T004654Z bridge、raw-20260717T004721Z sse、raw-20260716T114802Z stall）零重叠；全部 acceptance_criteria 可转化为可执行 pre-tests
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-subagent-acceptance-review
  - mode: subagent
  - summary: 审查 C1/C2/C4 同 lane 合修的边界正当性、acceptance_criteria 可测性、与相邻三条 lane 的 scope 隔离；确认证据链（事件日志时序 + 两次受控重启复现）支撑根因结论
  - verdict: pass
- promoted_issue_id: I-20260717T004620Z-A
- promoted_issue_path: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/issues/I-20260717T004620Z-A.md
- milestone: M-20260717T004620Z-A
- session_refs: []
