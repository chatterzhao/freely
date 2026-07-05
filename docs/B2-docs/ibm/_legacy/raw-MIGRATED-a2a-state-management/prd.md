# PRD: A2A 状态管理全量修复

## Goal
修复 A2A task state 修改点的 14 项问题，覆盖 stop 行为、重启恢复、审计 bug。

## Scope
5 文件，~100 行改动。
- `freely`: A0 + B1-B4
- `a2a_server.py`: A1-A3 + C5
- `a2a_task.py`: C2 + C3
- `freely_db_manager.py`: C4 + C6
- `wt-close`: C1

## Tasks
详见 tasks.md。14 项分 4 组：A 组（架构）+ B 组（恢复）+ C 组（审计 bug）。

## Dev-Loop Handoff
- 实现顺序：C1→C2→C3-C6→A0→A1-A3→B1-B4
- C 组优先（运行时 bug）
- A0 最后（需要配合 _restore_tasks 的完整 A1-A3+B1-B4）
