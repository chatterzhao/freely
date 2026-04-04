# Code Review: global-ai-account-watchdog-and-manager-bootstrap
- issue_id: `I-20260318-1630`

- date: 2026-03-26
- reviewer: Codex
- scope: slot switch global launch gate and machine-readable state isolation
- verdict: pass

## What changed

1. `tool-launchers.sh` now treats the shared Codex slot switch lock as a launch barrier, so new manager/worker Codex processes wait for switch/probe completion before `exec codex`.
2. `availability-watchdog.sh` now sends switch-wait warnings to stderr, preventing `codex_current_slot()` / session-state command substitution from capturing warning text into machine-readable slot fields.
3. Focused regressions now directly cover:
   - switch-lock warning isolation from machine-readable stdout
   - monitor/launch path defer behind the shared switch lock
   - first post-switch Codex launch using stabilized auth instead of pre-switch auth
   - existing ensure-manager defer path under the new slot-sweep-first contract

## Verification

- `bash -n docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `bash -n docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-current-slot-does-not-capture-switch-warning`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-defers-during-account-switch`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-serialization`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-defers-during-account-switch`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
- `./bin/governance-check`

## Findings

1. This closes a real same-family race: prior serialization only covered watchdog/bootstrap reads and probe, but not the actual `codex exec` launch path.
2. This also closes a real observability bug: switch-wait warnings no longer pollute `LAST_ACTIVE_SLOT` / `last_active_slot` or similar machine-readable slot surfaces.
3. Completion remains pending commit / merge judgement / canonical replay; this batch is verified in the dedicated worktree, not completed.
