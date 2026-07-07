---
candidate_id: C-20260707T134101Z-A
status: absorbed
source_raw: raw-20260707T134101Z
milestone: M-20260707T134101Z-A
---
## C-20260707T134101Z-A: 平台硬编码清理
- status: absorbed
- decision_reason: 消除所有硬编码平台调用 + issue-sync 自动同步 test worktree
- promoted_issue_id: I-20260707T134101Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260707T134101Z/issues/I-20260707T134101Z-A.md
- acceptance_criteria:
  - pr-merge-guarded issue-sync 后自动 git merge 到 test worktree
  - pr-merge-guarded _sync_prs_across_platforms 遍历所有 remote 而非只 gitee
  - pr-review-guarded 不硬编码 repo 名
  - wt-close 不硬编码 repo 名
  - 所有 git push 用 `all` remote（双平台）
