---
candidate_id: C-20260707T155021Z-A
status: absorbed
source_raw: raw-20260707T155021Z
milestone: M-20260707T155021Z-A
---
## C-20260707T155021Z-A: review-guidelines 行为测试强化
- status: absorbed
- decision_reason: b2/red/dev/green 各增行为测试检查，杜绝 grep/bash -n 走过场
- promoted_issue_id: I-20260707T155021Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260707T155021Z/issues/I-20260707T155021Z-A.md
- acceptance_criteria:
  - B2: test_command 必须可执行且验证行为
  - RED: actual_RED_output 必须是真实执行结果
  - dev: 代码必须修复 RED 发现的失败
  - GREEN: 禁止 ghost pass，测试必须验证行为正确性
