# Tasks: ai-auth-change-wake-command-lifecycle-governance

1. Freeze IBM
- Decide whether post-success wake becomes async, bounded-sync, or sync-with-suppression for specific callers.
- Decide whether no-op switch skips notify entirely.
- Decide where re-entrancy is cut: `ai-cli`, `freely auth-change-wake`, watchdog slot switch path, or a combination.
- Keep `login` outside the first implementation slice unless non-login evidence proves the same contract safely.

2. Add regressions first
- Add a focused regression for no-op switch exit semantics.
- Add a focused regression for wake re-entrancy suppression.
- Add a focused regression showing watchdog auth recovery still works.

3. Implement the narrow repair
- Change only the success-path wake lifecycle and the minimal re-entrancy guard surface required by the tests.
- Do not expand into login UX redesign, slot deletion, or general process cleanup work.

4. Verify with real commands
- Replay `ai list`, `whoami`, `status`.
- Replay no-op `ai switch` with bounded process-tree observation.
- Avoid real `login` and slot deletion in the first verification pass.
