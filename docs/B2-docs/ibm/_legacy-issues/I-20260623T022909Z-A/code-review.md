# Code Review

## Implementation Decision Note
- **Pattern**: Lazy importlib loader (`_get_pa()`) cached as module-level singleton
- **Why not rename the file**: Renaming would break all scripts that call it by path
- **Why not symlink**: Adds deployment complexity, fragile
- **Alternative considered**: `importlib.import_module()` with path manipulation — more complex, less readable

## Verification
- [x] `_get_pa()` returns the module on first call and caches it
- [x] All three call sites updated (lines 19, 438, 474)
- [x] No changes to other files
- [x] Commit `2b2f4c77f` contains only the intended changes

## Risks
None. Importlib is in Python stdlib.
