# Candidates

### C-20260318-A
- title: worktree 级 supervisor pid 归属校验
- status: promoted
- why:
  - 多工位监督要求 `status`/`fleet-status` 的 pid 展示可信。
  - stale pid 若被错误采信，会让自治控制面误判工位是否仍在运行。
- scope:
  - `runtime/freely`
  - `tests`
- acceptance:
- `freely baseline-status --project <wt>` 在 stale pid 指向其他 worktree 时输出 `supervisor_pid: none`
  - `freely fleet-status --project <wt>` 在同类场景下不显示错误 supervisor pid
  - `freely stop --project <wt>` 只停止真实属于该 worktree 的 supervisor
- promoted_issue_path: `docs/epics/workspace-routing-foundation/checkpoint-commit-and-multi-worktree-supervision-governance/issues/checkpoint-commit-and-multi-worktree-supervision-governance.md`
- legacy_id_mapping: I-20260318-0930  # 历史遗留的 issue id
- session_refs: []
- milestone: M-20260306-workspace-routing-foundation
