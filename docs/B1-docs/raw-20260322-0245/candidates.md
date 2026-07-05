# Candidates - 20260322-0245--runtime-worker-launch-linkage-and-stall-recovery

## Candidate Issues

### C-20260322-0245-A: legacy issue
- title: `Runtime worker launch linkage and stall recovery governance`
- status: `promoted`
- adoption_type: `materialized`
- decision_reason: 真实 dogfood 已证明这不是主管语义缺失，而是 runtime 还没把 manager 产出的 stable worker handoff 转成实际 worker execution，同时也缺少对长时间无输出 AI 进程的 runtime-owned stall recovery。
- promoted_issue_path: `docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md`
- legacy_id_mapping: I-20260322-0245  # 历史遗留的 issue id
- milestone: `M-20260306-workspace-routing-foundation`
- source_brainstorm: `docs/B1-docs/raw-20260322-0245/brainstorms.md`
- session_refs: []
- next_action: materialize IBM 产物，然后在 runtime / watchdog 真源里实现最小 worker launch linkage 与 stalled AI recovery
- revisit_trigger: 若 runtime 改动后仍无法把 manager handoff 转成 worker execution，或 stall recovery 仍无法让新 intake 进入下一轮 prompt，再开下一条 lifecycle
