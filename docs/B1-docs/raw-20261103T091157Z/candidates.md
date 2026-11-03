---
candidate_id: C-20261103T091157Z-A
status: promoted
source_raw: raw-20261103T091157Z
created_at: 2026-11-03
milestone: M-20261103T091157Z-A
---

# Candidates

## C-20261103T091157Z-A: 双平台活跃面 issue 对齐 + 本地 raw 元数据回填 + Gitee 搜索分页修复

- candidate_format_version: v2
- title: open issue 双平台对齐与可追溯
- status: promoted
- decision_reason: 总量相等需要为 ~2000 个历史 closed issue 补建镜像，属于无生命周期价值的归档污染；真正会持续造成漂移的是 open 集合与本地元数据。Gitee 搜索只扫第一页使历史镜像无法被身份解析，必须一并修。
- next_action: B2 物化 I-20261103T091157Z-A；先写 Gitee 搜索分页 RED，再修；随后用 adapter pull 物化 13 个双平台 open、关闭 4 个 Gitee 漂移镜像、回填本地编号，最后 parity 校验脚本 RED→GREEN。
- revisit_trigger: 若要求历史 closed 总量也完全一致，需要单独的批量归档迁移设计（不在本 issue）。
- acceptance_criteria:
  - 两平台 open raw key 集合完全相等。
  - 每个 open raw key 均存在 docs/B1-docs/raw-20261103T091157Z/issue.md，platform_ids.github 与 platform_ids.gitee 均非空且等于平台实际编号。
  - 4 个 Gitee-only 漂移镜像关闭并写明理由（GitHub 孪生已 closed）。
  - Gitee search_raw_issue 能分页检索全量 issue（单元测试覆盖第 2 页命中）。
  - `test-platform-open-parity.py` 可重复运行通过。
- promotion_gate: RED→GREEN + parity 校验通过 + governance-merge-gate 通过
- open_questions:
  - 历史 closed 总量差异（GitHub 2610 vs Gitee 471）是否需要在未来做归档级对齐；本 issue 记录为遗留债。
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 审计双平台全量 issue、本地 780 raw 文档 platform_ids 覆盖与 4 个漂移 open 的 GitHub 孪生状态；确认总量不可能低成本相等、活跃面可以完全对齐
  - verdict: pass
- promoted_issue_id: I-20261103T091157Z-A
- promoted_issue_path: docs/B2-docs/platform/issue-parity/raw-20261103T091157Z/issues/I-20261103T091157Z-A.md
- milestone: M-20261103T091157Z-A
- session_refs: []
