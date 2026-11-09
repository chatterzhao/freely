---
candidate_id: C-20261103T132636Z-A
status: promoted
source_raw: raw-20261103T132636Z
created_at: 2026-11-09
milestone: M-20261103T132636Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261103T132636Z-A: 外部输入不再进入代码体；`sed -i` 跨平台且有清理

- candidate_format_version: v2
- title: `pr-review-guarded` 的 2 处分支名插值改 heredoc + argv；6 处 `sed -i ''` 统一 `sed -i.bak` + 同命令删备份；顺带修 `wt-close` 的 `.bak` 残留
- status: promoted
- decision_reason: 外部分支名可合法包含 `'`/`;`/`$`/反引号，插值进 `python3 -c` 等于在 maintainer 机器上执行审查对象的代码；`sed -i ''` 在 GNU 下会让 `pr-review-guarded` 在评审**已记录后**中止，phase 不推进。
- next_action: 建 AT-001（3 静态 + 4 行为，含可执行 PoC）→ 改脚本 → 回归。
- revisit_trigger: 若后续把 `pr-review-guarded` 迁到 python 实现，argv 契约需随之重述。
- acceptance_criteria:
  - RED：基线 2 处插值 + 6 处 `sed -i ''` + 1 处 `.bak` 无清理。
  - RED：PoC 证明插值形式确实执行攻击者代码。
  - GREEN：AT-001 `7 ok / 0 failed`。
  - GREEN：`bash -n` 通过；`bin/test-all --ci` 与相关测试不退化。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 定位 2 处插值（原 issue 报 3 处，行号已漂移）；扫出 6 处 BSD sed 与 1 处 `.bak` 残留；确认 195 处 `python3 -c` 需 lint 而非一次清完。
  - verdict: pass
- promoted_issue_id: I-20261103T132636Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20261103T132636Z/issues/I-20261103T132636Z-A.md
- milestone: M-20261103T132636Z-A
- session_refs: []
