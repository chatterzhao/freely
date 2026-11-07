# PRD: 测试证据有显式写入命令，守护进程不再冒充测试结果

- issue_id: I-20261107T120208Z-A
- source_raw: raw-20261107T120208Z
- workflow_kind: fix
- milestone: M-20261107T120208Z-A
- story: gate/governance

## 目标

「测试是否在当前 HEAD 跑过」这一事实，必须由一条显式、可校验、退出码明确的命令写入；守护进程的启停不得再产生任何测试结论。

## 改动范围（1 个真源 + 1 个测试）

1. `docs/system/workspace/scripts/runtime/freely`：新增 `_test_gate_write` + `cmd_test_gate_record` + dispatcher/usage；删除 `_update_test_gate` 及 `cmd_start`/`cmd_stop` 的调用。
2. 新增 `docs/system/workspace/scripts/tests/test-test-gate-record`（AT-001）。

## 不退化边界

- `wt-create` 初始化仍写 `TEST_STATUS="not_tested"`（初始化标记语义不变，`_wt_test_initialized` 仍可识别任意状态）。
- `pretests-retirement-gate` 判定逻辑不动。
- `cmd_start`/`cmd_stop` 的进程清理、`write_workcell_state` 落盘、锁释放顺序不动。
- `test-command-lifecycle-wt-close.py` 的 1 项预存红不属本轮（归 #4151）。

## 功能需求

- FR-1: `freely test-gate record --worktree <test wt> --status completed` 写入三字段，`LAST_TESTED_COMMIT` = 该工位 HEAD，退出 0。
- FR-2: 非 `test-pre-merge-*` 工位拒绝（rc=2），不创建文件。
- FR-3: `--status` 只接受 `started|completed|failed`；`--commit` 必须存在于该仓库，否则 rc=2 且文件不变。
- FR-4: `--status started` 不写 commit；`--worktree` 省略时用当前目录。
- FR-5: 写入为原子替换（临时文件 + `mv`），不留残留文件。
- FR-6: `cmd_start` / `cmd_stop` 不再写 test-gate.env；`_update_test_gate` 消失。

## 验收

AT-001 基线快照 RED（缺命令、`_update_test_gate` 仍在、daemon 仍写状态）→ 工位 GREEN 20/20；7 个相关回归基线对比零 DIFF。
