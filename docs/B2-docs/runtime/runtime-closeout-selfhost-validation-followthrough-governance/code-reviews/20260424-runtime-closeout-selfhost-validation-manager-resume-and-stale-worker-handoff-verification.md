# Verification: runtime-closeout-selfhost-validation manager resume and stale worker handoff

- issue_id: `I-20260419-0333-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/issues/runtime-closeout-selfhost-validation-followthrough-governance.md`
- verification_date: `2026-04-24`
- verifier: `codex`

## Scope Verdict

- `PASS`: valid retained-cleanup `resume_manager` contracts now write a continuation handoff instead of poisoning the next manager round back into `manager_exit_contract_repair`.
- `PASS`: authoritative manager worker launch now clears a stale `worker_exit_contract_repair` handoff before the next retained-cleanup worker round, so the worker follows the fresh cleanup prompt rather than replaying a repair-only override.
- `PASS`: adjacent exit-contract repair boundaries remain intact: repair-first worker prompts still render ahead of the broad lead-agent body, invalid worker exit contracts still force precise resume repair, and cleanup followthrough still runs before a valid manager resume continues.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-resume-writes-continuation-handoff`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-clears-stale-worker-repair-handoff`
3. `bash docs/system/workspace/scripts/tests/test-freely-worker-repair-prompt-prioritizes-exit-contract`
4. `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-resume-triggers-cleanup-followthrough`
5. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`

## Real Replay Evidence

- Canonical daemon replay at `2026-04-24 04:26:41 PDT` already showed the same owner moving past stale pre-stop continuity: manager fresh-patrolled, selected retained cleanup again, and emitted a new worker prompt instead of staying pinned on the old repair lane.
- The remaining blocker was semantic poisoning inside runtime-owned artifacts: `resume_manager` still rewrote the next handoff as repair-first, and the retained worker still carried an older `worker_exit_contract_repair` handoff even after manager had emitted a fresh authoritative cleanup prompt.
- The runtime change therefore stayed inside the same closeout/self-host owner: preserve lawful repair-only resumes when the contract is actually invalid, but stop reusing repair-only semantics once manager has already advanced to a valid continuation or fresh worker relaunch.

## Implementation Decision Note

- decision: `Preserve repair-first semantics only for real repair rounds; valid manager resumes become continuation handoffs, and authoritative manager worker relaunch clears stale worker repair handoff state.`
- why_this: `The retained cleanup lane was no longer blocked by task selection. It was blocked because runtime kept re-injecting stale repair state into later rounds even after manager had already produced fresher continuation truth.`
- alternatives_considered: `Drop repair-first prompt behavior entirely; special-case retained cleanup prompts only; let manager keep compensating by writing increasingly stronger natural-language instructions into every new worker prompt.`
- boundary_non_goals: `This change does not classify the retained cleanup worktree by itself, retire the dirty lane, or alter scan-json selection order.`
- residual_risk: `Canonical success still requires a fresh `develop` daemon replay proving the retained cleanup worker now settles lawfully and manager then moves on to the next scan-selected task.`
