# Issue: kiro-cli-runtime-availability-failure-governance

- issue_id: `I-20260331-1830-A`
- title: Kiro CLI runtime availability failure governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `kiro-cli-runtime-availability-failure-governance`
- issue-name: `kiro-cli-runtime-availability-failure-governance`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260331-1830/candidates.md#c-20260331-1830-a`
- source_brainstorm: `docs/B1-docs/raw-20260331-1830/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/kiro-cli-runtime-availability-failure-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/kiro-cli-runtime-availability-failure-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/issues/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Recent dogfood runs exposed one concrete Kiro failure family:

- `Unable to verify subscription status: service error`
- `Monthly request limit reached`

Before the fix, Freely recorded these exits as plain `ai_exit_rc_0`, left `slot_switch_reason=none`, and immediately relaunched both root and worker supervisors into the same unusable path. That was not just noisy behavior; it corrupted runtime truth and hid a control-plane availability failure behind a fake healthy completion.

The minimal correct owner is therefore narrow:

1. classify the observed Kiro strings as canonical runtime availability failures,
2. stop the local relaunch loop once they appear, and
3. defer the next recovery decision back to the watchdog / manager control plane.

## Scope

1. Detect the observed Kiro monthly-limit and subscription-status-service-error strings from cycle logs.
2. Map them to explicit `slot_switch_reason` values instead of `ai_exit_rc_0`.
3. Keep root and worker supervisors on the same stop-and-defer contract.
4. Lock the behavior with a focused regression.
5. Write the classification boundary back to workspace tooling / availability truth sources.

## Non-Goals

1. Do not redesign cross-tool fallback ordering.
2. Do not invent a shared all-tools availability schema in this slice.
3. Do not add Kiro-specific cooldown/reset parsing beyond the observed stop-and-defer behavior.
4. Do not change Kiro's weak continuity contract.
5. Do not reopen the already completed Codex/OAuth availability owners unless new shared evidence appears.

## Acceptance

1. `kiro-cli` monthly-limit output is written as `kiro_monthly_request_limit`.
2. `Unable to verify subscription status: service error` without the monthly-limit line is still written as a canonical Kiro availability reason.
3. The supervisor stops after writing the availability reason instead of relaunching into `ai_exit_rc_0`.
4. The same contract holds in the focused test fixture for both root and worker style supervisors.
5. Workspace tooling / availability references document this failure family as part of the current Kiro runtime contract.

## Completion

- `docs/epics/workspace-routing-foundation/kiro-cli-runtime-availability-failure-governance/issues/kiro-cli-runtime-availability-failure-governance.md`
- `docs/epics/workspace-routing-foundation/kiro-cli-runtime-availability-failure-governance/prd.md`
- `docs/epics/workspace-routing-foundation/kiro-cli-runtime-availability-failure-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/kiro-cli-runtime-availability-failure-governance/tasks.md`
- `docs/epics/workspace-routing-foundation/kiro-cli-runtime-availability-failure-governance/code-reviews/20260331-kiro-cli-runtime-availability-verification.md`
- `docs/progress/workspace-routing-foundation/p-kiro-cli-runtime-availability-failure-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/skills/ai-cli-availability-manager/references/limit-patterns.md`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
- `./bin/governance-check`

## Next

- `2026-03-31 19:31 PDT` narrow Kiro-scoped closeout is complete: the runtime classifier and focused regression were already absorbed by `develop` commit `3a6b0e0`, and this issue only writes back the canonical owner / verification / milestone truth.
- Any future work that expands from "known Kiro failure family -> stop local relaunch" into same-tool slot recovery or cross-tool fallback must open a new lifecycle instead of reopening this completed owner.
