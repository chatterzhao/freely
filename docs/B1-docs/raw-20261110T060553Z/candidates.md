---
candidate_id: C-20261110T060553Z-A
status: promoted
source_raw: raw-20261110T060553Z
created_at: 2026-11-10
milestone: M-20261110T060553Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261110T060553Z-A: 状态文件安全协议第一阶段（真源 + 边界）

- candidate_format_version: v2
- title: 新增 `runtime/state_file.py`（JSON/TAB 新格式、兼容旧赋值不展开、77 键白名单、to-shell 惰性赋值）与 `bin/check-state-file-sources`（55 处 source 基线只降不升、禁止 eval/exec）
- status: promoted
- decision_reason: 状态文件是 shell 赋值且读侧 `source`，值含 `"`/`$()`/换行即注入或让 supervisor 崩溃；55 处读 + 15 处写需逐组迁移，先交付协议真源与冻结边界，才能让迁移可验证、不会反弹。
- next_action: 建 AT-001（2 静态 + 7 行为，含可执行 PoC）→ 实现模块与 lint → 回归 → 拆逐组迁移 issue 并排进 goal。
- revisit_trigger: 若第二阶段发现新的状态键或位置格式文件，需扩充 `ALLOWED_KEYS` 与协议说明。
- acceptance_criteria:
  - RED：基线无安全模块/lint；旧格式 `source` 的注入 PoC 真的执行。
  - GREEN：AT-001 `9 ok / 0 failed`；恶意值 round-trip 逐字节相等、不执行；未知键读写都拒绝；旧格式读回原样不展开；to-shell 惰性。
  - GREEN：边界 lint 通过（55 处只降不升），安全模块无 eval/exec/subprocess。
  - GREEN：6 个相关测试 + `bin/test-all --ci` 不退化。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 实测 55 处 source（原报 20）、39 处非状态 source、77 个键、位置格式文件；确认 `load_meta_env_snapshot` 白名单先例；判定一轮全迁不可验证，按族拆分。
  - verdict: pass
- promoted_issue_id: I-20261110T060553Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20261110T060553Z/issues/I-20261110T060553Z-A.md
- milestone: M-20261110T060553Z-A
- session_refs: []
