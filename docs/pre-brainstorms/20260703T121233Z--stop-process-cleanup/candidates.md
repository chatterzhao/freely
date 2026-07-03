---
candidate_id: C-20260703T121233Z-A
status: absorbed
absorbed_into: I-20260703T121233Z-A
source_raw: raw-20260703T121233Z
milestone: M-20260703T121233Z-A
---

## C-20260703T121233Z-A: 修复进程清理 + bridge 误重启

- status: absorbed
absorbed_into: I-20260703T121233Z-A
- decision_reason: |
  三个修复属同一边界——进程生命周期管理：
  1. stop 用进程组杀代替逐 PID 杀
  2. sse-watchdog 启动前检查已有实例
  3. bridge binary 比较归一化（存短名，启动用全路径）
- acceptance_criteria:
  - freely stop 后无遗留进程（watchdog_sse、sse-watchdog、a2a_server、opencode）
  - 重启 daemon 后只有一个 sse-watchdog.sh 实例
  - ACP bridge 不再每个 cycle 重启（不再有 "binary changed" 日志）
- promoted_issue_id: I-20260703T121233Z-A
- milestone: M-20260703T121233Z-A
