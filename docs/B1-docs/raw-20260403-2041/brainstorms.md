# Brainstorms - 20260403-2041--worktree-tool-boundary-bootstrap

## Context

`I-20260401-1303-A-2` already froze the first Freely tool-materialization split:

- Codex can own a project-local config surface
- some tools only expose launch-time boundary injection
- user home config remains manual-only guidance by default

However, a new dogfood failure showed the first slice was still incomplete for sibling worktree execution:

1. tool-local config and wrapper materialized in the project root but not automatically in newly created sibling worktrees
2. tools that can launch from the project root could still lose write access to `{project}-worktrees` and tempt users or agents back toward protected-root editing
3. hook and skill guidance still treated bare `git worktree add` as a normal path even though the new boundary contract now requires local tooling rematerialization

## Why This Is A Narrow Follow-On

This should not reopen the completed owner:

- `I-20260401-1303-A-2` already closed the first project-local versus launch-time materialization split
- `I-20260402-0403-A` already reconciled canonical repo posture and bootstrap proof

The remaining gap is narrower:

1. extend the managed tool boundary contract from the project root into sibling worktrees
2. preserve the project root as the integration / merge surface instead of redefining it as non-writable storage only
3. make standard worktree entrypoints rematerialize the same local tool boundary surfaces even when `.gitignore` excludes them

## Problem

If Freely can create sibling worktrees automatically but tool boundaries do not follow that move, two bad outcomes remain likely:

- launchers or direct tool use fail to write in the sibling worktree and work drifts back into `develop`
- users have to remember tool-specific local config recovery by hand, which breaks the claimed managed boundary model

The current residual is therefore not a generic worktree feature request. It is a concrete gap in the already-frozen tool boundary contract.

## Boundary

Keep this follow-on narrow:

1. sibling `{project}-worktrees` bootstrap and local boundary rematerialization
2. per-tool distinction between:
   - tool-native project config
   - Freely wrapper-owned local boundary
   - launch-time `--add-dir` style boundary extension
3. standard entrypoints:
   - `freely init`
   - `freely sync-tooling`
   - `wt-create`
   - protected-branch `post-checkout` auto-worktree path
4. governance guidance that names `wt-create` as standard and treats raw `git worktree add` as manual fallback plus `sync-tooling`

Do not absorb:

1. new security-review capability families
2. generic sandbox policy redesign for every external tool
3. runtime manager / watchdog changes unrelated to tool boundary materialization
4. broad worktree ownership redesign beyond this boundary bootstrap contract

## Proposed Direction

Materialize a narrow follow-on owner under `freely-product-architecture`:

- keep the project root as the primary integration and merge surface
- add the sibling worktrees root as an explicit managed writable/trusted boundary extension where the tool supports it
- rematerialize project-local tool surfaces into new worktrees instead of assuming ignored or untracked files will be copied by Git
- make docs, hooks, and skills point at the managed path rather than normalizing raw `git worktree add`

Expected capability surface:

- `.freely/tool-boundary-bootstrap.md`
- `.freely/bin/*` wrappers
- `.codex/config.toml`
- `freely sync-tooling`
- `wt-create`
- `.githooks/post-checkout`

Expected proof:

- new sibling worktrees receive the managed local boundary surfaces automatically
- `iflow` launch-time args include the sibling worktrees root
- project root remains usable for read / merge / integration without being treated as the owner-development surface

## Current Judgement

This residual is worth its own owner because:

- it closes a real path back to protected-root implementation drift
- it is too broad to hide inside a one-line followthrough
- it is still much narrower than reopening the old tool-materialization umbrella
