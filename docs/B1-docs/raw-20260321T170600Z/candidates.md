# Candidates - 20260321-1706--chat-triggered-worker-runtime-reactivation

### C-20260321T170600Z-A: legacy issue
- title: Worker runtime reactivation after chat-triggered delegated continuation
- status: promoted
- why_now: `freely chat` 在 worker 工位上会产生 delegated continuation，但在 `operator_stop` 后不会自动把 worker 主循环拉起，真实狗粮已出现“插话成功但无人推进”的假活性。
- acceptance_hint: truth sources 必须明确 chat-triggered worker reactivation gate；runtime 必须能在安全条件下重启 worker 主循环去消费 delegated intake；验证需覆盖 stopped worker + chat continuation 的真实重入路径。
- promoted_issue_path: `docs/B2-docs/human/chat-triggered-worker-runtime-reactivation-governance/issues/chat-triggered-worker-runtime-reactivation-governance.md`
- legacy_id_mapping: I-20260321T170600Z  # 历史遗留的 issue id
- milestone: `M-20260306-workspace-routing-foundation`
- adoption_type: pending://not-assessed
- session_refs:
  - tool: codex
    session_id: current-thread
    jsonl_path: unavailable://captured-in-active-issue-lifecycle
    role: research
