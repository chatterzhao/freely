# Candidates - 20260405-1805--test-pre-merge-family-promotion-gate-enforcement

### C-20260405-1805-A: legacy issue

- candidate_format_version: `v2`
- title: Test-pre-merge family promotion gate enforcement
- problem: `I-20260405-1615-A` 已冻结新的 promote model，但当前 governance truth sources 与 protected-branch gate 仍执行旧模型：文档仍允许 `feature/* -> develop`，而 `pr-merge-guarded` tests 仍阻止 `test-pre-merge-* -> develop`。如果不把 truth-source update 与 gate enforcement 放在同一 owner，同一时期就会同时存在两套合法路径定义。
- why_now:
  - 新 owner 已明确后续要拆出 gate enforcement follow-on，不宜继续把它停留在 handoff package
  - 用户已明确要求约束应由 hook / gate 强制，而不能只靠文档指导
  - 旧模型当前已经明确写在 `CONSTITUTION` / `LAWS` / `pre-test-merge-flow.md` / `pr-merge-guarded` / tests 中，属于真实可执行偏差，不是抽象风险
- acceptance_criteria:
  - 明确这条 owner 同时负责 truth-source update 与 promotion gate enforcement，不再拆成两个会漂移的 owner
  - 明确 `develop` 的正常合法来源改为 `test-pre-merge-*` family 与 `hotfix/*`
  - 明确 `feature/* -> develop` 作为正常路径被阻止
  - 明确 `test-pre-merge-*` family 覆盖 single-feature lane 与 explicit multi-bundle lane，不再新增第二前缀
  - 明确 `CONSTITUTION` / `LAWS` / `pre-test-merge-flow.md` / relevant skills 与 `pr-merge-guarded` / tests 同步更新
  - 明确本 owner 不承诺 lifecycle automation、manifest generation、paired create
- promotion_gate:
  - 证明这一条 owner 的边界是“更新真源并同步受保护分支 gate”，而不是再次重做 promote model 研究
  - 证明把 truth-source update 与 gate enforcement 放在同一 owner 内，比拆成两个 owner 更稳
  - 证明 lifecycle automation 仍保持为后续独立 owner，不在这里扩大
- open_questions:
  - `governance-check` / `governance-promotion-gate` 是否需要在本 owner 内同步增加 source-branch 合法性审计，还是先以 `pr-merge-guarded` 和 hooks 为主
  - explicit multi-bundle promote 在本 owner 内是否只需要 family-level source allowance，不需要完整 manifest validation
  - 哪些现有 tests 最适合作为 source-branch semantics 的主回归面
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports`
    note: promote model 已冻结；若 truth-source update 和 gate enforcement 不同时落地，短期内必然形成双真相。
- decision_reason:
  - 这不是“再开一个文档 owner”，而是把新模型真正接到可执行 gate 的最小下一跳
  - 先做 gate enforcement 比先做 lifecycle automation 更能立即封堵 `feature/* -> develop` 的治理逃逸
- priority: `P0`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- source_brainstorm: `docs/B1-docs/raw-20260405-1805/brainstorms.md`
- promoted_issue_id: `I-20260405-1805-A`
- promoted_issue_path: `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/issues/test-pre-merge-family-promotion-gate-enforcement-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - this candidate materialized as `I-20260405-1805-A`
  - keep the owner scoped to truth-source update plus protected-branch promotion gate enforcement
  - route lifecycle automation into a later owner after this enforcement owner closes
- revisit_trigger:
  - any attempt to update constitutional truth without synchronized gate changes
  - any attempt to change `pr-merge-guarded` source rules without synchronized constitutional writeback
  - renewed proposals for a second `test-pre-*` prefix
