# IBM Brainstorm: canonical-product-posture-bootstrap-reconciliation-governance

## Problem Slice

Completed product/tool owners already froze the right posture, but canonical tracked posture plus local bootstrap proof still lag them. The execution-boundary audit is therefore proving legacy drift on the canonical repo itself.

## Narrow Decision

Keep this lane purely as tracked posture plus local bootstrap reconciliation:

1. `.codex/config.toml` must match the completed `auto` materialization contract.
2. managed local config after `freely init --accept-default-autonomy` must carry activation-consent truth.
3. Real-environment `live-status` and `doctor` proof are the primary verification surface.

## Boundary Check

- Do not reopen contract wording.
- Do not widen into generic `init` redesign.
- Do not widen into workspace-routing or ACP.
