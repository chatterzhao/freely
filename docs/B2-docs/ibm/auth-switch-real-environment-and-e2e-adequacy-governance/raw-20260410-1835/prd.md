# PRD: auth-switch-real-environment-and-e2e-adequacy-governance

## Objective

Ensure that future auth/switch/startup-recovery follow-on owners cannot pass governance with purely structural pre-tests if they have removed all artifact-backed live executable evidence from `End-to-End` and `Real-Environment`.

## Product Requirements

1. IBM/checklist truth must state the family-specific adequacy rule.
2. `pretests-gate` must enforce the rule.
3. The rule must preserve live evidence surfaces such as real `bin/ai`, real `codex exec`, or real `freely start`.
4. The owner package must explain why the earlier miss happened so the acceptance standard is explicit, not implicit.
