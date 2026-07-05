# 候选：cc-acp-init-autonomy-consent-test-followthrough

- id: `C-20260401T231600Z-A`
- candidate_format_version: `v2`
- title: Align the `cc:auto + adapter=acp` init regression test with the canonical activation-consent contract
- source_brainstorm: `docs/B1-docs/raw-20260401-2316/brainstorms.md`
- reopen_of_issue: `docs/B2-docs/config/packaging/issues/freely-tool-autonomy-policy-materialization-governance.md`
- reopen_reason: `test-freely-init-cc-config still called the canonical cc:auto ACP init path without --accept-default-autonomy after activation consent became mandatory`
- problem: canonical `develop` still carries one stale test invocation on the `cc:auto + --tool-adapter acp` init path, so the test now fails even though runtime behavior already matches the frozen activation-consent contract.
- why_now:
  - the fix is already known and code-complete, but the develop merge hook correctly refuses candidate-less closeout patches
  - this is too narrow to reopen the broader tool materialization owner, yet too governance-relevant to merge without lifecycle evidence
  - keeping the regression red would make canonical `develop` disagree with the already-frozen autonomy consent truth
- acceptance_criteria:
  - a new narrow lifecycle records this as completed-family followthrough rather than silent drift
  - `test-freely-init-cc-config` passes with the canonical `--accept-default-autonomy` contract on the `cc:auto + adapter=acp` path
  - no runtime behavior changes are introduced
  - milestone / issue / progress / verification artifacts are sufficient for a develop-bound replay
- promotion_gate:
  - keep scope limited to test and lifecycle writeback
  - attach to the tool materialization family, not the broader security-review capability family
  - do not reopen runtime semantics that are already canonical
- open_questions:
  - none; the runtime contract is already frozen and only the stale fixture needs alignment
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `This is a strict followthrough patch: one stale test invocation lagged behind the already-canonical activation-consent contract for cc:auto ACP init.`
    verdict: `ready_for_ibm`
- priority: `P0`
- status: `promoted`
- decision_reason:
  - the failing test belongs to tool autonomy policy materialization, not a new runtime feature family
  - a fresh candidate / issue is the smallest compliant path through the develop merge gate
  - the owner stays narrow enough to close immediately after develop absorption
- milestone: `M-20260326-freely-product-architecture`
- promoted_issue_path: `docs/B2-docs/config/packaging/issues/cc-acp-init-autonomy-consent-test-followthrough-governance.md`
- promoted_issue_path_role: `primary-owner`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - `I-20260401T231600Z-A` owns the one-line regression repair plus the minimal develop-bound writeback required to absorb it.
- revisit_trigger:
  - reopen only if canonical `develop` still shows additional stale fixtures after this ACP init path is repaired

