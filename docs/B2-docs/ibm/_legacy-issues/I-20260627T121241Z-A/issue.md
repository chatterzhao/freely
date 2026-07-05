- issue_id: I-20260627T121241Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260627T121241Z-A
- source_candidate: docs/B1-docs/raw-20260627T121248Z41Z/candidates.md#C-20260627T121241Z-A
- source_raw: raw-20260627T121248Z41Z
- verification_artifact_dir: docs/B2-docs/scan-agent-id-fix/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260627T121241Z-A/issue.md
- pre_tests_path: docs/B2-docs/scan-agent-id-fix/verification/pre-tests.md
- title: scan Cat 3 agent-id.env 路径修复

# I-20260627T121241Z-A: scan agent-id.env 路径修复

- source_candidate: docs/B1-docs/raw-20260627T121248Z41Z/candidates.md#C-20260627T121241Z-A
- verification_artifact_dir: docs/B2-docs/scan-agent-id-fix/code-reviews

## 实现
- agent-id.env 路径: wt_path/.freely/run/ → project/.freely/
- 解析格式: AGENT_ID= → =分割取[-1]
- sessions 查询: role=? → (role=? OR role=?) 兼容双格式
