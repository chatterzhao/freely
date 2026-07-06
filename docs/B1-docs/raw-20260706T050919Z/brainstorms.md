---
b1_id: B1-20260706T050919Z
phase_state: completed
source_raw: raw-20260706T050919Z
produced_candidate: C-20260706T050919Z-A
---
# B1: 门禁 diff-scope 改造

## Problem
governance-merge-gate 的 build_issue_index() 和 _validate_raw_issue() 做全仓扫描，
历史文件误伤当前 PR，导致不得不用 --no-verify/--admin 绕过。

## Fix
- build_issue_index(changed_paths): 文件系统 fallback 只在 diff 内扫描
- _validate_raw_issue(issues_index): absorbed_into 查找优先用索引，删除全仓 os.walk

## Candidate
- candidate_id: C-20260706T050919Z-A
- status: promoted
- milestone: M-20260706T050919Z-A
