# Brainstorm: scan_state 输出到 Manager prompt

## Discovery
- raw issue: raw-20260623T162243Z (GitHub #3393)
- 上游: #3381 问题 4 — Manager 看不到 scan_state

## Research
- scan_state 数据更新已全部实现（_set_scan_states / wt-create / wt-close）
- 唯一缺失：append_task_source_patrol_seed_if_needed 不输出 scan_state
- 改动：8 行，只在 freely 脚本

## Decision
- 输出 scan_state + scan_state_worktree
- scan_state=working + 无活跃 Worker → 死 Worker 警告
