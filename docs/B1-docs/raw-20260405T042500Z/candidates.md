# Candidates - 20260405-0425--develop-guarded-merge-entrypoint-enforcement

## C-20260405T042500Z-A: legacy issue

- candidate_format_version: `v2`
- title: Develop guarded merge entrypoint enforcement
- problem: 当前 `develop` 上的 `pre-merge-commit` 只检查 merge 内容是否满足 governance / promotion gate，却没有要求 merge 必须经由 `freely pr-merge-guarded` 发起，因此手工裸 `git merge` 仍能在 `develop` 上落地并再次制造 protected-branch merge misuse。
- why_now:
  - 这不是理论风险，本轮刚刚又因为手工 `git merge` 在 `develop` 上制造了新的治理偏差
  - 现有 `pr-merge-guarded` 已是 canonical 入口，但 hook 没有强制它，导致两套 merge 入口并存且容易误用
  - 已完成的 protected-merge owners 都明确要求后续 residual misuse 走新的窄 follow-on，而不是改写旧 closeout
- acceptance_criteria:
  - `develop` 上的 merge commit 若缺少 `pr-merge-guarded` canonical state 和 completion marker，`pre-merge-commit` 必须失败并指向 `freely pr-merge-guarded`
  - 一旦 canonical guarded handshake 存在，现有 governance materialization gate 仍会继续执行，不得被 entrypoint enforcement 短路
  - duplicate promotion ownership gate 在 guarded handshake 存在时仍然生效
  - `freely pr-merge-guarded develop <feature>` 和 `freely pr-merge-guarded complete develop <feature>` 的正常路径继续通过
- promotion_gate:
  - 不 reopen `I-20260402T002000Z-A`
  - 不 reopen `I-20260402T191200Z-A`
  - 不把这条 owner 扩成“让本地 hook 绝对不可绕过”的 host/server enforcement 讨论
  - focused regressions 至少覆盖：raw merge blocked、guarded handshake still reaches governance gate、guarded handshake still reaches promotion gate
- open_questions:
  - 这轮是否只收 `develop`，还是后续另开 candidate 把同一入口 enforcement 扩到 `main` / `test-pre-merge-*`
  - hook 拒绝文案是否需要直接区分“裸 git merge 初始发起”和“裸 git merge --continue completion”
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports`
    note: 当前缺口是入口约束而不是 receipt/ledger 缺口，适合作为新的 develop-bound narrow owner。
- decision_reason:
  - 仓库已经拥有 `pr-merge-guarded` 真源，缺的是 `pre-merge-commit` 对该入口的显式依赖
  - 用 hook-level guarded handshake enforcement 可以直接拦住本轮真实误用，同时保留现有下游 gate 和 break-glass contract
- priority: `P1`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260405T042500Z-A`
- promoted_issue_path: `docs/B2-docs/ibm/develop-guarded-merge-entrypoint-enforcement-governance/issues/develop-guarded-merge-entrypoint-enforcement-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - materialize a narrow owner for develop-bound guarded merge entrypoint enforcement
  - wire the hook to reject raw merge entry before governance / promotion checks
- revisit_trigger:
  - another raw `git merge` on `develop` lands or reaches pre-merge-commit without guarded state
  - entrypoint enforcement accidentally suppresses governance materialization or promotion gate execution
