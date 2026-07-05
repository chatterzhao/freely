# PRD: structured-closeout-gate-context-and-review-evidence-governance

## Objective

Make the closeout adequacy contract recoverable before guarded `develop` merge by turning lane/gate/review-evidence requirements into structured verification truth instead of weak free-text replay hints.

## Product Requirements

1. Freeze machine-readable closeout fields for:
   - closeout command
   - target lane
   - promotion gate
   - adequacy requirement
   - review-artifact policy
2. Persist those fields in delegated intake, runtime verification contract, and worker workcell state.
3. Route cleanup/retirement replay through structured closeout fields rather than reparsing shell command strings.
4. Align worker guidance and merge-gate diagnostics so develop-bound promote explicitly states when a fresh staged owner review artifact is required.
5. Preserve current fail-closed gate behavior; this owner may improve observability and recovery guidance, not loosen enforcement.

## Non-Requirements

1. No new test orchestration DSL.
2. No global backfill of all historical worker snapshots.
3. No parallel review-artifact family outside owner `verification_artifact_dir`.
4. No branch-name heuristics or changed-path guessing.

## Non-Negotiables

- `pre-tests.md` remains the only canonical test/success artifact.
- `test-pre-merge-* -> develop` continue to require owner-bound staged review evidence when current policy demands it.
- runtime and cleanup replay may not silently infer missing lane/gate policy from free-text command fragments.
- any compatibility path for old snapshots must fail closed and route into retained continuation.

## Product Surface

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/quality/pretests-retirement-gate`
- `docs/system/workspace/scripts/quality/pretests-gate`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-natural-language-prompt`
- `docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`
- `docs/system/workspace/scripts/tests/test-pretests-retirement-gate`

## Decomposition

1. Freeze the structured closeout field schema.
2. Materialize those fields in prompt parsing, intake contract writing, and workcell state.
3. Update cleanup replay to consume structured fields.
4. Align gate diagnostics and worker-facing guidance.
5. Add focused regressions for missing lane/gate/evidence-policy context.

## Eval Plan

Success:

- runtime state records closeout lane/gate/evidence policy directly
- cleanup replay can fail with field-level diagnostics before reparsing command strings
- merge guidance explicitly names missing fresh staged owner review evidence when that is the blocker
- no current guarded merge path becomes more permissive

Failure:

- `LAST_WORKER_CLOSEOUT_GATE` remains the only authoritative replay source
- operators still cannot tell whether the blocker is missing adequacy item vs missing fresh staged review artifact
- cleanup replay silently downgrades missing structured fields into best-effort shell parsing

## Revisit Triggers

- if implementation proves review-artifact policy needs a separate shared enum owner
- if dev-loop shows the compatibility path for old snapshots is large enough to deserve its own follow-on
