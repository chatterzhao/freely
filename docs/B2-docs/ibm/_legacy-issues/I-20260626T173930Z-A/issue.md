- issue_id: I-20260626T173930Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260626T173930Z-A
- source_raw: raw-20260626T173930Z30Z
- source_candidate: docs/B1-docs/raw-20260626T173930Z30Z/candidates.md#C-20260626T173930Z-A
- verification_artifact_dir: docs/B2-docs/slot-assemble-unify/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260626T173930Z-A/issue.md
- title: ai_cli_tool_with_auth_assemble + slot recovery
- pre_tests_path: docs/B2-docs/slot-assemble-unify/verification/pre-tests.md

# I-20260626T173930Z-A: ai_cli_tool_with_auth_assemble + slot recovery

- source_raw: raw-20260626T173930Z30Z
- source_candidate: docs/B1-docs/raw-20260626T173930Z30Z/candidates.md#C-20260626T173930Z-A
- pre_tests_path: docs/B2-docs/slot-assemble-unify/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/slot-assemble-unify/code-reviews

## 实现

ai_cli_tool_with_auth_assemble(type, slot) 统一 _assemble_slot_test_command 和 _bridge_env_for_registered_tool。
slot recovery 通过 _test_slot 实测候选 slot（30s 超时），成功则更新 agent-table.toml。

## 补充修复 (2026-06-27)

tool-registry.toml:
- cline test_command: `--yolo` → `--auto-approve true`（--yolo 已废弃）
- claude test_command: 移除 `--max-tokens 50`（当前版本不支持）
