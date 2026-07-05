# Candidates - 20260321-1745--active-lifecycle-boundary-and-dogfooding-capability-discovery

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260321-1745-A
- title: Clarify active lifecycle boundary and dogfooding capability discovery
- problem: 当前对“历史 vs 当前可修改真源”的边界主要依赖人工口头判断，容易把未收口 issue/worktree 错当历史，或把已闭环 issue 错当当前承接面；同时，狗粮中暴露的问题还缺少一条明确原则，说明它们默认应先被判断为 Freely 的能力发现，而不是一次性项目经验。
- why_now: 这已经直接影响 Freely 开发 Freely 时如何开新生命周期、如何重构真源、以及如何把狗粮发现的问题真正产品化。如果不收敛，后续会继续在“回写历史”与“遗漏能力发现”之间反复摇摆。
- acceptance_hint:
  - 明确 `historical` 与 `active lifecycle` 的判断标准
  - 明确“历史 = 已完成且已收口”，不是“创建时间早”
  - 明确当前生命周期内允许应用产物收敛重构
  - 明确狗粮中暴露的可复现共性问题，默认先判断为 Freely 能力缺口
  - 落点优先放在三层 loop / 产品意图 / 管理路由真源，而不是只记在预研里
- priority: P0
- status: promoted
- decision_reason: 已进入正式 issue 生命周期；后续通过新的 issue 在三层 loop 与项目意图真源中收敛生命周期边界和狗粮能力发现原则，而不是继续停留在口头约定。
- next_action: 完成 IBM 产物与真源 wording 收敛后，进入 consistency verification，确认不会再把“历史/当前”边界读错，也不会把狗粮问题降格成一次性经验。
- revisit_trigger: 当新增 wording 落盘后，需要验证它与既有三层 loop / manager / worktree 治理仍一致时。
- promoted_issue_path: `docs/epics/workspace-routing-foundation/active-lifecycle-boundary-and-dogfooding-capability-discovery/issues/active-lifecycle-boundary-and-dogfooding-capability-discovery.md`
- legacy_id_mapping: I-20260321-1745  # 历史遗留的 issue id
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
