# PRD: Fix scan import

## Problem
`task-lifecycle-scan.py` crashes with `ModuleNotFoundError` when trying to import `platform_adapter` because the file is named `platform-adapter.py` (hyphen breaks Python import).

## Solution
Replace `from platform_adapter import ...` with lazy importlib-based loading via `importlib.util.spec_from_file_location`.

## Scope
Only `docs/system/workspace/scripts/runtime/task-lifecycle-scan.py`

## Non-goals
- No changes to `platform-adapter.py` itself
- No changes to other consumers of platform-adapter
