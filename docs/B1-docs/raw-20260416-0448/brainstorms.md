# Brainstorms: memark-protected-root-bootstrap-followthrough

## Context

`memark 0.1.1` now correctly rejects repository-root init when the root does not already ignore `.memark/` and `corpus/`. Replaying that check against canonical Freely root showed the remaining gap is not MemArk runtime logic inside Freely; it is a missing root ignore contract on the protected repository root.

The fix is narrow:

1. add `.memark/` and `corpus/` to the canonical root `.gitignore`
2. record that the root repository now satisfies the documented MemArk init prerequisite
3. keep the governance boundary explicit: protected root still does not become a writable runtime-state host for owner development

## Why This Is A Followthrough

This is closest to the already-completed fresh-project/bootstrap family rather than a new capability family:

- it is about first-hop project-root readiness
- it affects the canonical repo bootstrap surface
- the product truth is still that writable worktrees host active owner development while the protected root remains an integration surface

The missing ignore entries are therefore a bootstrap/governance followthrough, not a new MemArk capability or a Freely runtime redesign.

## Boundary

This owner should absorb:

1. the `.gitignore` addition for `.memark/` and `corpus/`
2. the candidate / issue / progress / verification artifacts needed for guarded promote into `develop`
3. focused proof that the new MemArk root-init prerequisite is now satisfied by the canonical repo metadata

This owner should not absorb:

1. a claim that `memark init` is now directly executed on protected Freely root
2. a policy change that allows protected root runtime-state writes
3. broader MemArk worktree automation or Freely runtime integration work
