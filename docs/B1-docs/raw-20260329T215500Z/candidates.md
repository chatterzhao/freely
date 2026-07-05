# Candidates - 20260329-2155--sensitive-local-artifact-ignore-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260329T215500Z-A: legacy issue
- candidate_format_version: v2
- title: Ignore common miswritten local sensitive artifacts before they can enter Git
- problem: A real repository-root `auth.json` containing live credential structure was observed in `develop`, and the repository had no ignore rule for it or other common local credential/private-key artifacts. That means Freely can surface sensitive local byproducts as ordinary untracked files even though they are not valid repository assets.
- why_now: This is no longer hypothetical. A live root `auth.json` had to be manually removed from `develop`, and current `.gitignore` only protected `.env*`. The smallest safe follow-up is to freeze a narrow ignore contract before the same class of file is accidentally staged or committed.
- acceptance_criteria:
  - repository-root `auth.json` is ignored by default
  - common local credential filenames and private-key/certificate extensions defined by the issue are ignored by default
  - the contract is covered by a focused regression using `git check-ignore --no-index`
  - the ignore set stays narrow enough that future tracked fixtures can still be restored with explicit exceptions
  - `develop` no longer carries the stray sensitive file
- promotion_gate:
  - prove the root sensitive file really existed and was not a fixture
  - prove the current repo has no conflicting tracked files for the proposed patterns
  - keep the first slice limited to ignore governance, not credential storage redesign
- open_questions:
  - should package-manager auth files such as `.npmrc` remain root-only ignores while certificate extensions stay repo-wide
  - should future fixture paths get predeclared explicit unignore carve-outs, or only when the first real fixture appears
  - should this issue later expand into a broader sensitive-local-artifact hygiene policy for generated tool state
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The field fact is concrete: a real root auth.json appeared, and the repo had no ignore guard for it. The repair can stay narrow, testable, and independent from account-runtime behavior.`
    verdict: `ready_for_ibm`
- priority: P2
- status: promoted
- decision_reason: The problem is real, low-level, and easy to make worse if handled ad hoc. A dedicated issue lets us freeze a conservative ignore contract and verify it without conflating this line with login, slot, or runtime recovery work.
- promoted_issue_path: `docs/B2-docs/ibm/sensitive-local-artifact-ignore-governance/issues/sensitive-local-artifact-ignore-governance.md`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- next_action: Materialize an owner issue, add a focused ignore regression, and land the minimal `.gitignore` contract.
- revisit_trigger: Reopen this line if a future fixture requires tracked cert/key material or if more sensitive local artifact families appear that the narrow rule set does not cover.
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
