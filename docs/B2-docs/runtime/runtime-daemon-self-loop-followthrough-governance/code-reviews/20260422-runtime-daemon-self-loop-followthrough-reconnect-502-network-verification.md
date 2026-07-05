# Verification: runtime-daemon-self-loop-followthrough-governance reconnect exhaustion 502 network marker

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-22`
- verifier: `codex`
- source_branch: `feature/codex-reconnect-exhaustion-network-marker-20260422`
- protected_test_branch: `test-pre-merge-20260422-codex-reconnect-exhaustion-network-marker`

## Scope Verdict

- `PASS`: canonical `develop` still failed the user success standard after proxy guidance landed, but the fresh replay narrowed the next blocker to exhausted Codex reconnect `502` exits being persisted as `tool_runtime_failure` instead of remaining on the bounded execution-network path.
- `PASS`: `docs/system/workspace/scripts/monitor-ai-cli.sh` now distinguishes network failure from generic tool failure and writes only the dedicated network marker when reconnect exhaustion plus upstream `502 Bad Gateway` evidence appears.
- `PASS`: `docs/system/workspace/scripts/runtime/freely` now passes a dedicated network marker file into monitor launch, consumes it before generic failure-marker fallback, and reuses runtime log classification to derive `execution_network_*` instead of widening into tool/slot fallback.
- `PASS`: `docs/system/workspace/scripts/tests/test-monitor-ai-cli-classifies-codex-reconnect-exhaustion-as-network-failure` locks the exhausted reconnect `502` regression without weakening the adjacent reconnect-defer or `429` paths.
- `PASS`: the owner remains `I-20260421-1200-A`; this is a bounded runtime/network-classification followthrough inside the same canonical daemon autonomy owner, not a broader tool policy or slot policy change.
- `PENDING`: canonical `develop` still needs post-merge daemon replay proving Freely starts, selects a task, completes it to the current-project success standard, merges upward, retires the temporary lane, and continues to another task.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-classifies-codex-reconnect-exhaustion-as-network-failure`
2. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-defers-codex-reconnect-until-retries-exhaust`
3. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-codex-on-429-rate-limit`
4. `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
5. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260422-feature-codex-reconnect-exhaustion-network-marker --issue docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
6. `./bin/governance-check`
7. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-classifies-codex-reconnect-exhaustion-as-network-failure`
8. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-defers-codex-reconnect-until-retries-exhaust`
9. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-codex-on-429-rate-limit`
10. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
11. `./bin/test-lane premerge-integration -- ./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260422-test-pre-merge-codex-reconnect-exhaustion-network-marker --issue docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
12. `./bin/test-lane premerge-integration -- ./bin/governance-check`

## Implementation Decision Note

- decision: `Keep exhausted Codex reconnect 502 exits on the existing execution-network path by introducing a dedicated network marker instead of collapsing them into generic tool runtime failure.`
- why_this: `Direct Codex execution already worked, and the failing replay showed the bug only appeared after monitor/runtime translated reconnect exhaustion into the wrong failure family. Preserving the bounded network classification fixes the real seam without widening into tool switching, slot policy, or generic retry redesign.`
- alternatives_considered: `Treat every exhausted reconnect as generic tool failure; re-enable automatic tool switching or slot switching to route around the symptom; redesign broader runtime recovery heuristics instead of preserving the existing execution-network path.`
- boundary_non_goals: `No default proxy-policy change, no auto tool switching, no slot switching, no fallback-policy redesign, and no claim that canonical self-host acceptance is complete before develop replay proves task completion, merge, retirement, and next-task continuation.`
- residual_risk: `If a relay emits different reconnect-exhaustion wording for the same upstream-network family, this narrow classifier may miss that new transcript and need another bounded same-owner followthrough.`
