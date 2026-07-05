# Issue: cc-acp-init-autonomy-consent-test-followthrough-governance

- issue_id: `I-20260401-2316-A`
- title: CC ACP init autonomy consent test followthrough governance
- phase_state: `completed`
- milestone: `M-20260326-freely-product-architecture`
- epic-name: `freely-product-architecture`
- story-name: `cc-acp-init-autonomy-consent-test-followthrough-governance`
- issue-name: `cc-acp-init-autonomy-consent-test-followthrough-governance`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260401T224500Z/candidates.md#c-20260401-2316-a`
- source_brainstorm: `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- reopen_of_issue: `docs/B2-docs/config/packaging/issues/freely-tool-autonomy-policy-materialization-governance.md`
- reopen_reason: `canonical cc:auto ACP init now requires --accept-default-autonomy, but test-freely-init-cc-config still used the old invocation`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/config/packaging/pre-tests.md`
- progress_path: `docs/progress/freely-product-architecture/p-cc-acp-init-autonomy-consent-test-followthrough-governance.md`
- verification_artifact_dir: `docs/B2-docs/config/packaging/code-reviews`
- depends_on:
  - `docs/B2-docs/config/packaging/issues/freely-tool-autonomy-policy-materialization-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

`I-20260401-1303-A-2` already froze the activation-consent and tool materialization contract for `cc:auto`. The remaining failure on canonical `develop` is not a new product question; it is a stale test invocation on the `cc:auto + --tool-adapter acp` init path.

Because the develop merge gate requires every develop-bound replay to remain candidate-driven, this followthrough needs its own narrow owner instead of silently editing a completed-family surface.

## Scope

1. Repair the stale `cc:auto + --tool-adapter acp` test invocation by adding `--accept-default-autonomy`.
2. Materialize the minimum candidate / issue / progress / verification lifecycle needed for develop-bound replay.
3. Explicitly classify this as a followthrough of the already-canonical tool materialization family.

## Non-Goals

1. Do not change `freely init` runtime behavior.
2. Do not expand ACP support or adapter semantics.
3. Do not reopen the broader `I-20260401-1303-A-2` owner.
4. Do not reinterpret activation consent as optional again.

## Acceptance

1. The reopen is documented as a narrow followthrough of `I-20260401-1303-A-2`.
2. `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config` passes with the canonical consent contract.
3. `./bin/governance-check` passes after lifecycle writeback.
4. The owner remains test-only and does not claim runtime semantic change.

## Completion

- `docs/B1-docs/raw-INDEX.md`
- `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- `docs/B1-docs/raw-20260401T224500Z/candidates.md`
- `docs/milestones.md`
- `docs/B2-docs/config/packaging/brainstorms/b-cc-acp-init-autonomy-consent-test-followthrough-governance.md`
- `docs/B2-docs/config/packaging/issues/cc-acp-init-autonomy-consent-test-followthrough-governance.md`
- `docs/B2-docs/config/packaging/prd.md`
- `docs/B2-docs/config/packaging/pre-tests.md`
- `docs/B2-docs/config/packaging/tasks.md`
- `docs/B2-docs/config/packaging/code-reviews/20260401-cc-acp-init-autonomy-consent-test-followthrough-verification.md`
- `docs/progress/freely-product-architecture/p-cc-acp-init-autonomy-consent-test-followthrough-governance.md`
- `docs/system/workspace/scripts/tests/test-freely-init-cc-config`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
- `./bin/governance-check`

## Completion Status

- canonical_merge_commit: `d5b7080`
- canonical_merge_target: `develop`
- post_merge_acceptance:
  - `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
  - `./bin/governance-check`

## Next

- Closed on canonical `develop`.
- Any future stale tool-materialization fixture should reopen as a new narrow owner rather than widening this followthrough.
