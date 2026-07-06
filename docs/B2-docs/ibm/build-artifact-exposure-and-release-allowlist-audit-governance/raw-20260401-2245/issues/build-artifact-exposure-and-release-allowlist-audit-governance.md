# Issue: build-artifact-exposure-and-release-allowlist-audit-governance

- issue_id: `I-20260401-2245-A`
- title: Build artifact exposure and release allowlist audit governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `build-artifact-exposure-and-release-allowlist-audit-governance`
- issue-name: `build-artifact-exposure-and-release-allowlist-audit-governance`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260401T224500Z/candidates.md#c-20260401-2245-a`
- source_brainstorm: `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: docs/B2-docs/ibm/build-artifact-exposure-and-release-allowlist-audit-governance/raw-20260401-2245/verification/pre-tests.md
- progress_path: `docs/progress/workspace-routing-foundation/p-build-artifact-exposure-and-release-allowlist-audit-governance.md`
- verification_artifact_dir: docs/B2-docs/ibm/build-artifact-exposure-and-release-allowlist-audit-governance/raw-20260401-2245/code-reviews
- depends_on:
  - `docs/B2-docs/config/packaging/raw-20260402-0403issues/default-autonomy-activation-consent-and-tool-policy-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely has already converged on a broader security direction: automation and enforced workflow should replace operator memory wherever possible. But the current repo still has a very practical gap:

1. build output can exist without a canonical forbidden-artifact scan,
2. there is no explicit release allowlist for output files,
3. `doctor` does not audit build artifact exposure at all, and
4. production sourcemap posture is still implicit rather than written into build truth.

This owner fixes that first concrete gap without pretending to solve the entire security baseline.

## Scope

1. Add a reusable build artifact exposure audit script.
2. Define a repo-scoped release allowlist consumed by that audit.
3. Fail on obviously forbidden release-facing artifacts such as:
   - `.map`
   - `.env*`
   - common secret / credential / certificate files
4. Run the audit from `freely doctor` when build output exists.
5. Run the audit from the current repo build path so release-facing builds fail early.
6. Make the current repo production sourcemap posture explicit in build config.

## Non-Goals

1. Do not widen this owner into full supply-chain policy.
2. Do not implement full runtime secret scanning across continuity, prompts, and logs.
3. Do not bind the first slice to any external SaaS scanner.
4. Do not redesign the broader execution-boundary review capability already owned by `I-20260401-1308-A`.

## Acceptance

1. A canonical audit script exists and is callable outside a single ad hoc shell session.
2. The audit rejects forbidden release-facing artifacts in the build output.
3. The audit also rejects output files that are not explicitly allowlisted.
4. `freely doctor` fails when the build artifact audit fails and passes when the output matches the allowlist.
5. The repo build path runs the audit automatically.
6. The repo build config explicitly states production sourcemap posture.

## Completion

- `docs/B1-docs/raw-INDEX.md`
- `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- `docs/B1-docs/raw-20260401T224500Z/candidates.md`
- `docs/milestones.md`
- `docs/B2-docs/ibm/build-artifact-exposure-and-release-allowlist-audit-governance/issues/build-artifact-exposure-and-release-allowlist-audit-governance.md`
- `docs/B2-docs/ibm/build-artifact-exposure-and-release-allowlist-audit-governance/pre-tests.md`
- `docs/B2-docs/ibm/build-artifact-exposure-and-release-allowlist-audit-governance/code-reviews/20260401-build-artifact-exposure-and-release-allowlist-verification.md`
- `docs/progress/workspace-routing-foundation/p-build-artifact-exposure-and-release-allowlist-audit-governance.md`
- `docs/system/workspace/release-build-allowlist.txt`
- `docs/system/workspace/scripts/quality/check-build-artifact-exposure`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-build-artifact-exposure-audit`
- `docs/system/workspace/scripts/tests/test-freely-doctor-build-artifact-exposure-gate`
- `bin/check-build-artifact-exposure`
- `package.json`
- `vite.config.ts`

## Verification

- `bash docs/system/workspace/scripts/tests/test-build-artifact-exposure-audit`
- `bash docs/system/workspace/scripts/tests/test-freely-doctor-build-artifact-exposure-gate`
- `bash docs/system/workspace/scripts/tests/test-freely-hook-gate`
- `bash docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
- `./bin/governance-check`

## Next

- This owner keeps the first slice narrow: artifact exposure, allowlist, doctor/build enforcement, and explicit production sourcemap posture.
- Follow-on capability owners should absorb wider secret scanning, supply-chain policy, and incident remediation rather than widening this owner into another umbrella.
