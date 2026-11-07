---
candidate_id: C-20261107T120208Z-A
status: promoted
source_raw: raw-20261107T120208Z
created_at: 2026-11-07
milestone: M-20261107T120208Z-A
---

# Candidates

被否决的替代方案（只改 stop 一处、让 agent 走 daemon、并入 worker contract、收紧门禁判定）见 brainstorms.md。

## C-20261107T120208Z-A: 测试证据有显式写入命令，守护进程不再冒充测试结果

- candidate_format_version: v2
- title: 新增 `freely test-gate record`（started/completed/failed，仅 test 工位、commit 可校验）、`_test_gate_write` 单一写入真源、`cmd_start`/`cmd_stop` 不再写 test-gate.env
- status: promoted
- decision_reason: 测试证据是门禁的输入之一，却没有任何命令能合法写它；唯一的写入者是守护进程生命周期动作，导致「没跑测试也能过门」与「agent 只能手写状态」两个方向的失真。
- next_action: 建 AT-001（6 静态 + 14 行为：写入/拒绝/校验/原子性），改 `runtime/freely`，删 `_update_test_gate` 与其两处调用，补 usage 与 dispatcher。
- revisit_trigger: 若将来引入独立的 test-runner 服务（异步跑测试），`record` 应改为由 runner 回调写入，命令面保留为人工补录入口。
- acceptance_criteria:
  - test 工位执行 `record --status completed` 写入 `TEST_STATUS=completed` + 真实 `LAST_TESTED_AT` + `LAST_TESTED_COMMIT=<HEAD>`，退出 0。
  - 非 `test-pre-merge-*` 工位调用退出 2 且不创建文件。
  - 非法 `--status` 与不存在的 `--commit` 退出 2 且不改文件。
  - `record --status started` 不写 commit；`started → completed` 可推进。
  - `cmd_start` / `cmd_stop` 源码内不再出现 test-gate 写入；`_update_test_gate` 被删除。
  - `_test_gate_write` 定义为唯一写入点且只有一个调用者（`cmd_test_gate_record`）；写入为原子替换，无残留临时文件。
- promotion_gate: AT-001 RED → GREEN + 回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐行核对 runtime 写入点、门禁读取逻辑与 `freely help` 命令面；复现 R10/R11 手写状态与 R12 被 `pretests_not_tested` 阻塞；证伪 #4135/#4151/#4186 覆盖范围。
  - verdict: pass
- promoted_issue_id: I-20261107T120208Z-A
- promoted_issue_path: docs/B2-docs/gate/governance/raw-20261107T120208Z/issues/I-20261107T120208Z-A.md
- milestone: M-20261107T120208Z-A
- session_refs: []
