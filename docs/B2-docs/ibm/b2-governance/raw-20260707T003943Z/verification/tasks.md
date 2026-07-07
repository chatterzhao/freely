# tasks: Gitee assignee API 修复

- issue_id: I-20260707T003943Z-A

## Task 1: 修复 get_assignees(Gitee)
- [x] 改用 subprocess.run + gitee-issue.py get
- 验证: AT-001

## Task 2: 修复 set_assignee(Gitee)
- [x] 改用 subprocess.run + gitee-issue.py update --assignee
- 验证: AT-002

## Task 3: pull_raw_issue 错误分级
- [x] 区分 fatal (already assigned) 和 warning (claim failed)
- 验证: AT-003

## Task 4: 端到端验证
- [x] wt-create Gitee issue 成功创建工位
- 验证: 实际运行通过
