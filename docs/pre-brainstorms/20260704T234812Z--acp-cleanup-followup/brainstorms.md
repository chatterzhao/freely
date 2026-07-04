---
b1_id: B1-20260704T234812Z
phase_state: completed
source_raw: raw-20260704T234812Z
source_url: https://github.com/chatterzhao/freely/issues/3732
produced_candidate: C-20260704T234812Z-A
created_at: 2026-07-04
---

# B1_IBM: #3731 ACP cleanup 遗漏修复 + hook 提示改进

## Input
- raw-20260704T234812Z (GitHub #3732)
- 前置: raw-20260704T064539Z (#3728 session-lifecycle-unify) + raw-20260704T080808Z (#3729 multi-bridge-per-tool)
- 关联: raw-20260704T164337Z (#3730/#3731 acp cleanup)

## Problem

#3731 声称完成了 4 项 cleanup 工作，但实际执行有遗漏和表面化问题：

1. **freely_db_manager.py**: `h_aw_upsert_only` 中 `if slot_val:` 缩进多一级，IndentationError
2. **acp-bridge.py CLI**: 签名有 `base_tool` 参数但 argparse 无 `--base-tool`，所有调用传 `""`
3. **_ensure_acp_bridge_running**: `pid_file`、`health_check`、`bridge start` 不传 `$base_tool`
4. **bash/Python 路径不一致**: bash 无条件加 `-` 分隔符，Python 条件加
5. **5 处硬编码 socket 路径**: 未使用 `_acp_bridge_socket` 函数
6. **3 个 docstring 未闭合**: `watchdog_sse.py` 中 `_handle_needs_*`
7. **3 处 agent_assign 裸调用**: 遗漏 slot 参数
8. **monitor-ai-acp.sh**: `_bridge_*` 调用不传 `base_tool`
9. **hook 提示**: 未告知 `freely feedback` + `freely wt-create` + skill

## Brainstorm

### 方案: 逐项修复（唯一方案，直接执行）

所有 9 个问题都是机械性 bug——语法错误、参数遗漏、路径不一致。无架构决策分歧。

| # | 文件 | 改动 |
|---|------|------|
| 1 | `freely_db_manager.py` | 修正 `h_aw_upsert_only` 缩进 |
| 2 | `acp-bridge.py` | 添加 `--base-tool` CLI 参数；`cmd_start/stop/status` 穿透；`AcpBridge.__init__` 接受 `base_tool` |
| 3 | `freely` | `_ensure_acp_bridge_running`: pid_file 传 `$base_tool`；health_check 传 `$base_tool`；bridge start 传 `--base-tool` |
| 4 | `freely` + `monitor-ai-acp.sh` | `_acp_bridge_pid_file`、`_acp_bridge_socket`、`_bridge_pid_file`、`_bridge_socket` 改为 conditional `-{base_tool}` suffix |
| 5 | `freely` | 5 处硬编码替换为 `$(_acp_bridge_socket "$project")` |
| 6 | `watchdog_sse.py` | 3 个 docstring 补全 `"""`；`_acp_rpc` 加 `base_tool` 参数 |
| 7 | `freely` | 3 处 `agent_assign` → `acp_session_register` |
| 8 | `monitor-ai-acp.sh` | `_bridge_pid_file`/`_bridge_socket` 传 `$base_tool`；bridge start 传 `--base-tool` |
| 9 | `pre-commit.sh` | 错误提示改为：`freely feedback` 命令 + `freely wt-create` 命令 + skill `freely-workflow-guarded-execution` |

## Decision: 逐项修复

全部机械性 bug，直接 fix。共 6 个文件，~70 行变更。

## Candidate
- candidate_id: C-20260704T234812Z-A
- status: promoted
- milestone: M-20260704T234812Z-A
