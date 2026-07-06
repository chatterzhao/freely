# Candidates - 20260402-0455--worktree-exclusive-ownership-governance

## C-20260402T045500Z-A: legacy issue

- candidate_format_version: `v2`
- title: Worktree exclusive ownership and promotion lease governance
- problem: Freely 已有多 worktree supervision、PID ownership、session evidence 与 develop merge issue binding，但仍缺少对同一 worktree / cleanup lane / promotion lane 的排它 ownership truth。问题不在于“一个 worktree 只能有一个 AI”，而在于缺少对 mutate intent 的独占治理，导致多个 AI 可能同时写同一 worktree、同时处理同一 dirty tree、或同时把同一 worktree promote 到 `develop`。
- why_now:
  - 最近 Freely 自举已真实暴露同一 worktree 的多 AI 踩踏，而不是抽象风险
  - 现有 `parallel_safe` / `write_scope` / same-lane busy guard 只覆盖调度语义，没有 runtime 级 lease
  - 仅靠 PID / session liveness check 无法稳定区分 observer、active owner、stale owner、recovery owner 与 takeover owner
- acceptance_criteria:
  - 明确这是 auto-loop / manager arbitration 问题，而不是任意 worker 自判问题
  - 明确区分 occupancy plane 与 intent lease plane
  - 给出 occupancy record 与 intent lease record 的最小字段表
  - 明确区分 `edit lease`、`cleanup lease`、`promotion lease`
  - 明确允许多 AI 并发 read / review，但限制 mutate intent 独占
  - 明确 worker locality：worker 默认不得因观测到别的 worktree dirty 而跨树 cleanup / merge
  - 定义 probe-first 与 lease-first 的职责边界，避免把 PID / jsonl 误当 ownership truth
  - 给出最小 machine-readable lease surface，能够被 runtime / live-status / fleet-status / manager continuity 消费
  - 定义 stale owner、handoff、takeover、release 的最小规则，以及 soft-stale / hard-stale 判断
  - 明确第一阶段是否 advisory-only，还是直接进入 blocking gate
- promotion_gate:
  - 证明现有 multi-worktree supervision 与 develop merge gate 无法单独覆盖此问题
  - 证明“全仓 cleanliness 检查”需要 ownership-aware routing，不能让 merge actor 因看到别树 dirty 就直接越权处理
  - 证明这条能力必须服从既有 `manager arbitration / worker locality / runtime machine-readable truth` 约束，而不是新造平行治理
  - 保持范围聚焦于 ownership / lease governance，不顺手重写整个 runtime
  - 至少给出一组可测试的并发冲突场景：同树双写、dirty cleanup 争抢、重复 promotion、worker 观测到 sibling dirty 后试图越权介入
- open_questions:
  - resolved in `I-20260402T045500Z-A`: phase-1 canonical truth 先由 project/runtime surface 持有，再由 status 聚合展示
  - resolved in `I-20260402T045500Z-A`: `promotion lease` target 固定为 `issue_id + integration_target`
  - resolved in `I-20260402T045500Z-A`: cleanup followthrough 第一阶段即消费 ownership-aware retain gate
  - resolved in `I-20260402T045500Z-A`: `soft-stale` 必须 manager review，`hard-stale` 才允许 runtime reclaim
  - resolved in `I-20260402T045500Z-A`: phase-1 blocking 仅覆盖 `same-worktree edit / cleanup / promotion`
- acceptance_reviews:
  - reviewer: `codex-explorer-russell`
    verdict: `supports`
    note: 现有治理已经把 merge / cleanup / fleet closure 定义为 manager-owned；缺口主要是 ownership truth 尚未机器化
  - reviewer: `codex-explorer-einstein`
    verdict: `supports`
    note: 现有 `dispatch_priority / parallel_safe / write_scope` 只覆盖 launch-time scheduling，不能替代长期 intent ownership
- decision_reason:
  - 当前缺口已是 Freely 狗粮链路中的真实治理问题，继续依赖人工判断会放大为数据竞争
  - `worktree -> pid` 绑定只适合作为 occupancy 探测层，但不足以承担最终 gate
  - lease model 能与现有 queue / frozen queue / continuity / merge gate 自然衔接
- priority: `P0`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260402T045500Z-A`
- promoted_issue_path: `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/raw-20260402-0455issues/worktree-exclusive-ownership-and-promotion-lease-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - this candidate materialized as `I-20260402T045500Z-A` and is now closed on canonical `develop` via merge `a10f6d8`
  - reopen only if a follow-on owner must extend ownership semantics beyond phase-1 `edit / cleanup / promotion`
  - keep any reopen narrow: ownership-aware routing and machine-readable truth, not generic runtime orchestration redesign
- revisit_trigger:
  - another same-worktree multi-AI collision
  - ambiguous cleanup ownership on a dirty worktree
  - repeated merge / promote collision on the same feature worktree
