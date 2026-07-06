# Progress: frontend-backend-boundary-contract-v1-for-frontend-probe

- issue_id: `I-20260317-1001`
- title: `Frontend/Backend Boundary Contract v1 for Frontend Probe`
- phase_state: `completed`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- updated_at: `2026-03-26`
- summary:
  - `frontend-backend-boundary-contract-v1-for-frontend-probe` 已从 IBM 冻结推进到 canonical completion：Probe day-1 的 command / event / snapshot object family、error surface、request correlation、stream ordering 与 adapter compatibility 都已写成下游可直接消费的真源。
  - downstream `frontend-probe-v0` 与 `rust-tauri-probe-bridge-v1` 已直接复用该 v1 contract，因此后续工作继续沿 active `in_dev` 主线推进，而不是让本 issue 长期停在 `done_ibm`。
- evidence:
  - `docs/B2-docs/human/tui/code-reviews/20260326-frontend-backend-boundary-contract-v1-canonical-verification.md`
  - `docs/B2-docs/human/tui/issues/frontend-probe-v0.md`
  - `docs/B2-docs/human/tui/issues/rust-tauri-probe-bridge-v1.md`
- next:
  - 后续 Probe v0 与 Rust/Tauri bridge 继续复用该 contract；若要升级成 v2 schema 或新增 domain object，另开 lifecycle
