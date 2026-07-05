# Candidates

## C-20260517T082453Z-A: supervisor bash rc=0 crash — 进程正常退出与 crash 分类歧义

- candidate_format_version: v2
- title: supervisor 进程正常退出 (rc=0) 被误分类为 crash
- status: needs_research
- decision_reason: 监控日志显示 cc-ds-flash-auto (adapter=acp, launch_kind=prompt) 的 bash 进程以 rc=0 正常退出，但被 supervisor 统一标记为 crash。需确认 supervisor 是否应区分正常退出与异常崩溃，以及 set_e_exit_cmd 溯源代码的实际语义
- next_action: 查阅 ACP adapter 退出溯源代码；确认 set_e_exit_cmd 标签生成逻辑；复现场景验证 rc=0 退出是否被其他 adapter 同样误报
- revisit_trigger: auto-loop 重启风暴计数器排除了 rc=0 退出；或 supervisor 日志持续出现 rc=0 crash 标志触发进一步调查
- acceptance_criteria:
  - 确认 set_e_exit_cmd 溯源代码行为与产生条件
  - 确定 supervisor crash 分类规则是否需要全局修复或仅 ACP adapter 修复
  - 产出修复范围与对应治理/实现方案
- promotion_gate: 修复范围明确，有治理/实现方案，且经 acceptance review 通过
- open_questions:
  - set_e_exit_cmd 标签由哪层代码产生？ACP adapter、监控框架还是 bash wrapper？
  - 其他 adapter (stdio, opencode) 是否也有同样的 rc=0 误报？
  - launch_kind=prompt 的一性次任务完成后退出，supervisor 应标记为 "completed" 还是保持为 "crash"？
  - 若需修复，修改面在 supervisor 控制面还是 adapter 退出溯源报告逻辑？
- acceptance_reviews: []
- promoted_issue_path: ""
- milestone: M-20260312-control-surface-runtime-convergence
- session_refs:
  - tool: cc
    session_id: "20260517100656-b45840"
    jsonl_path: "unavailable://cc-session-id-not-exposed"
    role: worker
