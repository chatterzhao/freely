# Issue: develop-push-attempt-followthrough-governance

- issue_id: `I-20260412-1721-A`
- title: Develop push attempt followthrough governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `develop-push-attempt-followthrough-governance`
- issue-name: `develop-push-attempt-followthrough-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260412T184500Z/candidates.md#c-20260412-1721-a`
- source_brainstorm: `docs/B1-docs/raw-20260412T184500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: docs/B2-docs/ibm/develop-push-attempt-followthrough-governance/raw-20260412-1721/verification/pre-tests.md
- progress_path: `docs/progress/workspace-routing-foundation/p-develop-push-attempt-followthrough-governance.md`
- verification_artifact_dir: docs/B2-docs/ibm/develop-push-attempt-followthrough-governance/raw-20260412-1721/code-reviews
- depends_on:
  - `docs/B2-docs/ibm/develop-push-pending-guard-governance/issues/develop-push-pending-guard-governance.md`
  - `docs/B2-docs/ibm/develop-push-followthrough-escalation-governance/issues/develop-push-followthrough-escalation-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely already exposes develop push debt as explicit truth, but it still stops short of automatically handling the current merge's remote-delivery followthrough. That leaves a gap between “merge completed locally” and “this round actually tried to deliver canonical truth to remote.”

## Scope

1. Add one controlled post-merge push attempt for successful `develop` merges.
2. Freeze the bounded execution contract for `freely develop-push attempt`.
3. Add explicit blocked-attempt truth so patrol/manager can distinguish unattempted push debt from failed delivery.
4. Preserve existing push gate behavior and lawful defer windows.
5. Keep retry engines, hook auto-push, and hidden transport loops out of scope.

## Non-Goals

1. Do not turn hooks into transport executors.
2. Do not add automatic retry-until-success behavior.
3. Do not erase `post_merge_acceptance` / `cleanup_followthrough` / `remote_delivery_hold`.
4. Do not redesign feature/test-pre-merge/develop merge topology.

## Acceptance

1. A lawful merge into `develop` triggers one controlled push attempt automatically.
2. The attempt still flows through the existing pre-push gate and can be blocked lawfully.
3. When the attempt is blocked and `develop` remains ahead of its tracked remote, the state becomes explicit `push_blocked` truth instead of generic `push_pending`.
4. `manager-agent`, patrol guidance, runtime status, and fleet surfaces can all recognize `push_blocked` as immediate followthrough.
5. No hidden auto-push or retry engine is introduced.

## Completion Evidence

- guarded develop merge receipt: `9bcf5fcf`
- canonical delivery command: `freely develop-push attempt --project /Users/zhaoyu/Downloads/code/my-freely/freely`
- canonical delivery result: `attempt_status: pushed`
- verification artifact: `docs/B2-docs/ibm/develop-push-attempt-followthrough-governance/code-reviews/20260412-develop-push-attempt-followthrough-verification.md`

## IBM Handoff

- implementation_scope_summary:
  - This owner is the execution follow-on for the completed develop-push governance family.
  - It adds one explicit push-attempt action and explicit blocked-attempt writeback, while preserving the no-hidden-auto-push boundary.
- required_doc_refs:
  - `docs/B1-docs/raw-20260412T184500Z/brainstorms.md`
  - `docs/B1-docs/raw-20260412T184500Z/candidates.md`
  - `docs/B2-docs/ibm/develop-push-attempt-followthrough-governance/prd.md`
  - `docs/B2-docs/ibm/develop-push-attempt-followthrough-governance/pre-tests.md`
  - `docs/B2-docs/ibm/develop-push-attempt-followthrough-governance/tasks.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/worktree/pr-merge-guarded`
  - `docs/system/workspace/hooks/pre-push.sh`
