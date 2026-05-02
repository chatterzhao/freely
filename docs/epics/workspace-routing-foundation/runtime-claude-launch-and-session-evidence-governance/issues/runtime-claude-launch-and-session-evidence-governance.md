# Issue: runtime-claude-launch-and-session-evidence-governance

- issue_id: `I-20260419-2245-A`
- title: `Runtime Claude launch and session evidence governance`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-claude-launch-and-session-evidence-governance`
- issue-name: `runtime-claude-launch-and-session-evidence-governance`
- priority: `P0`
- source_candidate: `docs/pre-brainstorms/20260419-2245--runtime-claude-launch-and-session-evidence/candidates.md#c-20260419-2245-a`
- source_brainstorm: `docs/pre-brainstorms/20260419-2245--runtime-claude-launch-and-session-evidence/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/runtime-claude-launch-and-session-evidence-governance/pre-tests.md`
- tasks_path: `docs/epics/workspace-routing-foundation/runtime-claude-launch-and-session-evidence-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-claude-launch-and-session-evidence-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/runtime-claude-launch-and-session-evidence-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
- created_at: `2026-04-19`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Manual replay narrowed the tool-switch failure to two concrete seams:

1. Freely launched Claude-family `-p/--print` calls by passing prompt text on argv together with `--add-dir`, but current Claude CLI behavior required the prompt to be delivered via stdin in this path.
2. Freely could record a freshly generated Claude session id and later reuse it as a resume target without any verified Claude session evidence on disk.
3. That combination made a fallback tool look broken or hung even when `claude -p` itself was healthy and short-lived exec semantics were working as designed.

## Scope

1. Fix Claude-family non-interactive print-mode launchers to provide prompts in the contract the CLI now accepts.
2. Only reuse Claude session ids as resume targets when project-local session evidence exists.
3. Rotate or clear stale Claude anchors when a fresh run produced no verified evidence.
4. Keep the repair compatible with other short-lived non-interactive tools instead of turning child exit into a special-case failure.

## Non-Goals

1. Do not redesign generic heal timing, pid reconciliation, or broader supervisor lifecycle policy.
2. Do not hard-code the runtime to `codex`-only execution.
3. Do not widen this owner into all tool-availability or account-switch policy.
4. Do not claim this owner fixes the separate worker/supervisor self-heal truth issue observed later in daemon replay.

## Acceptance

1. The runtime-equivalent Claude-family fresh launch path succeeds with `--add-dir` by feeding prompt content through stdin.
2. A Claude-family `resume` launch with no verified session evidence falls back to a fresh session anchor instead of silently doing nothing or reusing stale ids.
3. When a fresh Claude-family cycle leaves no verified project evidence, `CLAUDE_SESSION_ID_CURRENT` is cleared before future resume-target persistence.
4. Focused regressions and one manual real-CLI replay prove the repair without tying the runtime to one specific tool.

## Verification

- `bash docs/system/workspace/scripts/tests/test-tool-launchers-cc-stdin-add-dir`
- `bash docs/system/workspace/scripts/tests/test-freely-claude-resume-target-requires-evidence`
- `bash -n docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `bash -n docs/system/workspace/scripts/runtime/freely`
- `printf 'say hi\n' | claude -p --permission-mode bypassPermissions --add-dir /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees`
- runtime-equivalent fresh launcher replay via `tool_run_from_prompt_file ... fresh ...`
- runtime-equivalent resume launcher replay via `tool_run_from_prompt_file ... resume ...`
- `git diff --check`
- `./bin/governance-check`

## Success Criteria

1. Freely no longer misdiagnoses the Claude-family fallback as unavailable when the real failure was the non-interactive launch contract.
2. Only Freely-owned runtime processes and session evidence are eligible for lifecycle/reuse decisions; unrelated manual or foreign-project tool processes remain outside management.
3. Short-lived exec-style tools remain compatible with runtime state handling because missing Claude evidence now invalidates stale resume anchors instead of pretending the tool stayed alive.
4. The owner carries lawful candidate/issue/progress/review evidence through guarded merge into `develop`, then the feature and premerge worktrees retire.
