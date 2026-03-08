# Pre-Tests: state-sync-and-session-evidence-governance

1. `phase_state=in_ibm` 的 committed issue 不要求强行创建 `progress`。
2. `phase_state=in_dev` 时，必须同时能找到 `progress`。
3. candidate 晋升为 milestone-owned issue 时，`promoted_issue_path` 与 milestone `issue_path` 一致。
4. `session_refs` 至少包含 `tool/session_id/jsonl_path/role`。
