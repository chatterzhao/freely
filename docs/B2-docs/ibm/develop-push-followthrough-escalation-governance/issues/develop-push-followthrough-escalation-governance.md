# Issue: develop-push-followthrough-escalation-governance

- issue_id: `I-20260408-1200-A`
- title: Develop push followthrough escalation governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `develop-push-followthrough-escalation-governance`
- issue-name: `develop-push-followthrough-escalation-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260408/candidates.md#c-20260408-1200-a`
- source_brainstorm: `docs/B1-docs/raw-20260408/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/develop-push-followthrough-escalation-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-develop-push-followthrough-escalation-governance.md`
- verification_artifact_dir: `docs/B2-docs/ibm/develop-push-followthrough-escalation-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/ibm/develop-push-pending-guard-governance/issues/develop-push-pending-guard-governance.md`
  - `docs/B2-docs/git-worktree/worktree-maintenance-governance/issues/worktree-maintenance-governance.md`
  - `docs/B2-docs/ibm/deep-refactor-fleet-sequencing-governance/issues/deep-refactor-fleet-sequencing-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经能显式暴露 `push_pending` / `push_deferred`，但还没有冻结更强的 followthrough 语义：

1. merge 成功后，什么时候 `develop` push 成为 manager 的第一优先级
2. 哪些 defer reason 合法，哪些只能短暂观察后立即回到 push
3. 哪些活跃 feature / research tree 必须先吸收最新 `develop` 再继续 owner judgment

当前 repo 的现场已经证明这个缺口是真问题：

- root `develop` 可长期 ahead of remote
- 活跃树会在 stale upstream 上继续做治理判断
- AI / runtime 中断会让 lawful merge 长时间停留在 local-only canonical truth

## Scope

1. 冻结 `push_pending` 的 urgency contract：
   - 默认能 push 就应尽快 push
   - 若未 push，必须进入显式 followthrough / defer truth
2. 冻结合法 defer reason 与 manager escalation 规则。
3. 冻结 active worktree 的 `resync_required` 触发条件。
4. 冻结 patrol / status surfaces 应如何提示：
   - `push_urgency`
   - `resync_required`
   - `defer_reason`
5. 保留“不 auto-push、不把网络副作用塞进 hook/runtime”的边界。

## Non-Goals

1. 不在本 owner 内实现 hook auto-push。
2. 不在本 owner 内把所有 worker launch 全部自动阻断。
3. 不在本 owner 内实现新的 git transport 或 remote retry engine。
4. 不在本 owner 内取代现有 push-debt state truth。

## Acceptance

1. Freely 真源明确：`develop` merge 成功后，若不存在合法 defer，及时 push 是默认 followthrough，而不是无限挂起的可选动作。
2. Freely 真源明确：`push_pending` 可以保留，但 manager 必须能判断其 urgency，而不是只“看见即可”。
3. Freely 真源明确：当活跃 worktree 的 owner judgment、verification、cleanup 或 absorption 依赖最新 `develop` truth 时，必须先 resync 再继续。
4. Freely 真源明确：允许短暂 defer，但 defer reason 必须是有限白名单，并带恢复点。
5. Freely 真源明确：第一阶段不做 auto-push；仍由 operator / manager followthrough 完成 remote canonical delivery。

## IBM Handoff

- implementation_scope_summary:
  - `I-20260408-1200-A` 先冻结治理 contract：timely push default、lawful defer、resync trigger、status/patrol surfacing。
  - 第一阶段优先修改 truth source / status semantics，不要求一次性实现所有 runtime enforcement。
  - 若实现阶段发现 push urgency 与 resync trigger 完全不同步，再拆为两个 dev-loop lane。
- required_doc_refs:
  - `docs/B2-docs/ibm/develop-push-followthrough-escalation-governance/issues/develop-push-followthrough-escalation-governance.md`
  - `docs/B2-docs/ibm/develop-push-followthrough-escalation-governance/brainstorms/b-develop-push-followthrough-escalation-governance.md`
  - `docs/B2-docs/ibm/develop-push-followthrough-escalation-governance/prd.md`
  - `docs/B2-docs/ibm/develop-push-followthrough-escalation-governance/pre-tests.md`
  - `docs/B2-docs/ibm/develop-push-followthrough-escalation-governance/tasks.md`
  - `docs/system/workspace/agents/manager-agent.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/quality/governance-check`

## Closeout

- Canonical `develop` already carries the bounded push-followthrough truth across `LAWS`, manager guidance, runtime status surfaces, and focused regressions.
- `2026-04-09` closeout verification reconfirmed that the owner is absorbed and only lifecycle writeback was missing.
- Future work should open a new owner if canonical `develop` later regresses push urgency, lawful defer visibility, or `resync_required` surfacing; do not reopen this bounded lane for auto-push or transport automation.
