- issue_id: I-20260626T171144Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260626T171144Z-A
- source_raw: raw-20260626T171144Z
- source_candidate: docs/pre-brainstorms/20260626T171144Z--agent-table-slot-pin/candidates.md#C-20260626T171144Z-A
- verification_artifact_dir: docs/epics/agent-table-slot-pin/code-reviews
- canonical_issue_path: docs/issues/I-20260626T171144Z-A/issue.md
- title: agent-table slot pinning at startup
- pre_tests_path: docs/epics/agent-table-slot-pin/verification/pre-tests.md
# I-20260626T171144Z-A: agent-table slot pinning at startup
_init_agent_table_slot_pin: daemon start 时将 agent-table 分配的 slot 写入 current-slot 文件
