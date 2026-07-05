# Candidates - 20260322-1615--protected-post-merge-acceptance-route-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260322T161500Z-A: legacy issue
- title: Protected post-merge acceptance route and promotion guard governance
- note: 本候选保留历史形成的 `pre-test-merge` 命名；当前 canonical 语义一律按 `test-pre-merge-*` 临时测试批次前缀族解释。
- problem: Freely 已经允许 `post-merge acceptance` 在 `develop` / `test-pre-merge-*` 这类 protected environment 里发生，而且当前 canonical promote path 也已经固定为 `feature/* -> test-pre-merge-* -> develop`。但 hook 与 promotion/cleanup gate 还没有把“这里只能验证、不能留下新的未归属实现来源”完全兜住。当前能拦 commit，却不能彻底防 raw `git add`；而历史预研里仍残留 replay-only 假设，容易把后续 route 拉回过时模型。
- why_now: Freely 自己的主管位就是必须在主环境里验收的真实案例。若不先把这条路由冻结清楚，后续会持续出现“在 protected env 里测出问题，但修复归属与 promote 方式不清”的治理漂移。
- acceptance_hint:
  - 明确区分 `develop-only completion verification` 与 `test-pre-merge-* batch acceptance`
  - `pr-merge-guarded` / cleanup gate / patrol gate 至少有一层能可靠阻止 dirty protected env 直接 promote
  - `test-pre-merge-*` 明确是临时预集成验证批次，同时也是 `develop` 的 canonical promote family；不得再把旧 replay-only 模型当现行规则
  - 当前批次进入 `develop` 前，必须有足够 evidence 证明 protected env 没有留下未回流、未归属的实现差异
  - Freely 主管位这类主环境验收场景被明确覆盖，而不是只处理普通 feature 测试
- priority: P0
- status: needs_research
- next_action: 对齐当前 canonical truth，收束 `develop-only completion verification`、`test-pre-merge-* batch acceptance`、dirty protected env 回流证据，以及 stale batch / cleanup closeout 的 machine-readable gate；在这些边界冻结前，不把这条线误写成 replay-only 或直接 materialize。
- revisit_trigger: 当 protected verification environment 的 replay policy、failure reroute、machine-readable evidence 与最小 guard 落点可以被冻结成独立 issue contract，或下一次真实 post-merge acceptance 再次暴露 protected-env residue 漂移时。
- decision_reason: 这是 integration-acceptance-first 落地后的下一层治理缺口。没有这层 route/promotion guard，`post-merge acceptance` 仍然容易退化成“在 protected env 里临时操作，然后靠记忆回来源分支修”。
- promoted_issue_path: `pending://protected-post-merge-acceptance-route-materialization`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
