---
candidate_id: C-20261104T082542Z-A
status: promoted
source_raw: raw-20261104T082542Z
created_at: 2026-11-04
milestone: M-20261104T082542Z-A
---

# Candidates

## C-20261104T082542Z-A: 物化时写入达标 H1 并提供安全回填命令

- candidate_format_version: v2
- title: 复用 Q2 标题契约单一真源，在 pull_raw_issue 落盘时写入前缀无关的 H1，并提供默认 dry-run 的历史回填命令
- status: promoted
- decision_reason: 根因是「平台 title 未进入落盘 payload」，导致本地 _local_record 取不到 H1、parity fingerprint 必然 diverged。修复必须让本地 H1 与「平台 canonical title 去前缀后」的文本一致，因此应当复用 raw_title_contract 而不是另写剥离逻辑；同时 Q2 刚收敛，任何既有函数行为变化都不可接受。批量回填 700 份历史语料风险过高（410 份已 absorbed、18 份多 H1、标题来源不足），改为交付安全命令、不执行批量改写。
- next_action: 写 AT-001 RED（物化应有且仅有一个 H1、幂等、Q2 兼容不退化）；在 raw_title_contract 新增纯函数；adapter 落盘复用；新增 dry-run 回填命令；跑 GREEN 与真实平台副本 fingerprint 对齐验证。
- revisit_trigger: 若未来决定统一历史 raw key 格式或批量回填 700 份语料，另开 issue 评估；本 PR 不改写历史文件。
- acceptance_criteria:
  - 物化后的 issue.md 在 frontmatter 之后有且仅有一个 `# ` 行，且不含 `[RAW-` 前缀。
  - 本地 canonical_projection 的 title / body / fingerprint 与平台副本完全一致（真实双平台副本实测）。
  - 重复 pull 不产生第二个 H1；body 本已有 H1 时不重复注入。
  - Q2 的 canonical_raw_title / is_canonical_raw_title / platform_title 对 805 份真实 issue.md 新旧输出 0 差异；created_at 兼容分支、本地身份不漂移、_resolve_raw_identity 兜底均保留。
  - 回填命令默认 dry-run 且不写文件；标题来源不可靠时 SKIP；已有 H1 逐字节不动；--apply 原子写且幂等。
  - 7 个相关回归测试零新增失败。
- promotion_gate: AT-001 RED → GREEN + 真实平台 fingerprint parity + Q2 退化审计 + 相关回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐行核对 pull_raw_issue 落盘语句、raw-reconciliation-gate._local_record、canonical_projection 前缀剥离；在真实 wt-create 物化结果上确认无 H1；统计 805 份本地 raw 的 H1 覆盖率与多 H1 情况；实测 git show/前缀剥离后 fingerprint 对齐；核对 #4154 与 #4151 的覆盖范围，确认不重复建 issue。
  - verdict: pass
- promoted_issue_id: I-20261104T082542Z-A
- promoted_issue_path: docs/B2-docs/platform/issue-parity/raw-20261104T082542Z/issues/I-20261104T082542Z-A.md
- milestone: M-20261104T082542Z-A
- session_refs: []
