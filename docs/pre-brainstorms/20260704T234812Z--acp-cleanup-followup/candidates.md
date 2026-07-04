---
candidate_id: C-20260704T234812Z-A
status: promoted
source_raw: raw-20260704T234812Z
created_at: 2026-07-04
milestone: M-20260704T234812Z-A
---

## C-20260704T234812Z-A: #3731 ACP cleanup 遗漏修复 + hook 提示改进

- candidate_format_version: v2
- title: 修复 #3731 清理遗漏的 base_tool plumbing、语法错误、硬编码路径、hook 提示
- status: promoted
- decision_reason: |
  9 个问题全部为机械性 bug，无架构决策分歧。逐项修复即可。
  #3728/#3729 重构时 base_tool 参数已预留于所有签名中，本期只是补齐掉落的调用链。
- next_action: B2 设计 → dev 实现 → merge
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - freely_db_manager.py: h_aw_upsert_only 缩进正确，Python 语法通过
  - acp-bridge.py: CLI 有 --base-tool 参数，start/stop/status 穿透到 _pid_file/_socket_path
  - freely: _ensure_acp_bridge_running 所有 base_tool 参数传递到位；5 处硬编码路径替换
  - freely + monitor-ai-acp.sh: bash socket/pid 函数与 Python conditional suffix 一致
  - watchdog_sse.py: 3 个 docstring 闭合，_acp_rpc 签名含 base_tool
  - freely: agent_assign 裸调用迁移到 acp_session_register
  - monitor-ai-acp.sh: _bridge_pid_file/_bridge_socket 调用传 base_tool
  - pre-commit.sh: 拦截消息明确告知 `freely feedback` + `freely wt-create` + skill `freely-workflow-guarded-execution`
- promotion_gate: 所有文件语法检查通过（Python AST + bash -n），代码静态审查通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: plan-subagent
  - summary: 审查 9 项修复是否完整覆盖 #3731 遗漏的所有问题
  - verdict: pass
- promoted_issue_id: I-20260704T234812Z-A
- promoted_issue_path: docs/epics/agent-acp/acp-cleanup-loosened/raw-20260704T234812Z/issues/I-20260704T234812Z-A.md
- milestone: M-20260704T234812Z-A
- session_refs: []
