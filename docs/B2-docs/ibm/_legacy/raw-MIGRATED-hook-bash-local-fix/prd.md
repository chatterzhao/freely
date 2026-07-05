# PRD: Fix pre-push.sh local keyword for macOS bash compat

## Problem
`docs/system/workspace/hooks/pre-push.sh` uses `local` keyword outside a bash function. On macOS bash 3.x, `local` is only valid inside functions, causing immediate hook failure under `set -euo pipefail`. This blocks ALL gitee push operations.

## Success Criteria
1. `git push` to gitee origin no longer fails with "local: can only be used in a function" error
2. `wt-close --force` can delete remote branches on gitee
3. All existing pre-push hook functionality preserved (branch deletion guard, owner commit protection)
