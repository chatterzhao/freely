# Verification: codex-acp-fresh-path-prototype

- issue_id: `I-20260401-1545-A-01`
- reviewer: `codex`
- verdict: `pass_for_verification`

## Commands

- `bash -n docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `bash -n docs/system/workspace/scripts/monitor-ai-cli.sh`
- `python3 -m py_compile docs/system/workspace/scripts/runtime/run-acp-prompt.py`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-acp-fresh`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-adapter-dispatch`
- `bash docs/system/workspace/scripts/tests/test-freely-tool-adapter-policy-resolution`
- `bash docs/system/workspace/scripts/tests/test-freely-baseline-status`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-pid`
- `bash docs/system/workspace/scripts/tests/test-freely-init-ai-default-precedence`
- `bash docs/system/workspace/scripts/tests/test-freely-set-tool-command`
- `./bin/governance-check`
- `FREELY_CODEX_ACP_BIN="$HOME/.cache/freely/acp/codex-acp/0.11.1/aarch64-apple-darwin/codex-acp" bash docs/system/workspace/scripts/monitor-ai-cli.sh --project /tmp/freely-real-codex-acp.k6v8y7/project --tool codex --tool-adapter acp --model gpt-5.4 --reasoning-effort medium --mode auto --prompt-file /tmp/freely-real-codex-acp.k6v8y7/prompt.txt --pid-file /tmp/freely-real-codex-acp.k6v8y7/ai.pid --log-file /tmp/freely-real-codex-acp.k6v8y7/ai.log --launch-kind fresh`

## Results

1. `codex + adapter=acp` now has a real launcher path, not just metadata or placeholder routing.
2. Fake ACP end-to-end coverage remains green, proving Freely's one-shot ACP client, permission auto-approval, and launch dispatch contract are wired correctly.
3. Focused fake-agent coverage now explicitly proves both `fresh` and `fresh_with_handoff` for `codex + adapter=acp`, closing the remaining scope gap between the issue contract and the verification surface.
4. Real-environment viability evidence is now present: pinned `codex-acp` binary acquisition succeeded and the fresh-path sample produced ACP session `019d4c11-0bc0-7492-a63f-e9bbc1962d5b`.
5. The real sample returned `ACP_OK`, confirming the binary, auth state, session creation, and minimal prompt/response path all work together on a live Codex ACP turn.
6. The ACP path still warns that `reasoning_effort='medium'` is not yet mapped and that requested model `gpt-5.4` was not advertised by the agent; this is documented behavior, not a silent degradation.
7. `resume` remains explicitly outside ACP parity for this owner, so direct path still owns the strongest explicit resume contract.
8. Direct-path focused regressions still pass, including Codex fresh/resume argument handling, pid tracking, and the managed tool/adapter configuration surfaces.

## Implementation Decision Note

- decision: legacy: completed verification artifact
- why_this: legacy: no detailed record
- alternatives_considered: legacy: no detailed record
- boundary_non_goals: legacy: no detailed record
- residual_risk: legacy: no detailed record
