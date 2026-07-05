# B1 Brainstorm: scan-import-fix

## Discovery
`task-lifecycle-scan.py` cannot import `platform-adapter` module because the file uses a hyphen in its name (`platform-adapter.py`) while Python imports require valid identifiers. Direct `from platform_adapter import ...` fails with `ModuleNotFoundError`.

## Research
- File: `docs/system/workspace/scripts/sync/platform-adapter.py`
- All other scripts in the repo reference it by direct path call (`python3 .../platform-adapter.py ...`), not as an imported module
- `task-lifecycle-scan.py` is the only consumer that tries `from platform_adapter import ...`
- Fix confirmed via importlib: `importlib.util.spec_from_file_location` works correctly

## Decision
Proceed to candidate. The fix is already implemented and committed; governance is post-hoc per fix skill convention.
