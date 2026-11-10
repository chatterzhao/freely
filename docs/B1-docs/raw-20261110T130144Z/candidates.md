---
candidate_id: C-20261110T130144Z-A
status: promoted
source_raw: raw-20261110T130144Z
created_at: 2026-11-10
milestone: M-20261110T130144Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261110T130144Z-A: issue-sync 拆子命令模块 + 平台投影单一份契约 + bootstrap delete 收口

- candidate_format_version: v2
- title: `bin/issue-sync` 拆成 dispatcher + `issue-sync.d/*.sh`；`sync/issue_create_contract.py` 统一 body/标签；`bootstrap --delete` 改走 adapter
- status: promoted
- decision_reason: 1330 行单文件让每个子命令都无法单独 source/断言；`feedback` 与 `issue-sync create` 各自渲染 body 与标签（一个硬编码字面量、一个 `awk` 假剥离），第三个入口出现时会再次分叉；`bootstrap` 的直连删是 adapter 之外唯一平台写且未登记。
- next_action: AT-001（24 静态 + 11 行为）→ develop 基线 RED `6 ok / 29 failed` → 实现 → 工位 GREEN `35 ok / 0 failed` → 回归 + CI → PR。
- revisit_trigger: 若新增平台写入口或 `feedback edit` 也改投影形状，需把契约扩到 update 路径并重述边界。
- acceptance_criteria:
  - RED：`bin/issue-sync` 1330 行且无 `issue-sync.d`；无 `issue_create_contract.py`；`feedback` 含 `kind/raw,phase/proposed` 字面量；`bootstrap` 直连 `gh issue delete`。
  - GREEN：主文件 ≤ 665 行且不含任何 `cmd_*` 定义；9 个 `cmd-*.sh` 各自定义对应函数；契约模块拥有 `strip_frontmatter` / `platform_body` / `labels_for`；两条 create 路径的 body 与标签逐字相同（行为断言）；`bootstrap --delete` 经 `issue-write-one github delete` 且 `gh` 收到 adapter 解析出的 repo。
  - GREEN：`test-issue-sync-*`、`test-platform-*`、`test-feedback-severity`、`test-frontmatter-ownership`、`test-command-lifecycle-*` 全绿；`test-all --ci` 12/0。
  - 不退化：`issue-write-one` 契约、0/3/1 退出码、promote/close 行为、`raw_title_contract` 投影不变。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 普查 `_issue_body` 的 awk 语义、`pull_raw_issue` 对 frontmatter 的依赖、`feedback` 的标签字面量、`bootstrap` 的 delete 路径；用 `git archive develop` 基线跑最终版 AT 得 RED `6/29`；14 个模块按行区间机械切分后逐项 `bash -n`。
  - verdict: pass
- promoted_issue_id: I-20261110T130144Z-A
- promoted_issue_path: docs/B2-docs/platform/issue-sync-modules/raw-20261110T130144Z/issues/I-20261110T130144Z-A.md
- milestone: M-20261110T130144Z-A
- session_refs: []
