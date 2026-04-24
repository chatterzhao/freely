# Tasks - runtime-closeout-selfhost-validation-followthrough-governance

1. Reuse a healthy same-project supervisor from `freely daemon start` instead of relaunching another detached runtime chain.
2. Clean ambiguous missing-state project start locks only when no runtime is actually active.
3. Fast-path the bounded closeout/self-host interruption prompts while preserving generic AI fallback for `codex` and `cc`.
4. Write the focused verification artifact and keep the owner bound to this checkpoint worktree.
5. Decide whether a guarded premerge replay can follow directly or whether one real-repo self-host replay is still needed first.
6. Keep exit-contract repair resumes anchored to the repair contract and the original cleanup closeout gate so retained cleanup followthrough cannot silently downgrade into a no-op completion receipt.
7. Ensure expected-running worker recovery syncs canonical tooling into retained worktrees before launching their local supervisor.
8. Keep valid manager cleanup resumes and newly delegated worker relaunches from inheriting stale exit-contract repair semantics after the retained cleanup lane has already advanced.
