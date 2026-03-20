# Candidates - 20260320-0018--default-project-resolution-and-authorized-project-memory

## Context
- Source brainstorm: ./brainstorms.md
- Status: in_research

## Candidates

### C-20260320-0018-A
- title: Default project resolution and authorized project memory for CLI-first interruption entrypoints
- problem: `freely chat` / `freely tui` / `freely intake status` 等命令要求反复显式传 `--project`，使当前项目插话体验偏底层；同时若解析逻辑过宽，又会把任意目录误判为项目。
- why_now: human interruption 已经可用，下一步必须让常用 CLI 入口符合日常使用习惯，否则 TUI 与 chat 仍会被路径样板代码拖住。
- acceptance_hint:
  - 明确 `--project` 是 override，不是默认必传
  - 明确统一 resolver 的优先级
  - 明确全局记忆仅是已授权项目索引，不是第二套项目配置真源
  - 明确 `chat` / `tui` / `intake status` 等入口在当前仓库内可免参运行
  - 明确不会把任意外部 `$PWD` 误判为项目
- priority: P0
- status: needs_research
- decision_reason: 方向已清晰，但还需要通过脚本测试验证“当前目录解析”和“单授权项目回退”都能成立，才能安全推广到全部 CLI 入口。
- promoted_issue_path: pending://issue-materialization
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
