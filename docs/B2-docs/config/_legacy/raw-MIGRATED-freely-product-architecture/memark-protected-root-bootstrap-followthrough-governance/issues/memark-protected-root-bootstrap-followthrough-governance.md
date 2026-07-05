# Issue: memark-protected-root-bootstrap-followthrough-governance

- issue_id: `I-20260416-0448-A`
- title: MemArk protected-root bootstrap followthrough governance
- phase_state: `completed`
- milestone: `M-20260326-freely-product-architecture`
- epic-name: `freely-product-architecture`
- story-name: `memark-protected-root-bootstrap-followthrough-governance`
- issue-name: `memark-protected-root-bootstrap-followthrough-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260416/candidates.md#c-20260416-0448-a`
- source_brainstorm: `docs/B1-docs/raw-20260416/brainstorms.md`
- reopen_of_issue: `docs/B2-docs/config/packaging/issues/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
- reopen_reason: `memark 0.1.1 requires canonical repo roots to ignore .memark/ and corpus/ before root init, and Freely root still lacked those ignore entries`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/config/packaging/pre-tests.md`
- progress_path: `docs/progress/freely-product-architecture/p-memark-protected-root-bootstrap-followthrough-governance.md`
- verification_artifact_dir: `docs/B2-docs/config/packaging/code-reviews`
- depends_on:
  - `docs/B2-docs/config/packaging/issues/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
  - `docs/B2-docs/config/packaging/issues/worktree-tool-boundary-bootstrap-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Upgraded `memark 0.1.1` replay showed canonical Freely root still missed one narrow bootstrap prerequisite:

1. MemArk now requires `.memark/` and `corpus/` to be ignored before `memark init` can run at the main repository root.
2. Canonical Freely root previously did not ignore those paths, so the new guidance correctly rejected root init there.
3. Linked Freely worktrees were already using MemArk successfully, which means the remaining defect is bootstrap metadata at the protected root, not the worktree consumption path.

Because guarded develop promotion requires a candidate-driven lifecycle even for narrow followthrough patches, this root metadata repair needs its own owner instead of silently editing a completed family.

## Scope

1. Add `.memark/` and `corpus/` to canonical Freely root `.gitignore`.
2. Materialize the minimum candidate / issue / progress / verification lifecycle needed for guarded develop replay.
3. Prove the canonical root now satisfies the MemArk ignore prerequisite while keeping protected-root owner-development rules unchanged.

## Non-Goals

1. Do not claim that protected Freely root now directly hosts `memark init` runtime-state writes.
2. Do not change Freely protected-branch or worktree governance.
3. Do not widen into broader MemArk capability integration or automation redesign.
4. Do not reopen linked-worktree MemArk consumption, which is already working.

## Acceptance

1. Canonical Freely root `.gitignore` explicitly ignores `.memark/` and `corpus/`.
2. The reopen is documented as a narrow followthrough of `I-20260405-2358-A`.
3. Focused verification shows the canonical root now meets the documented MemArk init ignore prerequisite.
4. Verification also preserves the boundary that active owner development still runs in writable worktrees rather than on protected root.

## Verification

- `git diff --check`
- `rg -n '^\\.memark/$|^corpus/$' .gitignore`
- `/Users/zhaoyu/.memark/venv/bin/memark init /Users/zhaoyu/Downloads/code/my-freely/freely --no-auto --json`
- `/Users/zhaoyu/.memark/venv/bin/memark status --workspace /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-memark-init --project freely --json`
- `/Users/zhaoyu/.memark/venv/bin/memark context --workspace /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-memark-init --project freely --no-refresh`
- `./bin/governance-check`

## Current Evidence

1. The feature worktree already carries the `.gitignore` repair needed by the new MemArk bootstrap contract.
2. `memark status` and `memark context` already work in the linked `feature/memark-init` worktree, so this owner does not need to reopen worktree consumption.
3. The remaining promote blocker is governance lifecycle evidence, not MemArk runtime correctness in the linked worktree.

## Closeout

1. Keep the feature lane narrow: root `.gitignore` plus lifecycle writeback only.
2. Replay the owner through `feature/memark-init -> test-pre-merge-memark-init -> develop`.
3. After guarded develop promotion, re-check the canonical Freely root against MemArk's root-init contract and keep worktree-first execution guidance explicit.
