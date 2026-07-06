---
candidate_id: C-20260706T050919Z-A
status: promoted
source_raw: raw-20260706T050919Z
milestone: M-20260706T050919Z-A
---
## C-20260706T050919Z-A: 门禁 diff-scope 改造
- candidate_format_version: v2
- title: 门禁 diff-scope 改造
- status: promoted
- decision_reason: 两处改动消灭全仓扫描，历史文件不误伤当前 PR
- acceptance_criteria:
  - --range develop..HEAD 不报历史文件错误
  - diff 内的文件错误仍正常拦截
- promoted_issue_id: I-20260706T050919Z-A
- milestone: M-20260706T050919Z-A
