---
candidate_id: C-20261125T094413Z-A
status: promoted
source_raw: raw-20261125T094413Z
created_at: 2026-11-25
milestone: M-20261125T094413Z-A
---

## C-20261125T094413Z-A: 证据沿袭（语义影响判据）
- candidate_format_version: v2
- title: 元数据等价提交免重测 + test-gate 证据沿袭
- status: promoted
- promoted_issue_path: docs/B2-docs/gate/test-evidence-equivalence/raw-20261125T094413Z/issues/I-20261125T094413Z-A.md
- milestone: M-20261125T094413Z-A
- decision_reason: 用户项目里 issue 字段非测试对象可免重测；自举里是被测对象必须重测——判据必须是语义依赖而非路径一刀切
- acceptance_criteria: attest-meta 沿袭非敏感 diff；敏感 diff/硬排除路径拒绝；validate 三态
- promotion_gate: B0 判定为设计不完整
