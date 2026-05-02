# Candidates - 20260402-0403--canonical-product-posture-bootstrap-reconciliation

## C-20260402-0403-A

- title: Canonical product posture bootstrap reconciliation
- problem: canonical `develop` still fails Freely's own execution-boundary audit because tracked and bootstrap-managed repo posture truth lag the already-completed product and tool-materialization owners; `.codex/config.toml` still uses guarded approval posture and canonical local bootstrap state still lacks recorded activation-consent truth.
- why_now:
  - completed owners already froze the contract, so continued drift on `develop` is now misleading dogfood debt rather than open design space
  - `live-status` and `doctor` currently prove the mismatch on the canonical repo itself
  - the remaining work is narrow and directly verifiable
- acceptance_criteria:
  - canonical tracked posture plus managed local bootstrap truth match the already-frozen autonomy and activation-consent contract
  - canonical `freely live-status --project <repo>` no longer reports legacy activation-consent drift
  - canonical `freely doctor --project <repo>` passes without reopening unrelated owners
  - the owner stays narrowly scoped to canonical posture reconciliation, not generic init/bootstrap redesign
- promotion_gate:
  - prove the residual is not already owned by a still-active issue
  - keep the follow-on under product/tool posture reconciliation rather than workspace-routing
  - identify a bounded verification set on the canonical repo itself
- decision_reason:
  - completed owners should not remain "completed in theory, failing in practice" on canonical `develop`
  - this residual is too small to reopen the old umbrella and too concrete to leave as informal followthrough
- priority: `P1`
- status: `promoted`
- milestone: `M-20260326-freely-product-architecture`
- promoted_issue_path: `docs/epics/freely-product-architecture/canonical-product-posture-bootstrap-reconciliation-governance/issues/canonical-product-posture-bootstrap-reconciliation-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - materialize a narrow follow-on owner for canonical repo posture reconciliation
  - reconcile `.codex/config.toml` and canonical bootstrap proof for activation consent
  - verify with canonical `live-status`, `doctor`, and governance checks
