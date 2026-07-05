# Progress: backend-service-contract-and-adapter-taxonomy

- issue_id: `I-20260312-0011`
- title: `Backend Service Contract and Adapter Taxonomy`
- phase_state: `completed`
- milestone: `M-20260312-control-surface-runtime-convergence`
- updated_at: `2026-03-26`
- summary:
  - `backend-service-contract-and-adapter-taxonomy` 已从 IBM 冻结推进到 canonical completion：`ClientCommand` / `ServerEvent` / `Snapshot` 语义层、adapter taxonomy，以及 OpenClaw 仅为 optional adapter/profile 的边界都已稳定写成单一真源。
  - downstream frontend-probe 架构与 boundary contract issue 已直接复用同一对象族和 adapter 兼容原则，因此后续工作应 materialize 新 issue，而不是让本 issue 长期停留在 `done_ibm`。
- evidence:
  - `docs/epics/control-surface-runtime-convergence/backend-service-contract-and-adapter-taxonomy/code-reviews/20260320-backend-service-contract-and-adapter-taxonomy-ibm-completion.md`
  - `docs/epics/control-surface-runtime-convergence/backend-service-contract-and-adapter-taxonomy/code-reviews/20260326-backend-service-contract-and-adapter-taxonomy-canonical-verification.md`
  - `docs/epics/frontend-probe-dogfooding-loop/internal-frontend-backend-architecture-review/issues/internal-frontend-backend-architecture-review.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/issues/frontend-backend-boundary-contract-v1-for-frontend-probe.md`
- next:
  - 后续 control surface、standalone runtime、human intervention transport 继续复用该 contract 真源；若要引入新的系统拓扑总图或 adapter family，另开 lifecycle
