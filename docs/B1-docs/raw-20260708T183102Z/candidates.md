---
candidate_id: C-20260708T183102Z-A
status: absorbed
source_raw: raw-20260708T183102Z
milestone: M-20260708T183102Z-A
---
## C-20260708T183102Z-A: pr-merge path + wt-close issue-sync + worktree resolution

- candidate_format_version: v2
- title: 修复 pr-merge-guarded 路径、worktree 解析、wt-close 冗余 issue-sync
- status: absorbed
- milestone: `M-20260708T183102Z-A`
- decision_reason: 6 处修复分布在 2 个文件，核心是修复 _sync_issues_changed_in_merge 的读写路径不一致 + wt-close 的冗余 close 和引导逻辑
- next_action: 改 pr-merge-guarded 2 处 + wt-close 4 处
- revisit_trigger: N/A
- acceptance_criteria:
  - pr-merge-guarded _sync_issues_changed_in_merge 从 worktree 读 issue.md
  - pr-merge-guarded worktree 解析用 raw_key
  - wt-close 正常路径检测 platform_state: closed → 跳过 issue-sync
  - wt-close 检测到 issue-sync diff → 提示 stash + 正规化，不引导 force
  - wt-close 去掉 updated_at 时间戳
  - wt-close 吸收 I-* 路径不写 develop
- promotion_gate: 6 处修改完成 + pr-merge 能正确 sync + wt-close 不再冗余写入
- open_questions: []
- promoted_issue_id: I-20260708T183102Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260708T183102Z/issues/I-20260708T183102Z-A.md
