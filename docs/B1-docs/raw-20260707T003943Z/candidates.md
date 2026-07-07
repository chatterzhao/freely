---
candidate_id: C-20260707T003943Z-A
status: absorbed
source_raw: raw-20260707T003943Z
created_at: 2026-07-07
milestone: M-20260707T003943Z-A
---

## C-20260707T003943Z-A: Gitee assignee API 修复

- candidate_format_version: v2
- title: fix — platform-adapter.py Gitee assignee API 调用兼容
- status: absorbed
- decision_reason: Option B — Gitee 路径改用 subprocess.run 直接调用 gitee-issue.py CLI 子命令
- next_action: B2_IBM 物化 I-* issue → dev 完成实现 → pr → merge
- revisit_trigger: gitee-issue.py CLI 接口变更时需要检查
- acceptance_criteria:
  - get_assignees(Gitee) 使用 subprocess.run 调用 gitee-issue.py get
  - set_assignee(Gitee) 使用 subprocess.run 调用 gitee-issue.py update --assignee
  - pull_raw_issue 区分 "claimed by others"(fatal) 和 "claim failed"(warning)
  - freely wt-create --raw-key 对 Gitee issue 能够成功创建工位
- promotion_gate: platform-adapter.py 修改完成，wt-create 对 Gitee issue 正常工作
- open_questions: []
- acceptance_reviews: []
- promoted_issue_id: I-20260707T003943Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260707T003943Z/issues/I-20260707T003943Z-A.md
- milestone: M-20260707T003943Z-A
- session_refs: []
