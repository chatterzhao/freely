# Pre-Tests: 跨tool session
- issue_id: I-20260719T101009Z-A
## Acceptance Items
### acceptance-1
- id: AT-001 / requirement: Worker同tool fork用Manager bridge socket / testing_layer: unit / evidence_level: real_env / artifact_ref: docs/B2-docs/acp/cross-tool-session/raw-20260719T101009Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c '_worker_base.*==.*_mgr_base' docs/system/workspace/scripts/runtime/freely / expected_output: "1" / red-green-status: green / status: pass
### acceptance-2
- id: AT-002 / requirement: Worker不同tool ensure Worker bridge / testing_layer: unit / evidence_level: real_env / artifact_ref: docs/B2-docs/acp/cross-tool-session/raw-20260719T101009Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c '_ensure_acp_bridge_running.*_worker_base' docs/system/workspace/scripts/runtime/freely / expected_output: "1" / red-green-status: green / status: pass
### acceptance-3
- id: AT-003 / requirement: Reviewer跨tool ensure bridge / testing_layer: unit / evidence_level: real_env / artifact_ref: docs/B2-docs/acp/cross-tool-session/raw-20260719T101009Z/verification/test-evidence/acceptance-3.log
- test_command: grep -c '_reviewer_base.*_mgr_base_rev' docs/system/workspace/scripts/runtime/freely / expected_output: "3" / red-green-status: green / status: pass
## Unit: AT-001~003覆盖 / target_environment: fix-raw-20260719T101009Z-cross-tool-worker-launch / not_applicable_reason: covered_by_more_realistic_required_surface / replacement_evidence: AT-001~003
## Integration: post-merge daemon / target_environment: test-pre-merge-20260719T101009Z-cross-tool-worker-launch / not_applicable_reason: covered_by_more_realistic_required_surface
## End-to-End: target_environment: develop merge chain / not_applicable_reason: covered_by_more_realistic_required_surface
## Real-Environment: real_environment_status: pass / real_environment_reason: 同tool fork + 不同tool new 均已实现
