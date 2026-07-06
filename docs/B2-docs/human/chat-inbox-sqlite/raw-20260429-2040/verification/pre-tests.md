# Pre-tests — chat-inbox SQLite

- issue_id: `I-20260429-2040-A`
- issue_path: `docs/B2-docs/human/chat-inbox-sqlite/issues/I-20260429-2040-A.md`

## Unit
- acceptance target: `chat-inbox.py module loads and core functions are callable.`
- testing layer: `unit`
- target environment: `feature/chat-inbox-sqlite-20260429`
- required evidence: `python3 -c import test`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `python3 -c "import sys; sys.path.insert(0, 'docs/system/workspace/scripts'); from chat_inbox import ChatInbox; print('OK')"`.

## Integration
- acceptance target: `freely init creates chat-inbox.db with correct schema.`
- testing layer: `integration`
- target environment: `feature/chat-inbox-sqlite-20260429`
- required evidence: `focused regression for db init`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `chat-inbox SQLite write + consume + discard cycle completes.`
- testing layer: `end_to_end`
- target environment: `feature/chat-inbox-sqlite-20260429`
- required evidence: `chat-inbox end-to-end test output`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `freely chat --new-issue "test"` and verify DB record.

## Real-Environment
- acceptance target: `The guarded promote lane carries the chat-inbox SQLite feature without regression.`
- testing layer: `real_environment`
- target environment: `develop`
- required evidence: `guarded promote replay plus governance-check`
- blocker taxonomy: `protected_environment_only`
- real_environment_status: `pass`
- real_environment_reason: `Merged into develop via 12c16edf (test-pre-merge) and 7bb14222 (feat code).`

## Acceptance Items

### chat-inbox DB is created on init
- id: `chat-inbox-db-created`
- requirement: `freely init creates chat-inbox.db with chats table.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/human/chat-inbox-sqlite/code-reviews/20260430-acp-session-store-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-5`
- case_design: `Verify .freely/chat-inbox.db exists and chats table has correct schema after init.`

### Chat write does not touch git working tree
- id: `chat-write-no-git-change`
- requirement: `freely chat --new-issue writes to SQLite, not filesystem, leaving git status clean.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/human/chat-inbox-sqlite/code-reviews/20260430-acp-session-store-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2`
- case_design: `Run freely chat --new-issue and verify git status is clean.`

### Governance check passes
- id: `chat-inbox-governance-check`
- requirement: `governance-check reports no new errors.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/human/chat-inbox-sqlite/code-reviews/20260430-acp-session-store-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1`
- case_design: `Run ./bin/governance-check.`
