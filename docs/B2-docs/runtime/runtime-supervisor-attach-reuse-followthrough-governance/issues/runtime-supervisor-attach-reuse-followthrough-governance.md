# Issue: runtime-supervisor-attach-reuse-followthrough-governance

- issue_id: `I-20260419-1505-A`
- title: `Runtime supervisor attach reuse followthrough governance`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-supervisor-attach-reuse-followthrough-governance`
- issue-name: `runtime-supervisor-attach-reuse-followthrough-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260419/candidates.md#c-20260419-1505-a`
- source_brainstorm: `docs/B1-docs/raw-20260419/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/runtime/runtime-supervisor-attach-reuse-followthrough-governance/pre-tests.md`
- tasks_path: `docs/B2-docs/runtime/runtime-supervisor-attach-reuse-followthrough-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-supervisor-attach-reuse-followthrough-governance.md`
- verification_artifact_dir: `docs/B2-docs/runtime/runtime-supervisor-attach-reuse-followthrough-governance/code-reviews`
- created_at: `2026-04-19`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

The checkpoint branch `feature/checkpoint-lifecycle-trace-debuggability-20260419` preserves bounded runtime behavior that `develop` does not yet own:

1. Repeated `freely daemon start` should reuse a healthy same-project supervisor instead of launching another detached daemon-run process.
2. Foreground `freely start` should attach to the same live supervisor between AI cycles, including the narrower fallback where `ps` is unavailable but project ownership is still provable by cwd evidence.
3. Claude launcher execution should isolate `HOME` under the project runtime tree so project-local runtime state does not leak into the host user home.

These changes share one operational seam: reusing a live project runtime safely instead of spawning replacement chains or leaking launcher state. They are too concrete to remain undocumented checkpoint-only truth and narrow enough to avoid reopening broader runtime governance work.

## Scope

1. Reuse healthy same-project supervisors from `freely daemon start`.
2. Attach foreground `freely start` to a live supervisor between AI cycles when the runtime should still be considered active.
3. Preserve attach behavior when `ps` is unavailable but cwd ownership still proves the runtime belongs to the project.
4. Isolate Claude launcher `HOME` under the project runtime directory.
5. Carry the checkpoint through a lawful issue/progress/pre-tests/review chain.

## Non-Goals

1. Do not redesign generic runtime lifecycle policy outside this attach/reuse seam.
2. Do not reopen interruption-manager closeout routing work from later followthrough owners.
3. Do not mix this owner with memark protected-root bootstrap work.
4. Do not treat the checkpoint worktree as retired archive state before this bounded follow-on is merged or explicitly dropped.

## Acceptance

1. Repeated `freely daemon start` on a healthy project runtime reuses the live supervisor and does not launch an extra daemon-run process.
2. Foreground `freely start` attaches to a live supervisor between AI cycles instead of falling back to repair/relaunch.
3. The attach path still works when `ps` is unavailable but project ownership is provable.
4. Claude launcher execution isolates `HOME` under `.freely/tool-homes/claude`.
5. The owner carries explicit issue, pre-tests, tasks, progress, and verification truth in this worktree.

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
- `bash docs/system/workspace/scripts/tests/test-freely-start-attaches-live-supervisor-between-ai-cycles`
- `bash docs/system/workspace/scripts/tests/test-freely-start-attaches-when-ps-is-unavailable`
- `bash docs/system/workspace/scripts/tests/test-freely-cc-launch-isolates-home-under-project-runtime`
- `git diff --check`
- `./bin/governance-check`

## Closeout

1. Keep the current checkpoint worktree as the bounded implementation lane for this owner.
2. Record the focused regression evidence already preserved on this branch.
3. After governance truth is complete, decide whether this owner should move directly to guarded premerge replay or be absorbed by a newer runtime followthrough owner.
