# Candidates - 20260405-1914--test-lane-routing-and-enforcement

### C-20260405-1914-A: legacy issue

- candidate_format_version: `v2`
- title: Test lane routing and enforcement
- problem: 仓库已经出现 `./bin/test-lane`、lane-specific 规则写回和 focused regression，但它们没有正式 owner 链路，而且实现仍有真实缺口：`feature-local` 对 branch family 过宽、入口文件不可直接执行、部分技能与 checklist 仍保留旧 replay-only 语义。
- why_now:
  - 用户已明确要求“测试要按正确分支/worktree/lane 跑”，不能只靠文档提醒
  - promote model 已切到 `test-pre-merge-* -> develop`，测试 lane 规则再继续无主漂移，会反向制造新的双真相
  - 当前 `test-lane` 已有脚本与测试雏形，应该先纳入治理再继续扩大
- acceptance_criteria:
  - 明确三条 canonical lane 及其 branch/worktree 匹配关系
  - 明确 `feature-local` 只允许 dedicated `feature/*`、`feature/premerge-*`、`release/*`、`hotfix/*` families，而不是任意非 protected 分支
  - 明确 `premerge-integration` 只允许 `test-pre-merge-*`
  - 明确 `post-merge-followthrough` 只允许目标 protected branch canonical worktree
  - 明确 `./bin/test-lane` 与 `./bin/test-test-lane` 是正式入口，必须可直接执行
  - 明确相关 skills / checklist / hook README 必须与当前 promote model 和 lane model 对齐
  - 明确本 owner 不扩大到自动 lane 推断、batch create 或 lifecycle automation
- promotion_gate:
  - 证明这不是 1805 owner 的隐含剩余项，而是独立的 lane-routing/enforcement surface
  - 证明 machine-enforced lane contract 比“在文档里提醒先选 lane”更符合当前治理要求
  - 证明 focused regression 能覆盖 branch family mismatch、入口执行、lane misuse
- open_questions:
  - `feature-local` 是否应把 `feature/premerge-*` 与 `feature/*` 一并视为合法 writable lane family
  - 是否需要额外显式禁止 detached HEAD 和 ad hoc local branches
  - lane semantics 需要写回哪些最小 truth sources，才不会遗漏旧 replay 语义
- acceptance_reviews:
  - reviewer: `subagent-governance-review`
    verdict: `supports`
    note: 当前 `test-lane` 已有实现但无 owner；应 materialize 独立 owner，而不是继续挂在 promote-gate owner 下。
  - reviewer: `subagent-enforcement-review`
    verdict: `supports`
    note: `feature-local` 目前过宽，必须收紧到 dedicated branch families。
  - reviewer: `subagent-integration-review`
    verdict: `supports`
    note: 入口文件执行位与旧 replay 语义残留都是真实回归面，应纳入同一 owner 完成。
- decision_reason:
  - lane contract 是独立的 machine-enforced 治理面
  - 先把 `test-lane` 纳入 owner，再继续扩大测试能力，能避免继续裸实现
  - 入口可执行性、lane mismatch 和旧语义参考文档本来就需要同轮收敛
- priority: `P0`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- source_brainstorm: `docs/B1-docs/raw-20260405-1914/brainstorms.md`
- promoted_issue_id: `I-20260405-1914-A`
- promoted_issue_path: `docs/B2-docs/gate/test-lane-routing-and-enforcement-governance/issues/test-lane-routing-and-enforcement-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - this candidate materialized as `I-20260405-1914-A`
  - keep the owner scoped to explicit lane truth, wrapper correctness, machine enforcement, and focused regression
  - keep auto-routing, batch create, and lifecycle automation as later owners
- revisit_trigger:
  - another implementation lands new lane rules without citing this owner
  - `feature-local` is widened back to arbitrary writable branches
  - a future proposal tries to hide lane choice behind implicit inference
