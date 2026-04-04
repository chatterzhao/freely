# Verification: build-artifact-exposure-and-release-allowlist-audit-governance

- issue_id: `I-20260401-2245-A`
- issue_path: `docs/epics/workspace-routing-foundation/build-artifact-exposure-and-release-allowlist-audit-governance/issues/build-artifact-exposure-and-release-allowlist-audit-governance.md`
- verification_date: `2026-04-01`
- verification_scope: `focused regression + repo build replay`

## Verified Outcomes

1. A canonical build artifact audit now exists at `docs/system/workspace/scripts/quality/check-build-artifact-exposure` and is exposed via `bin/check-build-artifact-exposure`.
2. The audit rejects forbidden release-facing artifacts such as `.map` and `.env*`.
3. The audit rejects output files that are not explicitly allowlisted by `docs/system/workspace/release-build-allowlist.txt`.
4. `freely doctor` now runs the build artifact audit when build output exists.
5. The repo `build` path runs the audit immediately after `vite build`.
6. Production sourcemap posture is explicit in `vite.config.ts` via `build.sourcemap: mode !== "production"`.

## Commands

```bash
bash docs/system/workspace/scripts/tests/test-build-artifact-exposure-audit
bash docs/system/workspace/scripts/tests/test-freely-doctor-build-artifact-exposure-gate
bash docs/system/workspace/scripts/tests/test-freely-hook-gate
bash docs/system/workspace/scripts/tests/test-freely-chat-and-tui
bun install
bun run build
./bin/governance-check
./bin/pretests-gate --staged-only
```

## Evidence

1. `test-build-artifact-exposure-audit` passed and confirmed forbidden artifact rejection plus explicit allowlist enforcement.
2. `test-freely-doctor-build-artifact-exposure-gate` passed and confirmed `doctor` fails on dirty output and passes on clean allowlisted output.
3. `test-freely-hook-gate` still passed after the new `doctor` audit was introduced, after aligning the test fixture with the existing activation-consent requirement.
4. `test-freely-chat-and-tui` passed, showing the new audit did not regress chat/bootstrap behavior.
5. `bun run build` completed successfully and ended with `build artifact audit PASS`, proving the repo build path now enforces the audit.
6. `./bin/governance-check` passed with only the existing legacy naming warnings.
7. `./bin/pretests-gate --staged-only` passed.

## Residual Risks

1. This owner intentionally does not absorb broader supply-chain policy, generalized secret scanning outside build output, or external SaaS scanners.
2. Repos without build output continue to skip this audit in `doctor`; that is intentional for this slice and avoids pretending every repo is a frontend build target.

## Implementation Decision Note

- decision: legacy: completed verification artifact
- why_this: legacy: no detailed record
- alternatives_considered: legacy: no detailed record
- boundary_non_goals: legacy: no detailed record
- residual_risk: legacy: no detailed record
