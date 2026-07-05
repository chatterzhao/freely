# Candidates - 20260328-0335--operator-stop-runtime-stall-recovery-semantics

## Context
- Source brainstorm: `./brainstorms.md`
- Status: materialized

## Candidates

### C-20260328-0335-A
- title: Clarify whether repeated `operator_stop` during manager recovery is intended runtime semantics or a new stall-detector false positive
- problem: 修复 `same-lane busy` 误判后，`develop` manager 不再立即卡在 delegated continuation backlog，但仍会每隔约 3-4 分钟被 `runtime-stalled-ai-recovery -> local_continuation_reentry` TERM 一次，外显成 `operator_stop_requested`。更深层的现场还显示：manager watchdog 以 `cycle-*.log/prompt mtime > 90s` 作为主要 stall 判据，而 manager prompt 仍反复注入历史 delegated backlog，导致 manager 长时间没有新 continuity 写回。当前需要判断这到底是合法长静默 supervision 被误判，还是 delegated backlog 收口缺口与 stall detector 叠加形成的控制面 thrash。
- latest_evidence: `2026-03-28T10:47:11Z` 的新 manager cycle 在 `2026-03-28T10:50:32Z` 再次被 `operator_stop_requested` 杀掉，并于 `10:50:42Z` 自动拉起新 supervisor。对应 cycle log 在启动后只短暂更新，随后静默超过 `90s`。这把“90 秒静默后稳定复现 thrash”从推测提升成了直接现场证据。
- why_now: 这已经影响对产品语义的理解。用户会自然把 `operator_stop_requested` 读成显式 stop/restart 功能语义，但现场证据表明它目前更像 runtime-owned recovery path。若不先澄清，就会把控制面 bug、可观测性命名问题和 start/stop/restart 产品需求混为一谈。
- acceptance_hint:
  - 冻结 `operator_stop_requested` 在 runtime recovery 场景中的真实触发链
  - 判断当前周期性 stop 是否属于预期 watchdog recovery，还是新的 manager stall false positive
  - 判断 manager 长静默是否属于三个 loop 下的合法 supervision round，还是必须在 90s 内产出新 runtime-visible heartbeat
  - 判断 delegated intake/backlog 吸收缺口是否正在放大 manager prompt，并阻止新的 continuity 闭环
  - 明确这条问题应归属 runtime recovery / observability，还是应吸收到 start-restart control-plane semantics 产品线
  - 若需要 follow-on，拆清“stall detector contract”“delegated backlog absorption”“runtime event naming semantics”是否应分成独立 owner
- priority: P0
- status: promoted
- milestone: M-20260306-workspace-routing-foundation
- promoted_issue_path: `docs/B2-docs/ibm/manager-supervision-quiet-period-stall-signal-governance/issues/manager-supervision-quiet-period-stall-signal-governance.md`
- decision_reason: 现阶段证据已足以确认 primary owner 是 manager delegated-supervision quiet-period heartbeat contract，而不是旧 `same-lane busy` issue 的 verification 尾巴，也不是纯 observability 命名问题。该问题已经满足独立 issue materialization 条件。
- next_action: 按新 issue 进入 IBM/dev 流程，先补 negative/paired-positive tests，再选择 delegated-supervision idle-safe contract 或 signal-first / observe-delay 的最小修法，最后再处理 observability 区分。
- revisit_trigger: 后续仅在实现阶段发现 delegated backlog absorption 与 quiet-period signal contract 实际不可分时，才重新调整 owner 边界。
- implementation_judgement:
  - current_behavior_needed_by_design: no
  - likely_nature: runtime stall-detector bug or suboptimal heuristic
  - current_implementation_optimal: no
  - primary_contract_gap: manager delegated-supervision quiet-period is treated as strong stall evidence even when worker/runtime truth still looks healthy
  - lower_regression_precedent: reuse restart-storm style signal-first or observe-delay handling before direct recovery
  - lowest_regression_direction: narrow delegated-supervision idle-safe contract plus new negative tests, not a global threshold bump
- session_refs:
  - tool: codex
    session_id: current-thread
    jsonl_path: unavailable://codex-thread-only
    role: author
