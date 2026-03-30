# Pre-tests: sensitive-local-artifact-ignore-governance

1. Freeze the field fact:
   - `develop` had a real root `auth.json`
   - the repo had no ignore rule for it
2. Freeze the proposed narrow contract:
   - root `auth.json` must be ignored
   - root package/auth filenames defined by the issue must be ignored
   - common private-key/certificate extensions defined by the issue must be ignored
3. Prove no immediate repo conflict:
   - the repository does not already track files that would be silently hidden by the new patterns
4. Add a focused regression:
   - use `git check-ignore --no-index`
   - prove the protected paths are ignored
   - prove a normal repository path is still not ignored
5. Keep the fix narrow:
   - do not expand into credential-storage redesign
   - do not require real login, switch, or slot deletion

## Blocker Taxonomy

- `definition_missing`: the ignore surface is still too broad or too vague
- `conflict_found`: the proposed patterns would hide an existing tracked fixture or capability asset
- `commands_only`: only ad hoc shell proof exists and no regression has been added yet
- `execution_pending_or_failed`: the regression or governance check is not yet passing
