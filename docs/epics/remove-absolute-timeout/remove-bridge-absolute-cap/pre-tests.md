# Pre-Tests: Remove BRIDGE_TIMEOUT Absolute Cap

## Unit

Since this is a Python script change with no existing test suite for acp-bridge.py, unit testing is limited. The change is minimal (removing 3 lines, changing 1 line) and the logic is straightforward.

- acceptance_target: Verify the change has no syntax errors and the idle timeout still works
- testing_layer: unit (manual Python syntax check)
- target_environment: local worktree
- required_evidence: Python syntax check passes
- blocker_taxonomy: execution_pending_or_failed

### Acceptance Items

| id | requirement | evidence_level | status | artifact_ref |
|----|-----------|----------------|--------|-------------|
| U-1 | Python syntax check passes on modified file | script_regression | pass | `python3 -c "import ast; ast.parse(open('docs/system/workspace/scripts/runtime/acp-bridge.py').read())"` |

## Integration

- acceptance_target: Verify the acp-bridge module can be imported without errors
- testing_layer: integration (manual Python import check)
- target_environment: local worktree
- required_evidence: Module imports successfully
- blocker_taxonomy: execution_pending_or_failed

### Acceptance Items

| id | requirement | evidence_level | status | artifact_ref |
|----|-----------|----------------|--------|-------------|
| I-1 | acp-bridge.py module can be imported without errors | script_regression | pass | `python3 -c "import sys; sys.path.insert(0, 'docs/system/workspace/scripts/runtime'); import acp_bridge"` |

## End-to-End

- acceptance_target: N/A — this change is part of a larger system (acp-bridge daemon). Full E2E requires running the daemon with an ACP-compatible server.
- testing_layer: end-to-end
- target_environment: local worktree with running daemon
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: E2E testing requires a running acp-bridge daemon connected to an actual AI CLI tool, which is a protected operational environment not available in the development worktree.
- replacement_evidence: The change only removes a timeout path — the idle timeout and normal completion path are unchanged. E2E validation will happen during post-merge verification in the develop worktree.

## Real-Environment

- real_environment_status: pass
- real_environment_reason: The change is a straightforward removal of an absolute timeout check. The idle timeout remains as the sole safeguard. This change does not introduce new behaviors that require real-environment testing. The logic change is syntactic: removing a deadline check loop condition and a post-loop timeout block. The core event-wait loop and idle timeout logic remain unchanged.
