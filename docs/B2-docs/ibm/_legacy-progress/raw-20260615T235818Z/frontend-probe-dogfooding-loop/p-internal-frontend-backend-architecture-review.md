# Progress: internal-frontend-backend-architecture-review

- issue_id: `I-20260308-1245`
- title: `Freely 内部前后端架构复评与可插拔协议边界`
- phase_state: `completed`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- updated_at: `2026-03-26`
- summary:
  - `internal-frontend-backend-architecture-review` 已从总体 IBM 冻结推进到 canonical completion：frontend/backend 边界、状态归属矩阵、`ClientCommand` / `ServerEvent` / `Snapshot` 三层协议分层、输入仲裁与 MVP autonomy milestone 都已成为后续 issue 的可复用真源。
  - downstream `frontend-backend-boundary-contract-v1-for-frontend-probe` 与 control-surface contract issue 已直接复用这条边界，因此后续工作应继续 materialize Probe / bridge / runtime issue，而不是让本 issue 长期停在 `done_ibm`。
- evidence:
  - `docs/B2-docs/human/tui/raw-20260308-1244code-reviews/20260326-internal-frontend-backend-architecture-canonical-verification.md`
  - `docs/B2-docs/human/tui/raw-20260308-1244issues/frontend-backend-boundary-contract-v1-for-frontend-probe.md`
  - `docs/B2-docs/runtime/control-surface/issues/backend-service-contract-and-adapter-taxonomy.md`
- next:
  - 后续 frontend probe、runtime baseline、bridge 与 host integration 继续复用该边界；若要重写更高层产品拓扑或自治等级定义，另开 lifecycle
