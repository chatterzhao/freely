# Candidates

## C-20260517T083030Z-A: legacy issue

- candidate_format_version: v2
- title: supervisor crash 对 bash rc=0 的假阳性检测
- status: needs_research
- decision_reason: bash 以 rc=0（成功）退出被判定为 crash，需先研究 supervisor crash 检测逻辑才能确定修复方案
- next_action: 研究 supervisor 源码中 crash 检测的代码路径，确定 rc=0 是否应被过滤
- revisit_trigger: 完成 supervisor crash 检测逻辑研究后重新评估
- acceptance_criteria:
  - 明确 supervisor crash 检测的代码位置和判断逻辑
  - 确认 rc=0 类退出是否为系统性假阳性
  - 提出具体的修复方案（至少已知改什么文件、改什么判断条件）
  - 评估修正范围：仅过滤 rc=0 还是需要更全面的退出码策略
- promotion_gate: supervisor crash 检测逻辑研究完成，修复方案明确且经初步评审判定安全
- open_questions:
  - supervisor 的 crash 检测代码在哪里？
  - bash 退出 rc=0 是正常命令完成还是预期外行为？
  - 当前假阳性比例如何？是否值得优先修复？
  - 过滤 rc=0 后是否会影响真正的 crash 检测？
- acceptance_reviews: []
- promoted_issue_path: ''
- milestone: M-20260517T083030Z-A
- session_refs:
  - tool: cc-ds-flash-auto
  - session_id: raw-20260517T083030Z
  - jsonl_path: unavailable://platform-session-not-local
  - role: worker
