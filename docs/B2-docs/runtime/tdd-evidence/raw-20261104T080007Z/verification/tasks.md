# Tasks: 核心 runtime 建立函数级 RED→GREEN 证据链
- issue_id: I-20261104T080007Z-A
- pre_tests_path: docs/B2-docs/runtime/tdd-evidence/raw-20261104T080007Z/verification/pre-tests.md

## 任务分解

- [x] T1: 建 feature/test 工位（基于 `d315b5409`）。普查：运行时 27,272 行、`tests/` 603 项无 `unit/`、仓库无 PR 模板、`pr-create-guarded` body 默认裸文案、`pr-review-guarded` 无 TDD 检查；确认运行时是 sourceable 库（#4153）。
- [x] T2: 写 AT-001（6 静态 + 4 组行为），develop 基线 RED `2 ok / 19 failed`。
- [x] T3: `tests/unit/harness.sh` + `run.sh`（每测试独立进程、累加 SUMMARY、可 `--list` / 前缀过滤）。
- [x] T4: 14 个函数级测试：状态机 4（state 路径 / desired 读取 / 退出原因 / pid 角色）、锁 4（SSE claim 活主 / 僵尸接管 / 建目录 / 中断 triage）、退出码 4（绝对路径 / 项目解析 / 轮转 / 按数量清理）、事件 1（severity+trace_id）、DB 1（user_version + 新库拒绝）。
- [x] T5: `worktree/pr_body.py`（`## RED 证据` 三段式 + exit 3 拒绝）接入 `pr-create-guarded`；`quality/runtime_red_gate.py`（0/1/2）接入 `pr-review-guarded` Step 2.5。
- [x] T6: 三个历史修复补录 RED：A `6715a67a2`、B/C `83ba84a74`。
- [x] T7: 接入 `bin/test-all` 的 `CORE`/`CI_CORE`（`test-runtime-tdd-evidence.py` + `test-runtime-unit`）；`docs/epics-map.svg` 增 `runtime/tdd-evidence` story（runtime epic 39 story、整体 +26）。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001（RED fidelity） |
| T3, T4 | AT-001（静态 1–5 + runner 行为 2 项） |
| T5 | AT-001（PR body 3 项 + review gate 3 项） |
| T6 | 补录证据（3 份 BACKFILL-*-RED.log） |
| T7 | 回归 + CI + epics-map |
