# Candidates

- id: C-20260322-0115-A
- title: Unify Freely as the only front-door control surface
- status: promoted
- adoption_type: n/a
- source_brainstorm: `docs/B1-docs/20260322-0115--cli-first-entrypoint-and-observability-surface-unification/brainstorms.md`
- why_now: 当前 `chat` 与 `tui` 的 high-level 语义已经接近，但 post-submit runtime chain 仍不完全统一，阻碍 `freely` 成为唯一正式前台入口，也阻碍后续把 CLI 面当作 TUI/GUI 的 canonical backend。
- proposed_scope:
  - freeze CLI-first control surface contract
  - make `tui` submit path reuse the same high-level post-submit chain as `chat`
  - define CLI status family as canonical observability backend for future TUI/GUI
- acceptance_hint:
  - `freely chat` 与 `freely tui` 在提交后都走同一 high-level runtime chain
  - canonical observability backend is CLI-first, not external tool TUI
  - truth sources clearly state TUI/GUI are render layers over the same backend contract
- promoted_issue_path: `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/issues/cli-first-entrypoint-and-observability-surface-unification.md`
- legacy_id_mapping: I-20260322-0115  # 历史遗留的 issue id
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs: []
