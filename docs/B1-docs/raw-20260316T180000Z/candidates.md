# Candidates - 20260316-1800--session-lifecycle-rotation-and-handoff

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260316T180000Z-A: legacy issue
- title: Session Rotation and Handoff Policy for Auto-Run AI CLIs
- problem: Freely 当前只有“首轮 fresh、后续一律 resume”的粗粒度策略，无法在 `context compacted` 或连续 resume 退化后切换到更健康的新会话，也没有明确 handoff 交接面。
- why_now: 这已经直接影响 Freely 用自己理念持续开发自己。若不先解决，会话会在后台无限续接旧上下文，导致首跳重复、恢复判断失真、产品狗粮质量下降。
- acceptance_hint: supervisor 记录 session state；检测 `context compacted` 与 resume 阈值；需要轮换时改走 `fresh`；生成 handoff 文件并注入下一轮 prompt；`codex` 默认模型固定为 `gpt-5.4`、默认 reasoning effort 固定为 `medium`；补齐脚本级回归测试。
- priority: P0
- status: promoted
- decision_reason: 这是当前后台运行不稳定和会话治理缺口的直接承接项，优先级高于 sidecar 演化层与更远期 UI。
- promoted_issue_path: `docs/B2-docs/ibm/session-lifecycle-rotation-and-handoff-governance/issues/session-lifecycle-rotation-and-handoff-governance.md`
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
- sequencing_rank: 1
