# Code Review: ibm-pretests-executable-acceptance-quality-governance
- issue_id: `I-20260326-1815`

- date: `2026-03-26`
- reviewer: `codex`
- scope:
  - `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
  - `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
  - `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
  - `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
  - `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/*`

## Findings

- No blocking findings.

## Verification

- `./bin/governance-check`
- reviewed the updated IBM truth sources to confirm they now require:
  - executable acceptance instead of wording-review-only pre-tests
  - `environment` / `evidence` / `failure signal` / `failure handling / replay expectation`
  - default post-merge coverage for integration, application-native real-environment, and end-to-end dogfood acceptance on Freely autonomy issues

## Conclusion

The IBM quality bar is now materially harder to satisfy with weak `pre-tests.md` wording alone. The updated truth sources preserve the existing integration-acceptance-first direction while adding explicit recoverable acceptance structure and default dogfooding/runtime coverage expectations.
