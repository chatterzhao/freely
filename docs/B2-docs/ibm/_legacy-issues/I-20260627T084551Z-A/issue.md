- issue_id: I-20260627T084551Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260627T084551Z-A
- source_candidate: docs/B1-docs/raw-20260627T084551Z/candidates.md#C-20260627T084551Z-A
- source_raw: raw-20260627T084551Z
- verification_artifact_dir: docs/epics/acp-session-fork/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260627T084551Z-A/issue.md
- pre_tests_path: docs/B2-docs/acp-session-fork/verification/pre-tests.md
- title: run-acp-prompt.py fork 改用 session/fork

# I-20260627T084551Z-A: ACP session/fork

- source_candidate: docs/B1-docs/raw-20260627T084551Z/candidates.md#C-20260627T084551Z-A
- verification_artifact_dir: docs/epics/acp-session-fork/code-reviews

## 实现
- run-acp-prompt.py: fork 路径 try session/fork → 降级 session/new
- ensure-codex-acp: .json5 → .toml
