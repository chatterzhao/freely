# Candidates

## C-20260517T083200Z-A: supervisor crash — investigate rc=0 crash detection

- candidate_format_version: v2
- title: 调查 supervisor 将 rc=0 进程终止判定为 crash 的根因
- status: needs_research
- decision_reason: `raw-20260517T083200Z` 报告 supervisor crash 但 bash exit code 为 0——clean exit 被误判为 crash，需先定位根因再决定修复范围
- next_action: 读取 supervisor 与 ACP bridge 源码，确认 crash 检测逻辑中 exit code 的判定位置；若为 bug，产出正式 issue 进入修复；若为预期行为，记录文档并降级日志
- revisit_trigger: 当 supervisor 和 ACP bridge 的 crash/exit_code 判定逻辑已被阅读和理解，根因收敛后重新评估
- acceptance_criteria:
  - 已定位 supervisor crash 判定中 rc=0 被误报的具体代码位置
  - 已确认是 supervisor 判定 bug、ACP bridge exit code 透传缺陷、还是预期行为
  - 若是预期行为：记录文档说明原因，提出日志降级建议
  - 若是 bug：产出修复路径，决定修复范围（supervisor / ACP bridge / 两者）
- promotion_gate: 根因收敛，确认修复范围，完成至少一次 independent review
- open_questions:
  - supervisor 的 crash 判定是否同时检查 exit code 和进程断连事件？
  - ACP bridge 是否在底层进程 crash 时仍返回 rc=0？
  - resume 会话是否引入了特殊的退出路径/误报条件？
- acceptance_reviews: []
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260517T083200Z-A
- session_refs: []
