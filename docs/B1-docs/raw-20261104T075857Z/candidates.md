---
candidate_id: C-20261104T075857Z-A
status: promoted
source_raw: raw-20261104T075857Z
created_at: 2026-11-11
milestone: M-20261104T075857Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261104T075857Z-A: 跨进程数据契约 + 边界 runner（第一阶段）

- candidate_format_version: v2
- title: `contracts/cross-process/` 契约 + `cross_process_boundary.py` 三态边界 + lint + 单页文档
- status: promoted
- decision_reason: 三类边界失败（缺字段/类型错/超时）以前不可区分，导致空字符串被当成合法值、类型被强转、超时被当成普通失败；把语义写成可执行断言，比逐点改 22 处夹具更能降低真实风险。
- next_action: AT-001（14 静态 + 3 行为）→ develop `c159e6cef` 基线 RED `0 ok / 17 failed` → 实现 → GREEN `17 ok / 0 failed` → 回归 + CI → PR。
- revisit_trigger: 若后续把 `|| echo` 逐点归零，契约的 `known_gaps` 必须同步删除对应条目，否则 lint 会把已关闭的缺口继续当成开放项。
- acceptance_criteria:
  - RED：无契约、无 runner、无 lint、AT 未接线、epics-map 无 story，且三条边界行为在基线上全部不可执行。
  - GREEN：契约四段（state_file / error_model / timeout / boundaries）齐全且 stdlib 可解析。
  - GREEN：退出码 0–4 与四个 kind 声明齐全，`timeout.exit_code == 4` 且 `distinguishable` 为真。
  - GREEN：≥3 条边界各含 name/error_class/producer/consumer/required_keys，且 producer 文件真实存在。
  - GREEN：runner 三态可执行——缺字段 3、类型错 3、超时 4，超时不得退化成 3。
  - GREEN：lint 0/1/2；AT 进 CORE/CI_CORE；epics-map 注册 story；退出码与 `REFUSE_EXIT=3` 一致。
  - 不退化：不改 `state_file.py`、不改任何 gate 逻辑、不改 `bin/freely`、不动 22 处夹具。
- promotion_gate: AT-001 RED → GREEN + `test-all --ci` 18/0 + epics-map 对齐
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 用 `json.loads` 读 `state_file.py` 的 `ALLOWED_KEYS` 与读写函数确认协议真实语义；用 `git archive develop` 快照复现 RED；三条边界用真实子进程（sh printf / sleep）驱动 runner，不 mock。
  - verdict: pass
- promoted_issue_id: I-20261104T075857Z-A
- promoted_issue_path: docs/B2-docs/data-contracts/cross-process-contract/raw-20261104T075857Z/issues/I-20261104T075857Z-A.md
- milestone: M-20261104T075857Z-A
- session_refs: []
