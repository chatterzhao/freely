---
candidate_id: C-20261104T075810Z-A
status: promoted
source_raw: raw-20261104T075810Z
created_at: 2026-11-10
milestone: M-20261104T075810Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261104T075810Z-A: 配置契约落盘 + doctor 可观测类型校验

- candidate_format_version: v2
- title: 新增 `contracts/config/schema.yaml`（58 键）与 `quality/config_schema.py` 单一校验器；`freely doctor` 接线；`contracts/` 随包；本地字符串 `allowed_paths` 现场修正为 list
- status: promoted
- decision_reason: 配置类型错误目前完全静默（`.freely/config.toml:60` 是 str，gate 只认 list 且吞异常），导致豁免配置从未生效且无人察觉；外部项目无法验证配置是否被正确理解。
- next_action: 建 AT-001（12 静态/对照 + 8 行为）→ 基线 RED → 实现 → 回归。
- revisit_trigger: 若后续把角色配置合并为单文件，schema 的 consumers/scope 需同步更新。
- acceptance_criteria:
  - RED：develop 基线无 schema、无校验器、doctor 不报类型/未知键/必填；字符串 `allowed_paths` 静默通过。
  - GREEN：schema 覆盖 58 键且纯 stdlib 可解析；`allowed_paths` 声明 `list[str]`。
  - GREEN：字符串值、未知键、必填缺失均报出 `文件:行号` 与期望类型；bool/int/float 混淆可检出。
  - GREEN：模板生成的配置通过校验；`contracts/` 随包；gate 逐字节未改。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 实测 58 flat key、模板已 list、gate 静默分支在 :408-433、`.freely/config.toml` 为 gitignored；确认 doctor 无配置校验、安装态白名单缺 `contracts/`。
  - verdict: pass
- promoted_issue_id: I-20261104T075810Z-A
- promoted_issue_path: docs/B2-docs/config/toml-parsing-robustness/raw-20261104T075810Z/issues/I-20261104T075810Z-A.md
- milestone: M-20261104T075810Z-A
- session_refs: []
