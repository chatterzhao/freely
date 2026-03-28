# Progress: develop-merge-issue-binding-and-cmi-governance

- issue_id: `I-20260321-1835-A`
- issue_path: `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/issues/develop-merge-issue-binding-and-cmi-governance.md`
- phase_state: `in_dev`
- summary: `C-20260321-1835-A` 已 materialize 为独立 owner issue。本轮在已有“必须绑定具体 issue，且 touched candidate 与 touched owner issue 必须同线”的 contract 上，补齐 direct issue / promoted / absorbed canonical owner 的正向放行矩阵，以及 cross-line progress owner 的反向阻断矩阵。
- current_focus:
  - lock same-line direct issue positive coverage
  - lock promoted and absorbed canonical owner positive coverage
  - lock cross-line progress-owner rejection coverage
- next_action: `run the full merge-gate matrix and stage the owner issue continuation`
- revisit_trigger: 若 gate 对 direct issue、promoted owner、absorbed canonical owner、或 cross-line progress owner 任一场景出现误放/误拦，则继续扩 matrix 直到 allow/deny 边界稳定
