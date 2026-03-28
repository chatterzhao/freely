# Progress: develop-merge-issue-binding-and-cmi-governance

- issue_id: `I-20260321-1835-A`
- issue_path: `docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/issues/develop-merge-issue-binding-and-cmi-governance.md`
- phase_state: `in_dev`
- summary: `C-20260321-1835-A` 已从 pre-brainstorm supporting evidence materialize 为独立 owner issue。本轮正在把 develop merge gate 收紧到“必须绑定具体 issue，且 touched candidate 与 touched owner issue 必须同线”的 contract，并用 borrowed owner regression 固定住。
- current_focus:
  - materialize candidate into independent owner issue
  - tighten same-diff owner binding in `governance-merge-gate`
  - verify borrowed-owner and absorbed-owner failure paths
- next_action: `run focused governance regressions and stage the merge-ready owner line`
- revisit_trigger: 若 gate 仍允许 unrelated issue 充当 owner，继续扩 focused regressions 直到 diff-level owner binding 稳定
