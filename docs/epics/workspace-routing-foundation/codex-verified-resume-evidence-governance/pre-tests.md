# Pre-tests: codex-verified-resume-evidence-governance

1. Reproduce the invalid target in an isolated worktree:
   - `codex exec resume <bad-session-id>` must fail with `no rollout found for thread id`
2. Freeze the field contract:
   - a cycle that ends with `session_id` but `jsonl_path=unavailable` is not sufficient resume evidence
3. Add a focused regression:
   - `observed session id + missing rollout/jsonl` must not select next-cycle `resume`
4. Preserve the healthy path:
   - valid rollout-backed `codex` resume evidence still selects `resume`
5. Preserve orthogonal behavior:
   - auth/watchdog recovery semantics remain unchanged by this issue

## Blocker Taxonomy

- `definition_missing`: the runtime evidence boundary is still ambiguous between observed, persistable, and resumable
- `commands_only`: reproduction exists only as ad hoc shell commands without a stable regression
- `evidence_plan_missing`: issue does not yet define how valid-vs-invalid resume evidence will both be tested
- `execution_pending_or_failed`: regression or isolation repro is not yet passing
