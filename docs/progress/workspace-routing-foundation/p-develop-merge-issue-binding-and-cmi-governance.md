# Progress: develop-merge-issue-binding-and-cmi-governance

- issue_id: `I-20260321-1835-A`
- issue_path: `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/issues/develop-merge-issue-binding-and-cmi-governance.md`
- phase_state: `in_dev`
- summary: `C-20260321-1835-A` 已 materialize 为独立 owner issue。本轮确认 gate 仍缺 capability-change execution contract，于是在已有“必须绑定具体 issue，且 touched candidate 与 touched owner issue 必须同线”的基础上，补齐 execution-phase owner、same-line progress/review 以及 bare-issue rejection 规则。
- current_focus:
  - lock capability-change rejection for `in_ibm` / `done_ibm` / `completed` owners
  - lock capability-change rejection for bare issue without same-line progress/review
  - verify pre-merge hook wrappers still hit the strengthened gate
- next_action: `commit and merge the strengthened gate, then replay the stale lifecycle closeout fixes behind it`
- revisit_trigger: 若 gate 对 capability-change owner phase、same-line progress/review、borrowed owner、或 cross-line owner 任一场景出现误放/误拦，则继续扩 matrix 直到 allow/deny 边界稳定
