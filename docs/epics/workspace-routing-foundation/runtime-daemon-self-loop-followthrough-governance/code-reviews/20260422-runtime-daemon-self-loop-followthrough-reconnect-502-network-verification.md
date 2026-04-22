# Verification: runtime-daemon-self-loop-followthrough-governance reconnect exhaustion 502 network marker

- date: `2026-04-22`
- issue: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- scope: `Keep exhausted Codex reconnect 502 exits on the bounded execution-network path instead of persisting tool_runtime_failure.`

## Why

- Canonical `develop` still failed the user success standard even after proxy guidance landed.
- Direct `codex exec` returned `hi`, but the same minimal call through `monitor-ai-cli.sh` reproduced `ERROR: Reconnecting... 1/5 ... 5/5` followed by `ERROR: unexpected status 502 Bad Gateway: Upstream request failed`.
- That path wrote `tool_runtime_failure`, so manager recovery widened into tool/slot fallback even though the failure family was still execution-network scoped.

## Changes Verified

1. `docs/system/workspace/scripts/monitor-ai-cli.sh` now distinguishes network failure from generic tool failure and only writes `network_failure` into the dedicated marker file.
2. `docs/system/workspace/scripts/runtime/freely` now passes a dedicated network marker file into monitor launch, consumes it before generic failure-marker fallback, and reuses runtime log classification to derive `execution_network_*`.
3. `docs/system/workspace/scripts/tests/test-monitor-ai-cli-classifies-codex-reconnect-exhaustion-as-network-failure` locks the exhausted reconnect `502` regression without weakening the adjacent reconnect-defer or 429 paths.

## Evidence

1. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-classifies-codex-reconnect-exhaustion-as-network-failure`
2. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-defers-codex-reconnect-until-retries-exhaust`
3. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-codex-on-429-rate-limit`
4. `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`

## Result

- `PASS`: exhausted Codex reconnect `502` evidence now stays on the bounded execution-network path.
- `PASS`: reconnect-in-progress logs still do not trigger early kill.
- `PASS`: Codex 429 remains immediate tool-failure evidence.
- `PENDING`: merge into `develop`, rerun `./bin/freely daemon start`, and verify canonical self-host supervision advances into real task work instead of widening into generic fallback after reconnect exhaustion.
