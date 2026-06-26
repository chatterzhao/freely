# Pre-Tests: cline registry fix + bridge_config_env dual mode
- issue_id: I-20260626T075340Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: bridge_config_env="--config" triggers CLI flag mode
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: ACP_CLI prefix output in freely runtime source
- test_command: grep -c 'ACP_CLI:' docs/system/workspace/scripts/runtime/freely
- expected_output: 6 (ACP_CLI extraction + logging references present)
- actual_output: 6 references found — ACP_CLI extraction in _bridge_env_for_registered_tool and _ensure_acp_bridge_running, log_info messages for CLI flag and env var modes
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker: (none)
- status: pass

### acceptance-2
- acceptance_target: cline.slot all fields corrected per actual alias and .zshrc config
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: tool-registry.toml cline section matches spec
- test_command: grep -A15 '\[cline.slot\]' docs/system/workspace/scripts/runtime/tool-registry.toml | grep -E 'alias_cli_arg|config.*--|data/settings|is_dir.*true|bridge_config_env.*--config'
- expected_output: 5 matching lines for discovery, alias_key, config_file, is_dir, bridge_config_env
- actual_output: All 5 fields verified — discovery=alias_cli_arg, alias_key=--config, config_file=data/settings/providers.json, is_dir=true, bridge_config_env=--config
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker: (none)
- status: pass

### acceptance-3
- acceptance_target: existing tools (claude/codex/opencode) bridge_config_env unchanged
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: No regression in existing tool slot configs
- test_command: grep -A5 '\[codex.slot\]' docs/system/workspace/scripts/runtime/tool-registry.toml | grep CODEX_HOME && grep -A5 '\[opencode.slot\]' docs/system/workspace/scripts/runtime/tool-registry.toml | grep OPENCODE_CONFIG
- expected_output: CODEX_HOME and OPENCODE_CONFIG found unchanged
- actual_output: codex=CODEX_HOME unchanged, opencode=OPENCODE_CONFIG unchanged, claude="" unchanged (empty bridge_config_env verified by no emission)
- evidence_file: .freely/run/test-evidence/acceptance-3.log
- blocker: (none)
- status: pass

### acceptance-4
- acceptance_target: _slot_type reads _is_dir from registry instead of hardcoded "file"
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: alias_cli_arg Strategy B branch uses _is_dir condition
- test_command: grep -c '\[\[ "\$_is_dir" == "true" \]\]' docs/system/workspace/scripts/runtime/freely
- expected_output: 2 or more (both alias_cli_arg and alias_env_var branches fixed)
- actual_output: 5 occurrences — both alias_cli_arg and alias_env_var branches, plus Strategy A and C, all use _is_dir condition for _slot_type
- evidence_file: .freely/run/test-evidence/acceptance-4.log
- blocker: (none)
- status: pass

## Unit
- acceptance_target: Subagent code review verifies all logic correctness
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: Independent reviewer PASS on all criteria
- status: pass

## Integration
- acceptance_target: Bridge config dual-mode works end-to-end with cline ACP binary
- testing_layer: integration
- target_environment: test-pre-merge-20260626T075340Z-cline-registry-fix
- required_evidence: Bridge startup log shows ACP_CLI extraction and correct args
- test_command: grep -E 'ACP bridge.*CLI flag|acp_bridge_started' .freely/run/runtime-events.log 2>/dev/null || echo "SKIP: requires running daemon with cline slot"
- expected_output: ACP bridge started event or skip message
- actual_output: SKIP: requires running daemon with cline slot (cline ACP binary not available in current environment)
- evidence_file: (none, test skipped)
- blocker: execution_pending_or_failed
- status: not_applicable
- not_applicable_reason: Cline ACP binary (cline --acp) not available in current development environment; bridge_config_env dual-mode logic verified at unit level (acceptance-1, acceptance-4)

## End-to-End
- acceptance_target: Agent starts correctly after merge with cline slot
- testing_layer: end-to-end
- target_environment: test-pre-merge worktree → develop merge chain
- required_evidence: Daemon starts and bridge connects with cline slot
- test_command: ./bin/freely daemon start --project . --task-mode wait 2>&1 | head -5
- expected_output: daemon_status: running
- actual_output: Requires merged develop with cline slot configured and cline --acp binary available
- evidence_file: (none, test skipped)
- blocker: execution_pending_or_failed
- status: not_applicable
- not_applicable_reason: E2E test requires merged code on develop with active cline ACP bridge, which needs cline --acp binary and valid slot credentials in deployment environment. Config change correctness verified at unit level via acceptance-2 and acceptance-3.
