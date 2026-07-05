# Code Review - first-hop-second-hop-verification

- issue_id: `I-20260307-1201`
- date: `2026-03-16`
- reviewer_tool: `codex`
- reviewer_session_id: `current-thread`

## Scope

- `docs/system/workspace/agents/lead-agent.md`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/monitor-ai-cli.sh`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- `docs/system/workspace/scripts/tests/test-monitor-ai-cli-pid`
- `docs/system/workspace/scripts/tests/test-freely-supervisor-loop`
- `tests/test_doc_gate.sh`

## Findings

- no blocking findings

## Verified Behavior

- 首跳 prompt 显式要求：默认不要只输出 `next_prompt`，且同工具场景必须继续执行第二跳。
- `lead-agent` 与 `workspace/tools.md` 对“同工具继续第二跳”口径一致。
- `monitor-ai-cli.sh` 与 `runtime/freely` 已对齐 `reasoning_effort`、`fresh_with_handoff` 与 route-only handoff 识别所需的参数面。
- 回归测试已覆盖首跳路由 prompt、monitor pid 留痕与 doc gate 基线。

## Tests

- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-pid`
- `bash tests/test_doc_gate.sh`

## Residual Risks

- 尚未形成 promote / cleanup 证据，因此本 issue 仍停留在 `in_verification`。
- 当前研究阶段没有正式 `docs/progress/**`，执行证据仍临时落在 `docs/pre-brainstorms/CONVERGENCE.md`。
