# Tasks: wt-close raw-{key} param + help

- issue_id: I-20260629T160852Z-A

## Task List

### T-001: Add raw key → branch resolution
- status: done
- description: After arg parsing, detect raw-YYYYMMDDTHHMMSSZ format input and resolve to fix/feature branch via git branch --list

### T-002: Update usage() help text
- status: done
- description: Emphasize fix|feature branch input, document raw key support, explain test-pre-merge auto-cleanup

### T-003: Verify backward compatibility
- status: done
- description: Ensure existing branch name input and _resolve_branch() still work
