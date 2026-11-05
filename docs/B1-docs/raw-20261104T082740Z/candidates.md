---
candidate_id: C-20261104T082740Z-A
status: promoted
source_raw: raw-20261104T082740Z
created_at: 2026-11-05
milestone: M-20261104T082740Z-A
---

# Candidates

## C-20261104T082740Z-A: pretests-gate 字段值解析统一化

- candidate_format_version: v2
- title: 抽出唯一字段解析真源，修复行内代码误判与空值跨行错读，保留 #3957 四格式兼容
- status: promoted
- decision_reason: 8 处复制同一有缺陷正则，且 `\s*` 会跨行把下一行内容读成当前字段值，属于静默错读而非单纯误报；抽成 `_field_line_value()` 后所有调用点共用同一语义，改动局限在单个文件、可由脚本级回归测试完整覆盖。raw issue 只描述了 2 处，预研把范围收敛到 8 处并保留各调用方原有的空值语义，避免「修一个退化一片」。
- next_action: 先写 AT-001 回归测试确认 RED，再实现统一真源，跑 GREEN，最后在 test-pre-merge 工位做基线对比验证零回归。
- revisit_trigger: 若后续要把 pre-tests.md 整体改为结构化 schema（YAML/JSON frontmatter），另开 issue；本 PR 只统一「行内字段值」的读取语义，不改文档格式契约。
- acceptance_criteria:
  - 字段值含 Markdown 行内代码反引号、冒号、`$HOME` 时，字段被完整解析且原样保留。
  - `- requirement:` 等空值字段判定为缺失，绝不吸纳下一行内容。
  - 裸值 / 单引号 / 双引号 / 反引号四种写法在 `parse_fields()`、`parse_scalar()`、`parse_issue_binding()` 下全部得到相同的值（#3957 兼容不退化）。
  - `blocker_taxonomy` 空值行仍算字段存在；`follow_on_to` 空值行仍不算 follow-on；`tasks_path` 空值仍回退到默认 `tasks.md`。
  - 全部 14 个 `parse_fields` 键在值含行内代码时均可解析。
  - 隔离真实 git 仓库中，含行内代码的 pre-tests.md 通过门禁且退出码 0。
  - 与 develop 基线逐项比对，既有测试无新增失败。
- promotion_gate: AT-001 RED → GREEN + test-pre-merge 基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐行核对 pretests-gate 的 8 处字段正则；在未修改的 develop HEAD 上复现 7 项断言失败，并额外确认空值跨行错读、单双引号在 parse_scalar 不支持、#3957 仅修一处。核对 #3957 所在的 raw-20260717T041435Z 治理文档，确认四格式兼容是既有能力，必须保留。另以「基线 gate vs 修复 gate」运行 10 个门禁相关测试，确认 9 个既有失败完全同因、本 PR 零回归。
  - verdict: pass
- promoted_issue_id: I-20261104T082740Z-A
- promoted_issue_path: docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20261104T082740Z/issues/I-20261104T082740Z-A.md
- milestone: M-20261104T082740Z-A
- session_refs: []
