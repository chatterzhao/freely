# Brainstorm: runtime-startup-authority-and-readiness-governance

- issue_id: `I-20260413-0420-A`
- date: `2026-04-13`
- source_candidate: `docs/B1-docs/raw-20260413T020800Z/candidates.md#c-20260413-0420-a`

## Problem slice

The startup defect was reduced to one bounded execution seam:

1. supervisor identity and startup readiness were still inferred from PID resemblance
2. launch truth was published too late relative to start-lock release
3. daemon-ready semantics consumed the same weak heuristic
4. stop cleanup still had to distinguish authoritative siblings from ghost hints

## Chosen shape

1. Publish a runtime-owned supervisor identity file per active launch.
2. Make supervisor validation require both project ownership and identity truth.
3. Let `manager_supervisor_pid_for_project()` resolve only authoritative supervisors.
4. Hold the same-project start lock until startup truth is durably published.
5. Gate `daemon start` ready on startup truth rather than on the mere presence of a pid.
6. Narrow stop-marker preservation to authoritative supervisors.

## Rejected shortcuts

1. Do not keep argv matching as authority with just more filtering.
2. Do not solve daemon false-ready by sleeping longer.
3. Do not widen this owner into the manager continuity contract.
4. Do not preserve old tests that model supervisors purely by fake argv when the runtime contract now requires published authority.
