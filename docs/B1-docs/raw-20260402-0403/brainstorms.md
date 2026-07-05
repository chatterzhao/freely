# Brainstorms - 20260402-0403--canonical-product-posture-bootstrap-reconciliation

## Context

`I-20260401-1303-A` and `I-20260401-1303-A-2` already froze Freely's product contract:

- default `auto` posture is unattended and automatic-approval
- activation consent is the blocking posture gate
- project-local Codex materialization for `auto` writes `approval_policy = "never"`

However, canonical `develop` still does not satisfy that already-frozen truth:

- `.codex/config.toml` still carries `approval_policy = "on-request"`
- canonical local bootstrap state still lacks activation-consent truth
- `freely live-status --project <repo>` therefore reports `execution_boundary_audit_status: fail`

This is no longer a contract-definition gap. It is a bootstrap/materialization reconciliation gap on the canonical repo itself.

## Why This Is Not A Reopen

This should not reopen either completed owner:

- `I-20260401-1303-A` completed the product contract
- `I-20260401-1303-A-2` completed the first materialization slice and explicitly says future drift should materialize as a narrower follow-on

The remaining problem is narrower:

1. align tracked canonical repo posture plus local bootstrap proof with already-canonical product truth
2. prove the canonical repo now passes its own execution-boundary audit
3. avoid widening back into generic init/bootstrap redesign

## Problem

Freely now has an execution-boundary audit and a security review brief, but the canonical repo itself still fails them for historical reasons. That creates a misleading state:

- the capability is "completed"
- but the canonical project posture still looks legacy

This weakens dogfooding and makes the completed owners look less finished than they actually are.

## Boundary

This lane should stay narrow:

1. tracked project-local Codex posture for the canonical repo
2. bootstrap-managed activation-consent truth for the canonical repo
3. focused verification that `freely doctor` / `live-status` now pass on canonical `develop`

This lane should not absorb:

1. broader `init` skip/force/bootstrap redesign
2. new security-review capability semantics
3. new ACP or adapter work
4. wider repo hygiene unrelated to the execution-boundary audit

## Proposed Direction

Materialize a narrow follow-on owner under `freely-product-architecture`:

- keep the already-frozen product contract unchanged
- keep the already-frozen tool-materialization contract unchanged
- only reconcile canonical tracked posture and canonical bootstrap proof with those contracts

Expected file surface:

- `.codex/config.toml`
- milestone / issue / progress / verification writeback

Expected runtime evidence:

- `freely live-status --project <repo>` no longer reports `activation_consent_status=unknown-legacy`
- `freely live-status --project <repo>` no longer reports `codex_approval_policy=on-request expected=never`
- `freely doctor --project <repo>` passes on the canonical repo

## Open Questions

1. Should canonical activation consent be recorded through a one-time managed bootstrap with an explicit `recorded_via` marker such as `bootstrap-reconciliation`?
2. Should this owner add a focused regression test for canonical repo posture, or is real-environment `doctor/live-status` evidence sufficient?
3. Does this lane need to touch any user-facing consent prose, or only the tracked truth artifacts?

## Current Judgement

This is worth materializing as a narrow follow-on because:

- it is a real residual drift on canonical `develop`
- it no longer belongs to any completed owner
- it has a small, verifiable write surface
