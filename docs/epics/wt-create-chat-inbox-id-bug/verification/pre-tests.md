# Pre-Tests

## Acceptance Items

- [ ] wt-create --source chat-inbox completes without ID mismatch
- [ ] All 4 call sites use `$ts_bare` (tr -d 'TZ') for chat-inbox.py --id
- [ ] No regression in --source platform or --source local paths
- [ ] phase_state tests: raw-issue created with absorbed phase_state
- [ ] Worktree + test-pre-merge both created correctly

### V2 Adequacy

| Field | Value |
|-------|-------|
| adequacy_version | v2 |
| acceptance_items_count | 5 |
| covers_fix_scope | yes |
| covers_regression | yes |
| covers_state_transition | yes |
