---
b1_id: B1-20260717T060903Z
phase_state: completed
source_raw: raw-20260717T060903Z
produced_candidate: C-20260717T060903Z-A
created_at: 2026-07-17
---

# B1_IBM: acp_bridge pid 文件族 glob 展开与广播清理误伤

## Input
raw-20260717T041435Z 附带段正式立案。两处缺陷代码坐实（见 raw 正文 file:line）。

## Problem
1. `runtime_pid_file_for_role` acp_bridge 分支返回未引 glob：多 bridge 并存时 printf 展开多行，`clear_stale_runtime_pid_file_if_invalid` 的 `cat "$pid_file"` 拿多行路径失败 → pid 空 → 走"空 pid 清理"分支 `rm -f "$pid_file"`（多行路径 rm 也失败）→ 返回 0 伪装已清理，acp_bridge 角色的 self-heal 实际失效
2. 广播清理：单工具 stale 触发全族 `rm -f <hash>*.sock <hash>*.pid` → 其他工具活 bridge 文件被删、进程失联（ensure 视角=消失 → 重生；进程本体成孤儿靠 idle 自灭）

## Brainstorm
### Option A：runtime_pid_file_for_role 返回首个匹配文件
- 反对：多 bridge 时只 self-heal 一个，其余漏检
### Option B：self-heal 对 acp_bridge 逐文件枚举 + 清理 per-tool 化（选定）
- `startup_self_heal_clear_stale_pid_files_if_needed` 对 acp_bridge 特化：遍历 `<hash>-*.pid` 每个独立 `clear_stale_runtime_pid_file_if_invalid_single`（新小函数收编现逻辑，pid_file 传实参）；acp_bridge 清理块从文件名提取 `<tool>` 后缀，仅删 `<hash>-<tool>.sock/.pid/.pid.bin/.pid.tool`
- `runtime_pid_file_for_role` acp_bridge 分支保留兼容：返回首个存在的文件（引号安全），并注释指向枚举入口
### Option C：pid 文件族收进 SQLite
- 改动面大，另案

## Decision: Option B

## 边界
- 只改 self-heal 枚举与清理粒度；不动 ensure/bridge 本体（raw-20260717T004654Z 已修面不重叠）

## Candidate
- candidate_id: C-20260717T060903Z-A
- status: promoted
- milestone: M-20260717T060903Z-A
