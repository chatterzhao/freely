# Implementation Decision: runtime-startup-authority-and-readiness-governance

- issue_id: `I-20260413-0420-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-startup-authority-and-readiness-governance/issues/runtime-startup-authority-and-readiness-governance.md`
- branch: `feature/runtime-startup-authority-and-readiness-governance-20260413`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260413-feature-runtime-startup-authority-and-readiness-governance`
- decision_date: `2026-04-13`
- author: `codex`

## Implementation Decision Note

- decision: `Materialize C-20260413-0420-A as the bounded runtime owner that replaces pid/argv startup authority with runtime-published supervisor truth and daemon-ready gating.`
- why_this: `The root-cause packet already proved fake-supervisor acceptance, daemon false-ready, and early-unlock duplicate starts are one authority/readiness defect. This owner keeps that repair bounded without widening into the manager continuity contract.`
- alternatives_considered: `Keep patching argv heuristics; split daemon ready into a separate owner before launch authority is fixed; widen the same lane into manager handoff semantics.`
- boundary_non_goals: `Do not redesign manager continuity, full launch phase semantics, or foreground-versus-daemon entrypoint policy.`
- residual_risk: `Manager-ready and continuity materialization are still follow-on work, so this owner only guarantees startup authority/readiness truth rather than full manager handoff completeness.`

## Why

- supervisor identity had to stop being inferred from argv resemblance
- daemon ready needed the same truth model as foreground attach and stop cleanup
- same-project start serialization was still leaking before startup truth publication

## Scope decision

- Keep only:
  - authoritative supervisor identity publication
  - startup-truth-based validation and daemon-ready gating
  - start-lock timing and stop cleanup aligned to the same authority model
- Exclude:
  - manager continuity contract redesign
  - broader runtime state-machine formalization
  - unrelated recovery and slot-management policy work
