# Issue: canonical-product-posture-bootstrap-reconciliation-governance

- issue_id: `I-20260402-0403-A`
- title: Canonical product posture bootstrap reconciliation governance
- phase_state: `completed`
- milestone: `M-20260326-freely-product-architecture`
- epic-name: `freely-product-architecture`
- story-name: `canonical-product-posture-bootstrap-reconciliation-governance`
- issue-name: `canonical-product-posture-bootstrap-reconciliation-governance`
- priority: P1
- source_candidate: `docs/pre-brainstorms/20260402-0403--canonical-product-posture-bootstrap-reconciliation/candidates.md#c-20260402-0403-a`
- source_brainstorm: `docs/pre-brainstorms/20260402-0403--canonical-product-posture-bootstrap-reconciliation/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/freely-product-architecture/canonical-product-posture-bootstrap-reconciliation-governance/pre-tests.md`
- progress_path: `docs/progress/freely-product-architecture/p-canonical-product-posture-bootstrap-reconciliation-governance.md`
- verification_artifact_dir: `docs/epics/freely-product-architecture/canonical-product-posture-bootstrap-reconciliation-governance/code-reviews`
- depends_on:
  - `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/issues/default-autonomy-activation-consent-and-tool-policy-governance.md`
  - `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/issues/freely-tool-autonomy-policy-materialization-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely already completed the product contract and the first tool-materialization slice, but canonical `develop` still carries legacy tracked bootstrap truth:

1. `.codex/config.toml` still says `approval_policy = "on-request"` even though `auto` posture is already canonical.
2. Canonical local bootstrap state still lacks activation-consent truth, so the canonical repo reports `activation_consent_status: unknown-legacy`.
3. `freely live-status` and `freely doctor` therefore still show execution-boundary audit failure on the canonical repo itself.

This owner reconciles canonical tracked `.codex/config.toml` plus canonical local bootstrap proof with already-completed contract truth. It does not redefine the contract.

## Scope

1. Reconcile canonical tracked Codex project posture with the completed `auto` materialization contract.
2. Reconcile canonical bootstrap-managed activation-consent truth with the completed product posture contract.
3. Verify that canonical `live-status` and `doctor` now pass the execution-boundary audit on the repo itself.
4. Write back this reconciliation as a narrow follow-on instead of reopening the completed product/tool owners.

## Non-Goals

1. Do not redesign `init` bootstrap, skip/force, or generic repo takeover semantics.
2. Do not redefine activation-consent wording or runtime escalation semantics.
3. Do not widen into supply-chain, artifact exposure, ACP, or workspace-routing changes.
4. Do not reopen completed owners `I-20260401-1303-A` or `I-20260401-1303-A-2`.

## Acceptance

1. Canonical tracked `.codex/config.toml` matches the already-canonical `auto` posture for project-local Codex materialization.
2. Canonical repo bootstrap produces activation-consent truth in a managed local config that satisfies the current execution-boundary audit.
3. `freely live-status --project <repo>` no longer reports `activation_consent_status=unknown-legacy`.
4. `freely live-status --project <repo>` no longer reports `codex_approval_policy=on-request expected=never`.
5. `freely doctor --project <repo>` passes on the canonical repo.
6. The owner remains a narrow bootstrap-reconciliation follow-on, not a reopened umbrella.

## Completion

- `docs/pre-brainstorms/20260402-0403--canonical-product-posture-bootstrap-reconciliation/brainstorms.md`
- `docs/pre-brainstorms/20260402-0403--canonical-product-posture-bootstrap-reconciliation/candidates.md`
- `docs/pre-brainstorms/INDEX.md`
- `docs/milestones.md`
- `docs/epics/freely-product-architecture/canonical-product-posture-bootstrap-reconciliation-governance/issues/canonical-product-posture-bootstrap-reconciliation-governance.md`
- `docs/epics/freely-product-architecture/canonical-product-posture-bootstrap-reconciliation-governance/brainstorms/b-canonical-product-posture-bootstrap-reconciliation-governance.md`
- `docs/epics/freely-product-architecture/canonical-product-posture-bootstrap-reconciliation-governance/prd.md`
- `docs/epics/freely-product-architecture/canonical-product-posture-bootstrap-reconciliation-governance/pre-tests.md`
- `docs/epics/freely-product-architecture/canonical-product-posture-bootstrap-reconciliation-governance/tasks.md`
- `docs/progress/freely-product-architecture/p-canonical-product-posture-bootstrap-reconciliation-governance.md`
- `.codex/config.toml`

## Verification

- `freely init --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260402-feature-canonical-product-posture-bootstrap-reconciliation --intent /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260402-feature-canonical-product-posture-bootstrap-reconciliation/docs/PROJECT_INTENT.md --constitution /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260402-feature-canonical-product-posture-bootstrap-reconciliation/docs/CONSTITUTION.md --ai codex:gpt-5.4:auto --accept-default-autonomy --force`
- `freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260402-feature-canonical-product-posture-bootstrap-reconciliation`
- `freely doctor --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260402-feature-canonical-product-posture-bootstrap-reconciliation`
- `freely init --project /Users/zhaoyu/Downloads/code/my-freely/freely --intent /Users/zhaoyu/Downloads/code/my-freely/freely/docs/PROJECT_INTENT.md --constitution /Users/zhaoyu/Downloads/code/my-freely/freely/docs/CONSTITUTION.md --ai codex:gpt-5.4:auto --accept-default-autonomy --force`
- `freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
- `freely doctor --project /Users/zhaoyu/Downloads/code/my-freely/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
- `./bin/governance-check`

## Next

- Once canonical repo posture truth is reconciled, further autonomy/consent drift should materialize as a new narrow follow-on only if it exceeds tracked posture plus local bootstrap proof.
