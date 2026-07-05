# Verification: project-level-agents-bootstrap-and-management-contract-governance

- issue_id: `I-20260405-1130-A`
- reviewer: `codex`
- date: `2026-04-05`
- disposition: `pass_for_verification`

## Scope

Verify the first reusable capability-contract slice for project-level `AGENTS.md`: create when missing, preserve when present, read project root first, and treat self-hosting as the same contract.

## Checks

1. Confirmed `docs/system/workspace/project-agents-contract.md` freezes the project-level AGENTS contract.
2. Confirmed the contract states that `freely init` only creates `AGENTS.md` when missing and preserves an existing file.
3. Confirmed the contract states that runtime reads `<project-root>/AGENTS.md` before reusable workspace capability docs and that self-hosting follows the same rule.
4. Ran:
   - `bash docs/system/workspace/scripts/tests/test-freely-init-preserves-existing-agents-md`
   - `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
   - `bash docs/system/workspace/scripts/tests/test-freely-init-ai-default-precedence`
   - `./bin/governance-check`

## Result

- pass: the project-level AGENTS behavior is now reusable capability truth rather than only an implicit runtime detail
- pass: existing `AGENTS.md` preservation is covered by a focused regression
- pass: the owner remains narrow and does not widen into richer template customization or migration behavior

## Residual Risk

- richer template generation, update/merge flow, or project-intent injection is still unresolved and should reopen as a narrower follow-on instead of silently expanding this slice
