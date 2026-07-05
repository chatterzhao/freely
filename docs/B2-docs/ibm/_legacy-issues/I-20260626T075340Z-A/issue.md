- issue_id: I-20260626T075340Z-A
- kind: fix
- phase_state: completed
- source_candidate: docs/B1-docs/raw-20260626T075340Z/candidates.md#C-20260626T075340Z-A
- source_raw: raw-20260626T075340Z
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260626T075340Z-A/issue.md
- verification_artifact_dir: docs/epics/cline-registry-fix/verification
- pre_tests_path: docs/epics/cline-registry-fix/verification/pre-tests.md
- title: cline tool-registry.toml slot/session fix + bridge_config_env CLI flag mode

# I-20260626T075340Z-A: cline registry fix + bridge_config_env dual mode

## 实现

- [cline.slot] 修正 discovery/alias_key/config_file/is_dir/bridge_config_env
- [cline.session] 修正 id_format/extract_regex
- bridge_config_env 双模式：--* 前缀识别 CLI flag 模式
- _slot_type 硬编码 bug 修复
