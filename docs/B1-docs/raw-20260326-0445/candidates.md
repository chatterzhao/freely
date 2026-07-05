# 候选：manager-delegated-intake-absorption-closure

- id: `C-20260326-0445-A`
- title: Close manager-delegated intake lifecycle after successful continuity publication
- source_brainstorm: `docs/B1-docs/raw-20260326-0445/brainstorms.md`
- status: `promoted`
- adoption_type: `new_issue`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260326-0445`
- promoted_issue_path: `docs/B2-docs/ibm/manager-delegated-intake-absorption-closure-governance/issues/manager-delegated-intake-absorption-closure-governance.md`
- legacy_id_mapping: I-20260326-0445  # 历史遗留的 issue id
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- decision_reason:
  - 当前缺口超出 `I-20260322-0049` 已冻结 scope；旧 issue 只定义 generated / consumed_into_prompt / pending_after_failure，不承接最终 lifecycle closure。
  - 真实 runtime 已出现大量历史 intake 长期停在 `delegated`，而 manager continuity 反复把它们当作已 absorbed signal，形成治理与 machine-readable truth 漂移。
  - 该 gap 边界稳定，足以 materialize 成新的 milestone-owned issue，而不是继续停留在口头解释或一次性 continuity judgement。
- why_now:
  - canonical `develop` 当前已积累大量 historical delegated continuation 元数据尾巴
  - manager 已开始需要专门做 backlog convergence / absorption sweep
  - 若没有 intake lifecycle closure，后续所有 interruption backlog 都会持续积灰
- expected_outcome:
  - successful manager continuity publication closes matching delegated intake lifecycle
  - failed / no-output rounds retain delegated for recovery
  - live runtime no longer keeps stale historical manager interruption backlog indefinitely delegated
- likely_truth_sources:
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/tests/test-freely-session-rotation`
  - `docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
  - `docs/B2-docs/ibm/manager-continuation-handoff-consumption-governance/issues/manager-continuation-handoff-consumption-governance.md`
- next_action:
  - materialize IBM files with strict pre-tests gate, then implement the manager-side absorption reconciler and focused regressions
