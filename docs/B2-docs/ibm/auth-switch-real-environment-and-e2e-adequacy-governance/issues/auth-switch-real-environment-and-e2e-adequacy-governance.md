# Issue: auth-switch-real-environment-and-e2e-adequacy-governance

- issue_id: `I-20260410-1835-A`
- title: Auth switch real-environment and end-to-end adequacy governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `auth-switch-real-environment-and-e2e-adequacy-governance`
- issue-name: `auth-switch-real-environment-and-e2e-adequacy-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260410/candidates.md#c-20260410-1835-a`
- source_brainstorm: `docs/B1-docs/raw-20260410/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/auth-switch-real-environment-and-e2e-adequacy-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-auth-switch-real-environment-and-e2e-adequacy-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/auth-switch-real-environment-and-e2e-adequacy-governance/code-reviews`
- follow_on_to: `I-20260327-0701`
- created_at: `2026-04-10`
- session_refs: []

## Why

The observed miss was not that Freely lacked tests in the abstract. High-level truth already required `Unit / Integration / End-to-End / Real-Environment`, and the gates already checked that those sections existed. The gap was narrower and more serious:

1. recent auth/switch follow-on owners could dual-waive `End-to-End` and `Real-Environment`
2. the gate only checked the current owner contract, so those waivers looked structurally valid
3. real `bin/ai`, real `codex exec`, and real `freely start` evidence could therefore disappear from the owner acceptance surface without tripping a merge blocker

## Scope

1. Tighten IBM/checklist/quality-bar truth so follow-on owners touching `auth switch / account switch / slot recovery / startup recovery / watchdog / freely start / bin/ai / codex exec` cannot dual-waive `End-to-End` and `Real-Environment` without artifact-backed live evidence.
2. Tighten `pretests-gate` so the same family fails when both sections are waived without at least one passing `real_env` or `post_merge_dogfood` acceptance item.
3. Lock the behavior with a focused regression.
4. Record the root-cause line clearly: the miss came from owner-contract drift plus overly legal waivers, not from a total absence of gates.

## Non-Goals

1. Do not change runtime switch behavior in this owner.
2. Do not make merge gates invent a complete test matrix from changed paths alone.
3. Do not rewrite unrelated historical issues.

## Acceptance

1. IBM/checklist truth explicitly describes the auth/switch/startup-recovery adequacy rule.
2. `pretests-gate` blocks the bad dual-waive pattern for this family.
3. The focused gate regression passes.
4. The owner package itself explains why the earlier problem was missed and what class of real-environment evidence now prevents the same miss.

## Verification

- `docs/epics/workspace-routing-foundation/auth-switch-real-environment-and-e2e-adequacy-governance/code-reviews/20260410-auth-switch-real-environment-and-e2e-adequacy-verification.md`

## Completion

- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
- `docs/system/workspace/scripts/quality/pretests-gate`
- `docs/system/workspace/scripts/tests/test-pretests-gate`

## Next

- Completed in the dedicated governance feature worktree. Promote through `test-pre-merge-20260410-codex-switch-real-env` and guarded merge to `develop`.
