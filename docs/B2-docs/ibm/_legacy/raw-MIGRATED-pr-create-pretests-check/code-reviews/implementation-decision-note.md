# Code Review: I-20260624T152500Z-A

- issue_id: I-20260624T152500Z-A

## Implementation Decision Note

**Decision**: Add Step 2c to pr-create-guarded that calls pretests-retirement-gate before allowing PR creation. The check mirrors the exact pattern from wt-close (lines 320-346) using `--project` and `--worktree-path` flags.

**Rationale**:
- Consistency: Same gate script, same arguments, same error handling as wt-close
- Early detection: Catches untested code at PR creation time, not at worktree close time
- Graceful degradation: Skips the check if pretests-retirement-gate binary is missing

**Key change**: The script passes `$ROOT_DIR` (current worktree) as both `--project` and `--worktree-path`. This differs from wt-close which uses the primary worktree for `--project`. Rationale: during development, governance files live in the worktree alongside code changes, so the worktree root is the correct project root.

## Files Modified
- `docs/system/workspace/scripts/worktree/pr-create-guarded`: Added 42 lines for Step 2c

## Verification
- `bash -n` syntax check: PASS
- `pretests-retirement-gate --project <worktree> --worktree-path <worktree>`: exit 0 PASS
- Error message contains `freely-test-execution` skill reference and `pr-create-guarded` command name: PASS
