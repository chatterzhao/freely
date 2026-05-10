# Candidates

## C-20260510T0112Z-A: raw issue 正文注入治理提醒

- candidate_format_version: v2
- title: issue-sync 同步时为 raw issue 注入 wt-create 工位绑定提醒
- status: promoted
- decision_reason: 当前 raw issue 正文没有 governance 提示，消费者容易在错误工位实现
- promoted_issue_path: docs/issues/I-20260510T0112Z-A/issue.md
- milestone: M-20260510T0112Z-A
- next_action: B2_IBM → dev-loop → merge
- acceptance_criteria:
  - issue-sync _issue_body 对 kind=raw 注入治理提醒
  - 提醒包含 raw-key，指导 wt-create 使用
  - 不影响非 raw 类型 issue
