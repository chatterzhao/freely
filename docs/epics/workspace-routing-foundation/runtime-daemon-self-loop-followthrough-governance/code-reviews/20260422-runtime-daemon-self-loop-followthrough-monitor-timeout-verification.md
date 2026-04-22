# Code Review: runtime-daemon-self-loop-followthrough-governance monitor timeout verification

- date: `2026-04-22`
- issue: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- progress: `docs/progress/workspace-routing-foundation/p-runtime-daemon-self-loop-followthrough-governance.md`
- decision: `pass`
- scope: `Bounded followthrough for the false `tool_runtime_failure` triggered by the benign Codex model-refresh timeout line during canonical daemon replay.`

## What Changed

1. `docs/system/workspace/scripts/monitor-ai-cli.sh` now filters the known benign Codex startup line `failed to refresh available models: timeout waiting for child process to exit` before runtime-failure classification.
2. `docs/system/workspace/scripts/tests/test-monitor-ai-cli-ignores-codex-model-refresh-timeout` proves the monitor leaves that run alone and does not write a failure marker.
3. The same owner docs now record this seam as part of `I-20260421-1200-A` instead of opening a parallel lane.

## Verification

1. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-ignores-codex-model-refresh-timeout`
2. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-detects-fast-exit-codex-429`
3. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-defers-codex-reconnect-until-retries-exhaust`
4. `bash -n docs/system/workspace/scripts/monitor-ai-cli.sh`
5. `./bin/governance-check`

## Residual Risk

1. This filter is intentionally narrow and string-matched to the currently observed benign Codex line. If Codex changes that startup noise format again, runtime may need another bounded follow-on instead of broadening timeout classification heuristics.
