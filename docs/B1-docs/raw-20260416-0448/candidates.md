# 候选：memark-protected-root-bootstrap-followthrough

- id: `C-20260416-0448-A`
- candidate_format_version: `v2`
- title: Align canonical Freely root bootstrap metadata with the MemArk protected-root init contract
- source_brainstorm: `docs/B1-docs/raw-20260416-0448/brainstorms.md`
- reopen_of_issue: `docs/B2-docs/config/packaging/issues/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
- reopen_reason: `memark 0.1.1 now correctly requires canonical repo roots to ignore .memark/ and corpus/ before root init, and Freely root still lacked those ignore entries`
- problem: canonical Freely root failed the new MemArk root-init prerequisite because `.gitignore` did not ignore `.memark/` and `corpus/`, even though linked worktrees were already using MemArk successfully.
- why_now:
  - the upgraded local `memark` install is already the canonical user-facing guidance surface, so Freely should meet that contract too
  - guarded develop promotion was correctly blocked until this `.gitignore` repair gained a candidate-driven lifecycle
  - the remaining gap is narrow and bootstrap-scoped, so reopening the closest completed owner is the smallest compliant path
- acceptance_criteria:
  - canonical Freely root ignores `.memark/` and `corpus/`
  - the followthrough is documented as a bootstrap/governance reopen of `I-20260405-2358-A`
  - focused verification proves the ignore prerequisite is now present without claiming protected-root runtime-state writes
  - the resulting feature lane can replay through the guarded `feature/* -> test-pre-merge-* -> develop` path
- promotion_gate:
  - keep scope limited to root ignore metadata plus the minimum lifecycle writeback
  - preserve the existing protected-root boundary and worktree-first owner-development policy
  - verify readiness with focused MemArk/bootstrap checks and governance checks only
- open_questions:
  - none; the desired repo-root contract is now explicit in MemArk 0.1.1 guidance
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `This is a narrow completed-family followthrough: canonical Freely root metadata lagged behind the now-canonical MemArk init prerequisite, while writable worktrees already remained the right execution surface.`
    verdict: `ready_for_ibm`
- priority: `P1`
- status: `promoted`
- decision_reason:
  - the missing ignore entries belong to bootstrap/root-readiness governance, not to a new reusable capability family
  - a fresh candidate and issue are the minimum compliant route through the guarded develop merge gate
  - the owner stays narrow enough to close as soon as `develop` absorbs the root metadata repair
- milestone: `M-20260326-freely-product-architecture`
- promoted_issue_path: `docs/B2-docs/config/packaging/issues/memark-protected-root-bootstrap-followthrough-governance.md`
- promoted_issue_path_role: `primary-owner`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - `I-20260416-0448-A` owns the root `.gitignore` followthrough, focused verification, and guarded promotion evidence.
- revisit_trigger:
  - reopen only if canonical Freely root again loses the MemArk ignore prerequisite or protected-root bootstrap guidance drifts from MemArk's documented contract
