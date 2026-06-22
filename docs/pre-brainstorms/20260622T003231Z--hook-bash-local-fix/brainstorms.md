# Brainstorm: Fix pre-push.sh local keyword for macOS bash compat

## Discovery
`docs/system/workspace/hooks/pre-push.sh` line 13 uses `local` keyword outside a bash function. On macOS bash 3.x (pre-Homebrew), `local` is only valid inside functions, causing immediate hook failure under `set -euo pipefail`.

## Impact
- ALL git push operations to gitee fail
- wt-close remote branch deletion blocked
- Discovered during Manager patrol when trying to clean up merged branches

## Solution
Replace `local` declarations with plain variable assignments. Two occurrences on lines 13 and 19.

## Existing coverage
No existing I-* issue covers pre-push hook bash compatibility.
No duplicate pre-brainstorm found.

## Decision
Proceed to candidate.
