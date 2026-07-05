# Issue: manager-task-source-scan-idle-replan-boundary-governance

- issue_id: `I-20260420-1130-A`
- title: `Manager task-source scan idle/replan boundary governance`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-task-source-scan-idle-replan-boundary-governance`
- issue-name: `manager-task-source-scan-idle-replan-boundary-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260420T113000Z/candidates.md#c-20260420-1130-a`
- source_brainstorm: `docs/B1-docs/raw-20260420T113000Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/manager-task-source-scan-idle-replan-boundary-governance/pre-tests.md`
- tasks_path: `docs/B2-docs/ibm/manager-task-source-scan-idle-replan-boundary-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-manager-task-source-scan-idle-replan-boundary-governance.md`
- verification_artifact_dir: `docs/B2-docs/ibm/manager-task-source-scan-idle-replan-boundary-governance/code-reviews`
- depends_on:
  - `docs/B1-docs/raw-20260407T103600Z/candidates.md#c-20260407-0817-a`
  - `docs/B2-docs/ibm/manager-owner-stance-and-source-patrol-governance/issues/manager-owner-stance-and-source-patrol-governance.md`
  - `docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/issues/latest-manager-continuity-worker-consumption-governance.md`
- created_at: `2026-04-20`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely already has multiple places where a manager can discover work, but it still needed a runtime-owned answer to a narrower question: when should those surfaces be rescanned, and when should the current continuity or active worker remain authoritative?

The current self-host replay proved two opposite failures at the same seam:

1. stale delegated continuation could keep the manager from returning to higher-level task surfaces after startup or closeout
2. broad patrol could also pull the manager away from an already-active worker lane if scan regeneration happened every round

This owner freezes the idle/replan scan boundary and lands the first machine-readable patrol seed contract without widening into provider automation.

## Scope

1. Freeze `task-source-scan` as an idle/replan step rather than an every-cycle patrol step.
2. Freeze the first bounded trigger set for regeneration, reuse, and suppression.
3. Materialize the machine-readable `manager-task-source-scan-latest.json` and scan-state contract used by manager patrol.
4. Keep durable raw source families (`human interruption`, `external issue`) distinct from standing surfaces (`delegated continuation`, milestone, pre-brainstorm, progress).
5. Land the minimum runtime, test, and skill truth needed so startup manager rounds can find work autonomously without hijacking active worker continuity.

## Non-Goals

1. Do not widen this owner into GitHub or Gitee provider automation.
2. Do not collapse all standing surfaces into a new raw-source-family schema.
3. Do not redesign generic runtime/fleet orchestration outside the idle/replan patrol seam.
4. Do not promote `recovery` into the same patrol snapshot unless a later owner makes that boundary explicit.

## Acceptance

1. Runtime only regenerates task-source scan JSON on bounded idle/replan triggers.
2. Active workers suppress broad patrol scan regeneration while their current continuity remains authoritative.
3. Idle manager rounds can reuse the latest scan JSON as patrol seed when no new regeneration is needed.
4. The scan contract records trigger reason plus per-surface trust/reconcile hints for milestone, pre-brainstorm, progress, delegated continuation, and human chat intake.
5. Focused regressions cover startup generation, active-worker suppression, idle-after-continuity regeneration, stale delegated filtering, and launch-time prompt consumption.
6. The owner stays bounded to this patrol seam and does not absorb external issue provider automation or a broader runtime redesign.

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-includes-milestone-patrol-seed`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-suppresses-broad-patrol-while-worker-active`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-task-source-scan-ignores-pre-stop-continuity-anchor`
- `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-provider-hints`
- `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-python-compat`
- `bash docs/system/workspace/scripts/tests/test-start-lead-agent-verification-metadata-contract`
- `bash -n docs/system/workspace/scripts/runtime/freely`
- `./bin/governance-check`
- `git diff --check`

## Completion

- `docs/B1-docs/raw-20260420T113000Z/brainstorms.md`
- `docs/B1-docs/raw-20260420T113000Z/candidates.md`
- `docs/milestones.md`
- `docs/B2-docs/ibm/manager-task-source-scan-idle-replan-boundary-governance/issues/manager-task-source-scan-idle-replan-boundary-governance.md`
- `docs/B2-docs/ibm/manager-task-source-scan-idle-replan-boundary-governance/pre-tests.md`
- `docs/B2-docs/ibm/manager-task-source-scan-idle-replan-boundary-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-manager-task-source-scan-idle-replan-boundary-governance.md`
- `docs/B2-docs/ibm/manager-task-source-scan-idle-replan-boundary-governance/code-reviews/20260420-manager-task-source-scan-idle-replan-boundary-verification.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/task-source-scan.py`
- `docs/system/workspace/scripts/tests/test-freely-manager-prompt-includes-milestone-patrol-seed`
- `docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`
- `docs/system/workspace/scripts/tests/test-freely-manager-prompt-suppresses-broad-patrol-while-worker-active`
- `docs/system/workspace/scripts/tests/test-freely-manager-task-source-scan-ignores-pre-stop-continuity-anchor`
- `docs/system/workspace/scripts/tests/test-freely-task-source-scan-provider-hints`
- `docs/system/workspace/scripts/tests/test-freely-task-source-scan-python-compat`
- `docs/system/workspace/scripts/tests/test-start-lead-agent-verification-metadata-contract`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/skills/context-source-skill/SKILL.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`

## Next

- Keep provider scan/writeback, recovery-surface promotion, and broader patrol/fleet redesign in follow-on owners.
- Use this owner as the canonical boundary for future GitHub/Gitee patrol inputs instead of widening the current lane silently.
