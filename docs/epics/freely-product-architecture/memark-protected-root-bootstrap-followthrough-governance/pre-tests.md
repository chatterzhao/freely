# Pre-Tests: memark-protected-root-bootstrap-followthrough-governance

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
