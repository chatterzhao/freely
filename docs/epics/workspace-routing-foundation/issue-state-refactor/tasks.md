# Tasks — issue state refactor

- issue_id: I-20260505T1210Z-A-B

## task-1: cmd_close fix
- status: done
- owner: feature/raw-20260505T1210Z-issue-state-refactor-B
- changes: bin/issue-sync line 540: _fm_set_str platform_state closed

## task-2: cmd_create fix
- status: done
- owner: feature/raw-20260505T1210Z-issue-state-refactor-B
- changes: bin/issue-sync line 424: _fm_set_str platform_state open

## task-3: cmd_promote fix
- status: done
- owner: feature/raw-20260505T1210Z-issue-state-refactor-B
- changes: bin/issue-sync line 626: status→phase_state absorbed
