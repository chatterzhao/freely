# Tasks: sensitive-local-artifact-ignore-governance

1. Freeze IBM
- Keep the first slice limited to common miswritten local sensitive artifacts.
- Decide the narrow ignore set for root credential files and cert/key extensions.
- Keep future fixture carve-outs as explicit follow-up exceptions, not implicit broad allowances.

2. Add regression first
- Add a focused `git check-ignore --no-index` regression for the protected paths.
- Prove a normal repository path is not ignored.

3. Implement the narrow repair
- Update `.gitignore` with the minimal agreed rules.
- Remove the stray root `auth.json` from `develop`.

4. Verify
- Run the focused regression.
- Run `./bin/governance-check`.
- Recheck `develop` worktree hygiene.
