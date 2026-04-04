# Brainstorm: worktree-tool-boundary-bootstrap-governance

## Focus

Freeze the smallest implementation-bearing follow-on that keeps managed tool boundaries consistent across:

1. project root bootstrap
2. sibling worktree creation
3. launch-time writable-root extension for tools that need it

## Narrowing Decisions

1. Keep `codex` on its verified tool-native project config surface.
2. Keep `iflow`, `claude`, and similar tools on wrapper plus launch-time boundary extension unless a verified project-local surface exists.
3. Treat `freely sync-tooling` as the canonical rematerialization primitive.
4. Treat `wt-create` plus protected-branch auto-worktree as managed entrypoints that must call the rematerialization primitive.

## Excluded

1. No new user-home config management.
2. No generic sandbox redesign.
3. No change to the meaning of protected roots: they remain integration surfaces, not owner-development surfaces.
