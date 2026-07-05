# Candidates

## C-20260616T044825Z-A: legacy issue

- candidate_format_version: v2
- title: Remove BRIDGE_TIMEOUT absolute cap for session/prompt in acp-bridge.py
- status: promoted
- decision_reason: Industry standard (6 ACP projects checked) uses only idle timeouts, no absolute caps. The absolute 30-minute timeout kills legitimate long-running AI sessions even when actively producing output. The idle timeout (ACP_IDLE_TIMEOUT) already provides sufficient protection against hung sessions.
- next_action: Materialize as I-* issue and complete the implementation lifecycle. Implementation is already committed — B2_IBM needs PRD/tasks/pre-tests/code-review artifacts for governance gate compliance.
- revisit_trigger: N/A (promoted — fix already implemented and committed)
- acceptance_criteria:
  - The absolute timeout check in `_send_request()` is removed
  - The `while time.time() < deadline:` loop is changed to `while True:`
  - Only the idle timeout check remains for session/prompt handling
  - No regression in non-session/prompt methods (they use a separate timeout path)
- promotion_gate:
  - Code change verified in the fix worktree
  - No syntax errors in acp-bridge.py
  - B2_IBM materialization produces PRD, pre-tests, tasks, and code-review
- open_questions: []
- acceptance_reviews: []
- promoted_issue_path: `docs/issues/I-20260616T044825Z-A/issue.md`
- milestone: M-20260616T044825Z-A
- session_refs: []
