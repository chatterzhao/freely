---
candidate_id: C-20260710T002224Z-A
status: absorbed
source_raw: raw-20260710T002224Z
absorbed_into: I-20260710T002224Z-A
milestone: M-20260710T002224Z-A
---
## C-20260710T002224Z-A: pre-scan-fix.sh FREELY_SKIP_IBM_GATE fix
- status: absorbed
- decision_reason: --skip-ibm 参数不存在于任何命令，需替换为 FREELY_SKIP_IBM_GATE 环境变量
- acceptance_criteria: 所有命令参数正确，bash -n 通过
- promoted_issue_id: I-20260710T002224Z-A
- promoted_issue_path: docs/B2-docs/runtime/scan/raw-20260710T002224Z/issues/I-20260710T002224Z-A.md
