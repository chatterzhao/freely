- issue_id: I-20260626T171144Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260626T171144Z-A
- source_raw: raw-20260626T171144Z44Z
- source_candidate: docs/B1-docs/raw-20260626T171144Z44Z/candidates.md#C-20260626T171144Z-A
- verification_artifact_dir: docs/B2-docs/agent-table-slot-pin/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260626T171144ZI-20260626T171144Z-A/issue.md
- title: agent-table slot pinning at startup
- pre_tests_path: docs/B2-docs/agent-table-slot-pin/verification/pre-tests.md
# I-20260626T171144Z-A: agent-table slot pinning at startup
_init_agent_table_slot_pin: daemon start 时将 agent-table 分配的 slot 写入 current-slot 文件
