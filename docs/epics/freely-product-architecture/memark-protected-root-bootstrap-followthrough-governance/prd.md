# PRD: memark-protected-root-bootstrap-followthrough-governance

## Goal

Bring canonical Freely root metadata up to the documented MemArk root-init prerequisite without changing Freely's existing protected-root and worktree execution boundary.

## Requirements

1. Canonical root `.gitignore` must ignore `.memark/` and `corpus/`.
2. The followthrough must remain attached to the bootstrap/governance family rather than a new capability family.
3. Focused MemArk/bootstrap checks and governance checks must pass in the feature lane.

## Non-Requirements

1. No protected-root runtime-state policy change.
2. No new MemArk automation features inside Freely.
3. No broader bootstrap refactor beyond the root ignore prerequisite.
