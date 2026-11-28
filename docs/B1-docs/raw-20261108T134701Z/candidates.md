---
candidate_id: C-20261108T134701Z-A
status: promoted
source_raw: raw-20261108T134701Z
created_at: 2026-11-08
milestone: M-20261108T134701Z-A
---

## C-20261108T134701Z-A: 入口命令名与 dispatcher 对齐
- candidate_format_version: v2
- title: 删除 unimplemented install 承诺并新增命令名静态契约
- status: promoted
- design_verdict: 实现偏差（入口注释与命令真源不一致）
- anchor_refs:
  - docs/system/workspace/commands.md:41-50（`./bin/install-state-check` / `freely-package --version auto --activate`）
  - docs/system/workspace/scripts/tests/test-install-state-cli.py（27166 行预算、不新增 runtime 分派）
  - docs/B2-docs/gate/platform/raw-20261105T121046Z/code-reviews/implementation-decision-note.md（明确不实现 freely install）
- decision_reason: 实现 freely install 会造成双安装真相源并撞 runtime 行预算；删除承诺 + 静态契约检查是唯一符合设计意图的方案。
- next_action: 进入 B2_IBM 物化 I-20261108T134701Z-A，写 pre-tests 后先跑 RED。
- revisit_trigger: 若未来确有 `freely install` 产品需求，须先废止 `freely-package --activate` 并单独立项。
- acceptance_criteria:
  - bin/freely 注释不再宣称 `freely install` 或自动移除 `@freely-dev-path`。
  - 安装态入口在文档投影中只指向真实存在的命令。
  - 新增静态契约检查：文档/入口注释中承诺的 `freely <cmd>` 必须存在于 dispatcher 或 bin/；对合成反例 fail-closed。
  - runtime/freely 行预算不变（无新分派）。
- promotion_gate: B0 判定为实现偏差，且 Option A 被 27166 行预算与双真相源排除。
- open_questions: []
- acceptance_reviews:
  - reviewer: main-agent
  - mode: B0-five-layer-audit
  - summary: 广搜三类文档，确认 commands.md 与 test-install-state-cli.py 为当前真源，bin/freely 注释过期。
  - verdict: pass
- promoted_issue_id: I-20261108T134701Z-A
- promoted_issue_path: docs/B2-docs/command-wrapper/install-command-parity/raw-20261108T134701Z/issues/I-20261108T134701Z-A.md
- milestone: M-20261108T134701Z-A
- session_refs: []
