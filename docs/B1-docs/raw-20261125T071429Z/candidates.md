---
candidate_id: C-20261125T071429Z-A
status: promoted
source_raw: raw-20261125T071429Z
created_at: 2026-11-25
milestone: M-20261125T071429Z-A
---

## C-20261125T071429Z-A: I-* 终态判据改为平台取证，关闭通道按 local_id 对账

- candidate_format_version: v2
- title: I-* 终态判据改为平台取证，关闭通道按 local_id 对账
- status: promoted
- design_verdict: 实现偏差
- anchor_refs: docs/system/workspace/ibm-framework.md:128（平台是真源、本地是副本）；docs/system/workspace/scripts/worktree/wt-close:1150-1151（只读清理器，不写 issue 文件）；bin/issue-sync.d/cmd-batch.sh:64（closed 即双方一致的错误假设）；docs/B1-docs/raw-20260621T185519Z/issue.md（--skip-platform 无验证，待加固）
- decision_reason: 选 Option C——判据真源错误与失败不可见必须同时修，任一层单独修都会留下「工位已删、issue 仍开」的路径。
- next_action: 在 `platform-adapter` 增只读副本枚举；`wt-close` Phase 2.5 改为平台取证且 fail-closed；`close_linked` 按 local_id 对账关闭；`cmd-batch.sh`/`pr-merge-guarded` 去 `|| true`；`_already_on_platform` 加平台侧判定。
- revisit_trigger: 平台侧不支持按标题枚举（读能力缺失）或读延迟导致误拒超过 5%。
- acceptance_criteria:
  - 本地 `platform_state: closed` 但平台存在 OPEN 同名副本时，`wt-close --dry-run` 拒绝并打印 OPEN 副本编号。
  - 平台任一 configured platform 不可读时，`wt-close` 拒绝（fail-closed），错误信息给出重试命令。
  - `issue-sync batch` 关闭 I-* 时，未映射到 `platform_ids` 的同类副本也被关闭；任一平台失败则非零退出且不写 `platform_state`。
  - `pr-merge-guarded` 在 batch 非零时中止合并。
  - `platform_ids: {}` 且平台已有同名副本时，batch 不创建重复副本。
- promotion_gate: B1 审计通过 + candidate 入 milestone + I-* 文档建立。
- open_questions: []
- acceptance_reviews:
  - reviewer: b1-independent-review
  - mode: plan-subagent
  - summary: B0 广搜、锚点逐字命中、五方判定与四问齐备，无门禁阻断项。
  - verdict: pass
- promoted_issue_id: I-20261125T071429Z-A
- promoted_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261125T071429Z/issues/I-20261125T071429Z-A.md
- milestone: M-20261125T071429Z-A
- session_refs: []
