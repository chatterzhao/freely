---
candidate_id: C-20261110T052506Z-A
status: promoted
source_raw: raw-20261110T052506Z
created_at: 2026-11-10
milestone: M-20261110T052506Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261110T052506Z-A: guarded PR plan 可诊断 + git 传输超时守卫

- candidate_format_version: v2
- title: plan 保留逐平台 error；`recovery_for_plan()` 单一真源分类文案；`GIT_FETCH_TIMEOUT_SECS` 单一常量 + `run_git()` helper
- status: promoted
- decision_reason: R23 收口亲历 GitHub git 通道 502/超时，plan 只报 `branch_state: error` 且 recovery 误导去同步分支；重试即成功，说明缺的是可诊断性而非流程逻辑。
- next_action: 建 AT-001（4 静态 + 2 对照 + 12 行为）→ 基线 RED → 实现 → 64 组矩阵零退化对比。
- revisit_trigger: 若后续把平台探测改成并发或加重试，timeout 常量与分类文案需同步复核。
- acceptance_criteria:
  - RED：注入 `RuntimeError` 的夹具输出不含真实原因、recovery 仍指向同步分支；fetch 无 timeout。
  - GREEN：每个失败平台带 `error` 与原始摘要；环境类 recovery 含 `ls-remote`/`ssh` 探测命令。
  - GREEN：`ahead`/`diverged` 仍为分支同步文案；`safe_to_execute=false` 与 `actions=[]` 不变；既有 pr-update 回归全绿。
  - GREEN：64 组状态矩阵与 develop 基线 0 差异；真机 `pr-create-guarded` 健康路径双平台成功。
- promotion_gate: AT-001 RED → GREEN + 矩阵零退化 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: executable-reproduction + desk-research
  - summary: 定位 `pr_lifecycle.py:54` 丢 error、`platform-adapter.py:108-121` 无 timeout；实测三远端可达性；逐条证伪 6 个相邻 issue。
  - verdict: pass
- promoted_issue_id: I-20261110T052506Z-A
- promoted_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261110T052506Z/issues/I-20261110T052506Z-A.md
- milestone: M-20261110T052506Z-A
- session_refs: []
