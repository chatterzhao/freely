# Verification: auth-switch-real-environment-and-e2e-adequacy-governance

- issue_id: `I-20260410-1835-A`
- issue_path: `docs/epics/workspace-routing-foundation/auth-switch-real-environment-and-e2e-adequacy-governance/issues/auth-switch-real-environment-and-e2e-adequacy-governance.md`
- verification_date: `2026-04-10`
- verifier: `codex`

## Scope Verdict

- `PASS`: IBM/checklist truth now states that auth/switch/startup-recovery family follow-on owners cannot dual-waive `End-to-End` and `Real-Environment` without artifact-backed live evidence
- `PASS`: `pretests-gate` enforces that adequacy rule
- `PASS`: the focused `test-pretests-gate` regression proves the bad pattern is rejected and the corrected pattern passes
- `PASS`: the owner package records why the earlier regression was missed and what class of live executable evidence now prevents the same miss

## Commands

1. `bash docs/system/workspace/scripts/tests/test-pretests-gate`

## Root-Cause Summary

1. The miss was not caused by a total absence of tests or gates.
2. The active owner contract drifted narrower and legally waived both `End-to-End` and `Real-Environment`.
3. Existing gates only validated the current owner contract, so the drift passed structurally.
4. This owner closes that exact gap by preserving a mandatory live-evidence surface for the auth/switch/startup-recovery family.

## Live Evidence Surface Protected By This Owner

The acceptable live evidence surfaces called out by the updated truth are:

1. real `bin/ai` command execution
2. real `codex exec` slot validation
3. real `freely start` plus log observation

Those surfaces are what the runtime follow-on owner now records, and what future owners in this family can no longer waive away without replacement evidence at `real_env` or `post_merge_dogfood` level.

## Implementation Decision Note

- decision: `Add an auth/switch family adequacy rule to IBM/checklist truth and enforce it in pretests-gate with a focused regression.`
- why_this: `The failure mode was owner-contract drift, so the fix had to bind the owner acceptance surface more tightly rather than just adding another standalone runtime test.`
- alternatives_considered: `Only add more ad hoc tests; make merge gates infer capability families from implementation paths alone; broaden the rule to every owner immediately; leave the rule as prose with no executable gate.`
- boundary_non_goals: `No runtime behavior changes, no historical issue rewrite, and no broad path-guessing test-matrix inference.`
- residual_risk: `Other capability families may later need similar adequacy rules, but this owner deliberately fixes the proved auth/switch/startup-recovery gap first.`
