# Progress: project-command-semantics-and-restore-work-governance

- issue_id: `I-20260327-2006-A`
- title: Project command semantics and explicit restore-work governance
- phase_state: `completed`
- runtime_state: `merged_to_develop`
- branch: `develop`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely`
- issue_path: `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/issues/project-command-semantics-and-restore-work-governance.md`
- session_refs:
  - {tool: codex, session_id: "019d3752-80a1-7773-808d-081375e06aa7", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/28/rollout-2026-03-28T19-00-47-019d3752-80a1-7773-808d-081375e06aa7.jsonl", role: "dev-loop-progress-refresh"}
  - {tool: codex, session_id: "019d377f-37b7-7cf2-8b76-d6a4a36a4a7f", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/28/rollout-2026-03-28T19-49-37-019d377f-37b7-7cf2-8b76-d6a4a36a4a7f.jsonl", role: "completion-verification-continuity-refresh"}
  - {tool: codex, session_id: "019d3d46-4e39-7020-afdc-cd2f6822ae30", jsonl_path: "unavailable://live-status-deep-ref-only", role: "fresh-session-first-hop-recheck"}

## Summary

- `2026-03-30 17:34 PDT` parent owner closeout is complete. The canonical absorption happened at `develop` merge `b93efd2`.
- Verification is anchored by `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/code-reviews/20260328-project-command-semantics-feature-verification.md`.
- The verification-lane follow-up also closed the earlier harness gap: `test-freely-project-command-semantics` now completes in about `13.76s`, and interrupted runs clean up without leaving watcher residue.

## Current Focus

- Keep the merged project command taxonomy stable.
- Leave downstream global restart and future contract expansion in separate owners.

## Verification

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `perl -e 'alarm shift @ARGV; exec @ARGV' 5 bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready`
- `./bin/governance-check`
- `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/code-reviews/20260328-project-command-semantics-feature-verification.md`

## Next Action

- 已完成 closeout。若未来 project command family 需要新 contract，必须新开 lifecycle，而不是继续写回本完成 owner。
