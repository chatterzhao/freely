# Brainstorm: memark-protected-root-bootstrap-followthrough-governance

## Narrowing

The product question is already settled:

- `memark init` now requires `.memark/` and `corpus/` to be ignored at the canonical repository root
- linked worktrees should attach only after the main repository root is ready
- Freely protected roots still do not become owner-development write surfaces

This owner therefore does not need new product discovery. It only needs to freeze that:

1. canonical Freely root metadata lagged behind the new MemArk bootstrap contract
2. the repair is the root `.gitignore` addition plus lifecycle evidence
3. the protected-root boundary remains unchanged

## Owner Boundary

This owner should absorb:

1. `.gitignore` entries for `.memark/` and `corpus/`
2. the candidate / issue / progress / verification evidence required by the develop merge gate
3. focused proof that canonical root now satisfies the documented MemArk ignore prerequisite

This owner should not absorb:

1. direct protected-root `memark init` execution claims
2. policy changes to protected-branch write rules
3. broader MemArk runtime integration work
