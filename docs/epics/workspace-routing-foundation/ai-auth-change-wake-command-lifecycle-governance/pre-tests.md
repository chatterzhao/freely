# Pre-tests: ai-auth-change-wake-command-lifecycle-governance

1. Freeze the field contract:
   - `ai list/whoami/status` exit normally, while `ai switch` success-path can remain alive behind synchronous `auth-change-wake`
2. Reproduce the narrowest real failure:
   - no-op `ai switch codex <current-slot>` prints success and still remains alive after a bounded wait
3. Inspect the process tree:
   - the stuck parent is `ai-cli`
   - the immediate child is `freely auth-change-wake --reason switch_success`
4. Add a focused regression:
   - success-path wake must not keep `ai switch` alive indefinitely
5. Add a focused re-entrancy regression:
   - watchdog-triggered slot handling must not recurse through the same notify loop forever
6. Preserve orthogonal behavior:
   - manager/watchdog auth recovery still works
7. Preserve test safety:
   - do not require real `login`
   - do not require slot deletion

## Blocker Taxonomy

- `definition_missing`: exit semantics or wake acknowledgement policy is still ambiguous
- `repro_gap`: no stable no-op switch reproduction exists
- `reentrancy_gap`: issue does not yet define where recursion must be cut, or whether the full closed loop is still only a high-confidence hypothesis
- `commands_only`: only ad hoc shell evidence exists and no regression has been added yet
- `execution_pending_or_failed`: focused tests are not yet passing
