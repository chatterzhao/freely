# Tasks

## T1: Fix chat-inbox ID normalization in _pull_raw_issue
- File: `docs/system/workspace/scripts/worktree/wt-create`, lines 309, 313
- Change: `--id "$ts"` → `--id "$ts_bare"`
- Status: done (committed 1f6a60340)

## T2: Fix chat-inbox ID normalization in _require_issue_exists
- File: `docs/system/workspace/scripts/worktree/wt-create`, line 451
- Change: Add `ts_bare` computation, `--id "$ts"` → `--id "$ts_bare"`
- Status: done (committed 1f6a60340)

## T3: Fix chat-inbox ID normalization in _materialize_chat_if_needed
- File: `docs/system/workspace/scripts/worktree/wt-create`, line 565
- Change: `--id "$ts"` → `--id "$ts_bare"`
- Status: done (committed 1f6a60340)

## T4: B1_IBM governance
- Files: pre-brainstorms, milestones.md
- Status: done

## T5: B2_IBM governance
- Files: I-* issue, prd.md, pre-tests.md, tasks.md, code-review
- Status: done

## T6: PR creation and merge
- Command: pr-create-guarded → pr-review-guarded → pr-merge-guarded
- Status: pending
