# Candidates - 20260316-1648--codex-reasoning-effort-runtime-alignment

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260316T164800Z-A: legacy issue
- title: Project-Scoped Codex Reasoning Effort Runtime Wiring
- problem: Freely 当前只能显式指定 `tool / model / mode`，无法把 Codex 的 reasoning effort 作为项目级运行时状态记录并传递给 `monitor-ai-cli.sh`，导致 `gpt-5.4 medium` 这类实际运行配置依赖用户全局 `~/.codex/config.toml`。
- why_now: 当前仓库已经开始在 dedicated worktree 中用 Freely 自举启动 Codex；如果 reasoning effort 仍是隐式全局状态，狗粮行为就不可复现，也无法通过 `freely baseline-status` 自检。
- acceptance_hint: 保持 `--ai` 三段式不变，新增可选 `--reasoning-effort`；将其写入 `.freely/config.env`、显示在 `freely baseline-status`、透传到 `start-lead-agent.sh`，并在 `tool=codex` 时转成 `codex exec -c model_reasoning_effort=\"<effort>\"`；补齐最小回归测试。
- priority: P0
- status: promoted
- decision_reason: 这是当前狗粮启动链路暴露出的最短路径缺口，改动面小且不会破坏宪法中的 AI spec。
- promoted_issue_path: `docs/B2-docs/ibm/session-lifecycle-rotation-and-handoff-governance/issues/session-lifecycle-rotation-and-handoff-governance.md`
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
- sequencing_rank: 1
