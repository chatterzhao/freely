# Candidates - 20260321-2010--explicit-session-addressed-resume-over-last-and-pty

## Context
- Source brainstorm: ./brainstorms.md
- Status: proposed

## Candidates

### C-20260321-2010-A: legacy issue
- title: Define explicit session-addressed resume as Freely's canonical continuity model
- problem: Freely 当前对不同工具的 continuity 寻址不一致。`cc` 已用显式 `session-id`，但 `codex` 仍用 `resume --last`，`iflow` / `kiro-cli` 也没有显式 workcell-scoped session contract。在多进程并行下，这会让 resume 命中错误会话，也会让 supervisor/runtime 混淆“最近会话”和“当前 workcell 应接的会话”。
- why_now: 本轮自举明确暴露了 manager event re-entry 错路由问题；同时本机研究已确认 `codex exec resume` 支持显式 `SESSION_ID` 与 stdin prompt，因此已经有足够清晰的正式 primitive 可被 Freely 收编。
- acceptance_hint:
  - Freely truth sources 明确：canonical continuity model = explicit session-addressed resume
  - `codex` 不能再以 `resume --last` 作为默认并发路径
  - `PTY input injection` 只能作为 fallback，不是默认 supervisor/runtime 模型
  - 需要审视 `iflow` / `kiro-cli` 当前 continuation contract 是否足以支持多进程并行
  - `session evidence` 至少应表达 `tool + session_id + jsonl/rollout path + cwd`
- priority: P1
- status: promoted
- decision_reason: 现有实现差异已经足够清晰，且 `codex` 正式 CLI 已提供显式续会话能力。继续停留在模糊研究会延后 runtime 真问题的修复。
- promoted_issue_path: `docs/B2-docs/ibm/explicit-session-addressed-resume-governance/issues/explicit-session-addressed-resume-governance.md`
- legacy_id_mapping: I-20260321-2010  # 历史遗留的 issue id
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
    session_id: current-thread
    jsonl_path: unavailable://to-be-recorded-in-issue-lifecycle
    role: research
