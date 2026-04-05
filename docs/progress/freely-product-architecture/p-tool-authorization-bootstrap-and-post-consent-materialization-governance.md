# Progress: tool-authorization-bootstrap-and-post-consent-materialization-governance

- issue_id: `I-20260405-1235-A`
- issue_path: `docs/epics/freely-product-architecture/tool-authorization-bootstrap-and-post-consent-materialization-governance/issues/tool-authorization-bootstrap-and-post-consent-materialization-governance.md`
- title: `Tool authorization bootstrap and post-consent materialization governance`
- phase_state: `done_ibm`
- runtime_state: `stopped`
- milestone: `M-20260326-freely-product-architecture`
- branch: `feature/tool-authorization-bootstrap-research-20260405-0335`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-0335-feature-tool-authorization-bootstrap-research`
- updated_at: `2026-04-05`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- The pre-brainstorm is now promoted into a dedicated `freely-product-architecture` owner rather than being squeezed into existing consent/tool-policy owners.
- The owner freezes four distinct layers: activation consent, project authorization bootstrap, tool trust/permission surface, and adapter surface.
- The current implementation review already shows why a new owner is required: `init` / `set-tool` / `sync-tooling` can mutate tooling surfaces, `cc + acp` still has config/runtime drift, and future CLI/TUI/GUI/settings must share one backend contract.
- The owner is now parked as the canonical IBM handoff for:
  - a per-tool matrix for `codex`, `cc`, `cc-use-codex-cli`, `iflow`, and `kiro-cli`
  - shared degradation semantics for missing/partial authorization bootstrap
  - runtime refactor seams for `cmd_init`, `cmd_set_tool`, and `cmd_sync_tooling`
- This lane remains documentation-first; future implementation must split into narrower follow-on owners instead of widening this architecture owner.

## Verification Snapshot

- Passed in this worktree:
  - `./bin/governance-check`

## Next Action

- Keep this owner parked as `done_ibm` architecture truth for post-consent authorization/bootstrap semantics.
- Route persisted state materialization, per-tool repair execution, and adapter/tool drift cleanup into narrower follow-on owners.
