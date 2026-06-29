# Pre-Tests: memark-protected-root-bootstrap-followthrough-governance

## Unit
- acceptance target: `No code-path rewrite is required for this owner; the unit boundary is that the canonical root ignore contract is expressed as plain repository metadata.`
- testing layer: `unit`
- target environment: `feature/memark-init`
- required evidence: `tracked root .gitignore entries plus issue-bound verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `rg -n '^\\.memark/$|^corpus/$' .gitignore`.

## Integration
- acceptance target: `Canonical Freely root carries the MemArk ignore prerequisite while linked worktree MemArk usage remains healthy.`
- testing layer: `integration`
- target environment: `feature/memark-init`
- required evidence: `focused MemArk/bootstrap checks plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `git diff --check`.
2. Run `/Users/zhaoyu/.memark/venv/bin/memark init /Users/zhaoyu/Downloads/code/my-freely/freely --no-auto --json`.
3. Run `/Users/zhaoyu/.memark/venv/bin/memark status --workspace /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-memark-init --project freely --json`.
4. Run `/Users/zhaoyu/.memark/venv/bin/memark context --workspace /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-memark-init --project freely --no-refresh`.
5. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `A guarded feature -> test-pre-merge -> develop chain can evaluate this owner against explicit premerge adequacy truth instead of candidate-only metadata.`
- testing layer: `end_to_end`
- target environment: `test-pre-merge-20260416-memark-init`
- required evidence: `guarded merge replay plus pretests-gate and governance evidence`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `freely pr-merge-guarded test-pre-merge-20260416-memark-init feature/memark-init`.
2. Run `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260416-test-pre-merge-memark-init --issue docs/epics/freely-product-architecture/memark-protected-root-bootstrap-followthrough-governance/issues/memark-protected-root-bootstrap-followthrough-governance.md`.
3. Run `./bin/test-lane premerge-integration -- ./bin/governance-check`.

## Real-Environment
- acceptance target: `The practical MemArk execution surface remains the linked writable worktree after the root metadata repair.`
- testing layer: `real_environment`
- target environment: `feature/memark-init`
- required evidence: `linked worktree MemArk status and context output`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `/Users/zhaoyu/.memark/venv/bin/memark status --workspace /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-memark-init --project freely --json`.
2. Run `/Users/zhaoyu/.memark/venv/bin/memark context --workspace /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-memark-init --project freely --no-refresh`.
- real_environment_status: `pass`
- real_environment_reason: `Linked worktree MemArk usage remained healthy before and after the root ignore repair, so this owner only needs to preserve that usable surface while fixing canonical root metadata.`

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `the owner is explicitly recorded as a completed-family bootstrap followthrough of the fresh-project bootstrap family`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/memark-protected-root-bootstrap-followthrough-governance/issues/memark-protected-root-bootstrap-followthrough-governance.md`

### PT-2
- id: `PT-2`
- requirement: `canonical Freely root .gitignore contains .memark/ and corpus/`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `.gitignore`

### PT-3
- id: `PT-3`
- requirement: `the linked feature worktree still has usable MemArk status and context after the root ignore repair`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/memark-protected-root-bootstrap-followthrough-governance/code-reviews/20260416-memark-protected-root-bootstrap-followthrough-verification.md`

### PT-4
- id: `PT-4`
- requirement: `governance truth remains internally consistent after adding the narrow followthrough owner`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `./bin/governance-check`

### Guarded develop promote proves MemArk bootstrap adequacy
- id: `develop-promote-memark-bootstrap-adequacy`
- requirement: `A guarded test-pre-merge replay proves this owner carries explicit premerge-integration coverage for the root ignore prerequisite before develop promotion.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `Replay the narrow bootstrap followthrough on a disposable test-pre-merge branch created from develop and use that replay to prove guarded promotion adequacy for the root ignore prerequisite.`
- case_design: `Merge feature/memark-init into test-pre-merge-20260416-memark-init with pr-merge-guarded, rerun pretests-gate plus governance-check there, and use the resulting evidence to show develop promotion is tied to the explicit premerge lane instead of generic pass text.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/memark-protected-root-bootstrap-followthrough-governance/code-reviews/20260416-memark-protected-root-bootstrap-followthrough-verification.md`

## Pre-merge Focused Regression / Smoke

1. acceptance target:
   - canonical Freely root now satisfies the MemArk ignore prerequisite while linked worktree usage remains healthy
2. testing layer:
   - integration
3. target environment:
   - feature worktree plus canonical root readback
4. required evidence:
   - `git diff --check`
   - `rg -n '^\\.memark/$|^corpus/$' .gitignore`
   - `/Users/zhaoyu/.memark/venv/bin/memark init /Users/zhaoyu/Downloads/code/my-freely/freely --no-auto --json`
   - `/Users/zhaoyu/.memark/venv/bin/memark status --workspace /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-memark-init --project freely --json`
   - `/Users/zhaoyu/.memark/venv/bin/memark context --workspace /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-memark-init --project freely --no-refresh`
   - `./bin/governance-check`
5. blocker taxonomy:
   - `definition_missing`
   - `commands_only`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
6. failure handling / replay expectation:
   - keep the owner narrow and repair only root ignore metadata or its lifecycle evidence

## Post-merge Integration Acceptance

1. acceptance target:
   - canonical `develop` carries the root ignore prerequisite and linked worktree MemArk usage remains the practical execution surface
2. testing layer:
   - contract replay against `develop`
3. target environment:
   - `develop`
4. required evidence:
   - `rg -n '^\\.memark/$|^corpus/$' .gitignore`
   - `/Users/zhaoyu/.memark/venv/bin/memark init /Users/zhaoyu/Downloads/code/my-freely/freely --no-auto --json`
5. blocker taxonomy:
   - `execution_pending_or_failed`
   - `evidence_plan_missing`
6. failure handling / replay expectation:
   - if root bootstrap regresses again, reopen as a new narrow bootstrap owner rather than widening this one
