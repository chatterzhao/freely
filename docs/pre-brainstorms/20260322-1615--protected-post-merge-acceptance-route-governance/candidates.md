# Candidates - 20260322-1615--protected-post-merge-acceptance-route-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260322-1615-A
- title: Protected post-merge acceptance route and promotion guard governance
- note: 本候选保留历史形成的 `pre-test-merge` 命名；当前 canonical 语义一律按 `test-pre-merge-*` 临时测试批次前缀族解释。
- problem: Freely 已经允许 `post-merge acceptance` 在 `develop` / `test-pre-merge-*` 这类 protected environment 里发生，但 hook 与 promotion gate 还没有把“这里只能验证、不能成为新的实现来源”完全兜住。当前能拦 commit，却不能彻底防 raw `git add`；而系统仍残留把 `pre-test-merge` 当成可直接并入 `develop` 的旧语义。
- why_now: Freely 自己的主管位就是必须在主环境里验收的真实案例。若不先把这条路由冻结清楚，后续会持续出现“在 protected env 里测出问题，但修复归属与 promote 方式不清”的治理漂移。
- acceptance_hint:
  - 明确区分 `develop-only completion verification` 与 `test-pre-merge-* batch acceptance`
  - `merge-guarded` / cleanup gate / patrol gate 至少有一层能可靠阻止 dirty protected env 直接 promote
  - `test-pre-merge-*` 明确是 shadow batch，只做测试 merge，不直接 merge 到 `develop`
  - `develop` 只吸收来源 feature replay，并定义 batch manifest 与验证重放要求
  - Freely 主管位这类主环境验收场景被明确覆盖，而不是只处理普通 feature 测试
- priority: P0
- status: proposed
- decision_reason: 这是 integration-acceptance-first 落地后的下一层治理缺口。没有这层 route/promotion guard，`post-merge acceptance` 仍然容易退化成“在 protected env 里临时操作，然后靠记忆回来源分支修”。
- promoted_issue_path: `pending://protected-post-merge-acceptance-route-materialization`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
