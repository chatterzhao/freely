# Issue: supply-chain-baseline-and-install-intake-audit-governance

- issue_id: `I-20260401-0115-A`
- title: Supply-chain baseline and install-intake audit governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `supply-chain-baseline-and-install-intake-audit-governance`
- issue-name: `supply-chain-baseline-and-install-intake-audit-governance`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260401-0115/candidates.md#c-20260401-0115-a`
- source_brainstorm: `docs/B1-docs/raw-20260401-0115/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/supply-chain-baseline-and-install-intake-audit-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-supply-chain-baseline-and-install-intake-audit-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/supply-chain-baseline-and-install-intake-audit-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/build-artifact-exposure-and-release-allowlist-audit-governance/issues/build-artifact-exposure-and-release-allowlist-audit-governance.md`
  - `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/issues/agent-execution-safety-review-and-security-decision-support.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely already turned artifact exposure and execution-boundary review into machine-enforced truth, but one real security baseline topic remains unmaterialized: supply-chain and install-intake hygiene. Right now there is no canonical audit for lockfile presence, risky direct dependency specifiers, install lifecycle hooks, or mutable GitHub Action refs.

This owner closes that narrow gap without reopening the broader security umbrella.

## Scope

1. Add a reusable supply-chain baseline audit script.
2. Fail when a repo with a root `package.json` lacks a recognized root lockfile.
3. Fail when direct dependency specifiers use disallowed non-registry sources:
   - `git+`
   - `github:`
   - `http:`
   - `https:`
   - `file:`
   - `link:`
4. Fail when package manifests define install-time lifecycle scripts unless the script name is explicitly allowlisted:
   - `preinstall`
   - `install`
   - `postinstall`
   - `prepare`
5. Carry a repo-scoped lifecycle allowlist file so exceptions are explicit instead of implicit.
6. Fail when GitHub Actions external `uses:` refs are not pinned to full commit SHAs.
7. Run the same audit from `freely doctor`.

## Non-Goals

1. Do not widen into minimum package age or provenance policy.
2. Do not implement transitive vulnerability scanning or external CVE intelligence.
3. Do not absorb artifact exposure, generalized secret scanning, or runtime-state remediation.
4. Do not redesign execution-boundary review or autonomy consent.

## Acceptance

1. A canonical audit script exists and is callable outside a single ad hoc shell session.
2. The audit passes on the current repo baseline.
3. The audit fails on missing root lockfile when `package.json` exists.
4. The audit fails on disallowed direct dependency sources.
5. The audit fails on install-time lifecycle scripts unless they are explicitly allowlisted.
6. The repo carries an explicit lifecycle allowlist file, even when it is empty by default.
7. The audit fails on mutable external GitHub Action refs.
8. `freely doctor` fails when the supply-chain audit fails and passes when the repo satisfies the baseline.

## Completion

- `docs/B1-docs/raw-INDEX.md`
- `docs/B1-docs/raw-20260401-0115/brainstorms.md`
- `docs/B1-docs/raw-20260401-0115/candidates.md`
- `docs/milestones.md`
- `docs/epics/workspace-routing-foundation/supply-chain-baseline-and-install-intake-audit-governance/issues/supply-chain-baseline-and-install-intake-audit-governance.md`
- `docs/epics/workspace-routing-foundation/supply-chain-baseline-and-install-intake-audit-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/supply-chain-baseline-and-install-intake-audit-governance/prd.md`
- `docs/epics/workspace-routing-foundation/supply-chain-baseline-and-install-intake-audit-governance/tasks.md`
- `docs/epics/workspace-routing-foundation/supply-chain-baseline-and-install-intake-audit-governance/brainstorms/b-supply-chain-baseline-and-install-intake-audit-governance.md`
- `docs/epics/workspace-routing-foundation/supply-chain-baseline-and-install-intake-audit-governance/code-reviews/20260401-supply-chain-baseline-and-install-intake-audit-verification.md`
- `docs/progress/workspace-routing-foundation/p-supply-chain-baseline-and-install-intake-audit-governance.md`
- `docs/system/workspace/install-lifecycle-allowlist.txt`
- `docs/system/workspace/scripts/quality/check-supply-chain-baseline`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-check-supply-chain-baseline`
- `docs/system/workspace/scripts/tests/test-freely-doctor-supply-chain-gate`
- `docs/system/workspace/scripts/tests/test-freely-doctor-execution-boundary-audit`
- `docs/system/workspace/scripts/tests/test-freely-hook-gate`
- `docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
- `docs/system/workspace/tools.md`
- `bin/check-supply-chain-baseline`
- `package.json`

## Verification

- `bash docs/system/workspace/scripts/tests/test-check-supply-chain-baseline`
- `bash docs/system/workspace/scripts/tests/test-freely-doctor-supply-chain-gate`
- `bash docs/system/workspace/scripts/tests/test-freely-doctor-execution-boundary-audit`
- `bash docs/system/workspace/scripts/tests/test-freely-hook-gate`
- `bash docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
- `./bin/governance-check`

## Next

- This owner stays intentionally narrow: baseline lockfile, direct dependency intake, explicit lifecycle allowlist enforcement, workflow pinning, and doctor enforcement only.
- Follow-on owners should absorb minimum package age, provenance, transitive scanning, and broader remediation rather than stretching this owner into another umbrella.
- Merged to `develop` via commit `1d082fc`, and closeout writeback now records the owner as completed.
