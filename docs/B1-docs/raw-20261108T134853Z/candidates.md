---
candidate_id: C-20261108T134853Z-A
status: promoted
source_raw: raw-20261108T134853Z
created_at: 2026-11-08
milestone: M-20261108T134853Z-A
---

# Candidates

被否决的替代方案（建单后补标签、无条件预建、文档要求人工预建、feedback 层去掉标签重试）见 brainstorms.md。

## C-20261108T134853Z-A: GitHub handler 自动补齐缺失标签并有限重试

- candidate_format_version: v2
- title: `GitHubHandler.ensure_github_labels()` + `create_issue` 在 label-not-found 时补标签并重试一次；其他错误不掩盖；健康路径零额外调用
- status: promoted
- decision_reason: 缺标签让所有 feedback 在 GitHub 侧整单失败，产生只有 Gitee 副本的 PARTIAL raw，直接阻塞自举立项；人工补标签只能救本机，不是机制保证。
- next_action: 建 AT-001（5 静态 + 9 行为，stub `subprocess.run` 驱动真实 GitHubHandler），改 `platform-adapter.py`。
- revisit_trigger: 若 GitHub 未来支持自动建标签，或改用 GraphQL/REST 直接建单，需重新评估失败判定字符串与重试边界。
- acceptance_criteria:
  - RED：stub 首次 `issue create --label` 返回 `could not add label: ... not found` 时，当前 handler 直接返回 error、无 label create、无重试。
  - GREEN：同一 stub 下自动创建每个缺失标签（各一次）、重试一次、返回 created。
  - GREEN：标签已存在时零 label-create 调用、恰好一次 issue create。
  - GREEN：auth 等非 label 错误不重试、不建标签；重试后仍失败有界返回 error；无 labels 的旧路径不变。
  - GREEN：真机 `freely feedback create` 双平台 created（本条 issue 自身即真机证据）。
- promotion_gate: AT-001 RED → GREEN + 16 个相关回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 真机复现 PARTIAL 与报错；核对 R15 AT-001 只验 argv；逐条证伪 #4187/#4194/#4183/#4216/#4221；确认 Gitee 侧无需改动。
  - verdict: pass
- promoted_issue_id: I-20261108T134853Z-A
- promoted_issue_path: docs/B2-docs/gate/platform/raw-20261108T134853Z/issues/I-20261108T134853Z-A.md
- milestone: M-20261108T134853Z-A
- session_refs: []
