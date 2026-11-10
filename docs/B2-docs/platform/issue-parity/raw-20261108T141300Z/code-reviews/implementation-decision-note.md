# Implementation Decision Note
- issue_id: I-20261108T141300Z-A
- issue_path: docs/B2-docs/platform/issue-parity/raw-20261108T141300Z/issues/I-20261108T141300Z-A.md
- decision: 物化时以双平台 `severity/*` 标签为权威写回可选第 22 字段；显式冲突 fail-closed；恢复副本比较对 severity 的区分
- why_this: `feedback --severity` 把 P0/P1 写进 frontmatter 与平台标签，但 `pull_raw_issue` 重建 `fm` 时只取严格 21 字段，开工位那一刻优先级退回默认 P2；R16.5 为放行只能把 severity/* 从 `canonical_projection` 排除。
- alternatives_considered: ①从平台 body frontmatter 复制 severity——body 是创建时快照，不是分诊时的权威视图，且历史 body 可能无 frontmatter；②把 severity 加进 `RAW_METADATA_FIELDS` 变必需字段——会拒绝所有存量 strict 文档；③一方缺标签也 fail-closed——会让 R59 等副本缺失的存量 raw 无法开工位，与 sync-debt 降级机制冲突；④一次性回填历史 raw——issue 明确要求零改写。
- boundary_non_goals: 不改契约字段定义；不回填历史 raw；不动 `phase/*` 排除；不改 `bin/raw-issue-pull` 的 stdout 契约。
- residual_risk: ①一方缺标签、一方有值时采用有值方（有 stderr 告警），若该缺失其实是平台读取降级，仍可能采纳单方视图——由 sync-debt 记录降级，后续 reconcile 可纠；②恢复比较主要强化 platform-vs-platform，本地 record 无 labels 时第二指纹仍跳过标签维度；③平台标签被人工改成 P0/P1 之外的值会被忽略（只认合法三档）。
- verification: AT-001 基线 RED `1 ok / 8 failed`（`P0 survives materialization (found=False)`）→ 工位 GREEN `9 ok / 0 failed`；`test-command-lifecycle-materialization.py` / `test-command-lifecycle-raw-metadata.py` / `test-feedback-severity.py` / `test-raw-reconciliation.py` / `test-raw-replica-degraded.py` / `bin/test-all --ci` 全绿。
- self_bootstrap_findings: ①契约早已支持可选 severity，缺口纯粹是物化接线——先读契约避免重复造能力；②AT 初版把 `parse_issue_text` 的 `(metadata, body)` 元组当 dict 用，误报「解析器读回 P2」，是测试 bug 非实现缺陷；③模板用已 absorbed 的 R17 文档，`pull` 会把 phase 覆盖成 proposed，必须同时清空 `absorbed_into`/`canonical_issue_path`/`completed_at`/`closeout_note`，否则 validate 拒绝。

## Implementation Decision Note
- decision: 标签解析 + 写回可选字段 + 恢复副本比较
- why_this: 物化丢优先级，本地分诊与平台标签不一致
- alternatives_considered: body 复制 / 必需字段 / 缺标签即失败 / 历史回填
- boundary_non_goals: 契约定义、历史 raw、phase 排除、stdout 契约均不动
- residual_risk: 单方视图、第二指纹跳过、非法标签忽略
