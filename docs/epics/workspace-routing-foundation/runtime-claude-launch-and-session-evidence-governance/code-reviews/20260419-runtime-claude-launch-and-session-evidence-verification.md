# Verification: runtime-claude-launch-and-session-evidence-governance

- issue_id: `I-20260419-2245-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-claude-launch-and-session-evidence-governance/issues/runtime-claude-launch-and-session-evidence-governance.md`
- verification_date: `2026-04-19`
- verifier: `codex`

## Scope Verdict

- `PASS`: manual replay proved the broken switch path was Freely's Claude-family non-interactive launch syntax, not a general fallback-policy failure.
- `PASS`: Claude-family `-p/--print` launches with `--add-dir` now succeed when prompt content is sent over stdin.
- `PASS`: resume-target selection now requires verified Claude session evidence, so stale generated ids are rotated or cleared instead of becoming false resumable truth.
- `PASS`: the repair stays bounded to launcher/session-evidence semantics and does not broaden Freely's ownership to unrelated manually started tool processes.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-tool-launchers-cc-stdin-add-dir`
2. `bash docs/system/workspace/scripts/tests/test-freely-claude-resume-target-requires-evidence`
3. `bash -n docs/system/workspace/scripts/runtime/tool-launchers.sh`
4. `bash -n docs/system/workspace/scripts/runtime/freely`
5. `printf 'say hi\n' | claude -p --permission-mode bypassPermissions --add-dir /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees`
6. runtime-equivalent fresh launcher replay via `tool_run_from_prompt_file ... fresh ...`
7. runtime-equivalent resume launcher replay via `tool_run_from_prompt_file ... resume ...`
8. `git diff --check`
9. `./bin/governance-check`

## Implementation Decision Note

- decision: `Promote the Claude-family launch-contract and session-evidence repair as one bounded runtime owner.`
- why_this: `The failing real command, focused code diff, and regression coverage all point to the same seam: print-mode stdin contract plus verified resume evidence.`
- alternatives_considered: `Treat the breakage as only an iflow outage; force the runtime onto codex-only behavior; widen the lane into generic self-heal/liveness redesign.`
- boundary_non_goals: `This owner does not claim to solve the later worker/supervisor truth issue and does not reopen account-switch policy.`
- residual_risk: `Future CLI contract drift could require another narrow follow-on, but current bounded evidence covers the real failing path seen on 2026-04-19.`
