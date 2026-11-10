---
candidate_id: C-20261110T074344Z-A
status: promoted
source_raw: raw-20261110T074344Z
created_at: 2026-11-10
milestone: M-20261110T074344Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261110T074344Z-A: cooldown 族首个迁移到安全协议

- candidate_format_version: v2
- title: `state_file.py` 加 `values`/`--kv` 接口；`_read/_write_cooldown_state` 改走协议；全局状态 source 55→54
- status: promoted
- decision_reason: 协议真源已交付但零调用点，注入面未关闭；需要一族完整迁移作为可复制样板，并让边界数字真实下降。
- next_action: 建 AT-001（2 静态 + 6 行为，source 真实 freely）→ 加接口 → 改两函数 → 回归 → 剩余 54 处按族排期。
- revisit_trigger: 若后续族出现非白名单键或位置格式，需先扩充协议再迁移。
- acceptance_criteria:
  - RED：cooldown 族仍 source；旧格式注入经 `_read_cooldown_state` 真的创建 marker。
  - GREEN：AT-001 `8 ok / 0 failed`；TAB+JSON 落盘、旧格式兼容、注入不执行、恶意值逐字节。
  - GREEN：`check-state-file-sources` 计数 54 且 lint 通过。
  - GREEN：R23.9 的 `test-state-file-protocol.py` 与 5 个相关测试 + `test-all --ci` 全绿。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 核对 55 处形态与 cooldown 族边界；验证 macOS bash 3.2 无 mapfile 故用 read；实测旧格式注入 PoC 创建 marker、新协议不创建；确认 `COOLDOWN_SWITCH_*` 无其他下游引用。
  - verdict: pass
- promoted_issue_id: I-20261110T074344Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20261110T074344Z/issues/I-20261110T074344Z-A.md
- milestone: M-20261110T074344Z-A
- session_refs: []
