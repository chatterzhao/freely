---
schema_version: '1'
local_id: raw-20261107T120208Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261107T120208Z-A
platform_ids:
  github:
    issue_id: '4216'
    url: https://github.com/chatterzhao/freely/issues/4216
    synced_at: ''
  gitee:
    issue_id: IKTNYG
    url: https://gitee.com/zhaoquan/freely/issues/IKTNYG
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/governance/raw-20261107T120208Z/issues/I-20261107T120208Z-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-07T12:02:08Z'
updated_at: '2026-11-07T12:42:44Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261107T120208Z-A
source_candidate: ''
completed_at: '2026-11-07T12:35:59Z'
closeout_note: ''
---

# fix: test-gate 状态没有 agent 可用的记录命令，只能手写 .freely/run/test-gate.env

workflow_kind: fix

workflow_kind: fix

## 根因

`.freely/run/test-gate.env`（`TEST_STATUS` / `LAST_TESTED_AT` / `LAST_TESTED_COMMIT`）是本仓「测试是否在当前 HEAD 跑过」的状态载体，但**它不是任何命令的可写对象**：

- 唯一写入者是 `docs/system/workspace/scripts/runtime/freely` 中的 `_update_test_gate()`（:8583），调用点只有两处：
  - `cmd_start` → `_update_test_gate "$project" "testing"`（:22586）
  - `cmd_stop` → `_update_test_gate "$project" "completed"`（:22216）
- `freely help` 中没有任何 `test-gate` / `test record` / `pretests record` 子命令；该文件不被任何 CLI 参数写入。
- `cmd_stop` 的清理动作包含 `pkill -f run-acp-prompt.py` 与 `claude.*--session-id`，从 agent 会话内调用会连带杀掉自己 → agent **无法**通过 stop 写入 completed。

结果：agent 在 test 工位完成验证后，没有任何合法路径把「已测试 + HEAD」落盘，只能手写该文件。

## 证据

- 本仓 2026-11-07 R10 / R11 两轮收口时，均手工 `cat > .freely/run/test-gate.env` 写入 `TEST_STATUS="completed"`、`LAST_TESTED_AT`、`LAST_TESTED_COMMIT=$(git rev-parse HEAD)`。手写即伪造封装输出，违反「一切状态由封装命令产生」的约束。
- `grep -rn "test-gate.env"` 全仓：写入方 3 处（`_update_test_gate` 2 处调用 + `wt-create` 的 `_init_test_worktree_state` 初始化），**读取方没有任何存活实现**（`pretests-retirement-gate` 在当前树上已无 test-gate 读取代码）。即当前处于「有人写、几乎没人读、没人能合法写」的三重错位。
- `freely help | grep -i test` 无任何 test 状态相关子命令（仅 `intake` / `issue-sync` 等无关行命中）。

## 影响

- **agent 主路径不可用**：agent 驱动的轮次要么手写状态文件（伪造），要么留下 `TEST_STATUS` 停留在 `testing` 或缺失，二者都让「测试证据」不可信。
- **状态语义与写入者耦合错误**：`TEST_STATUS=completed` 目前只能由 `daemon stop` 产生，而 `daemon stop` 是「守护进程生命周期」操作，不是「测试执行」操作（#4135 已指出 start 失败后 stop 仍写 completed 的语义错误，本条是同一根因的另一面）。
- **新工位初始化与运行期更新是两条独立实现**（`_init_test_worktree_state` 与 `_update_test_gate` 各自拼文件），没有单一真源，字段或格式漂移无法被一处修正覆盖。
- 与 R11 收口的「写通道必须自证已同步、部分成功必须可判」契约同族：状态写入同样需要一条显式、可审计、退出码明确的命令。

## 修复方案（待 B1 评审细化，方向）

1. **新增显式记录命令**（推荐）：`freely test-gate record --status <started|completed|failed> [--worktree <path>] [--commit <sha>]`，仅对 `test-pre-merge-*` 工位生效；写前校验工位与分支，`completed` 时记录 `git rev-parse HEAD`；退出码 0/1，部分/异常显式报错。
2. **收敛写入单一真源**：`_init_test_worktree_state`、`cmd_start`、`cmd_stop`、新命令统一调用同一个 `test_gate_write(status, commit)`，禁止其他位置 `cat >` 该文件（静态断言守护）。
3. **语义拆分**：`TEST_STATUS` 只表达测试执行结果，`daemon start/stop` 不得直接改写为 `completed`；#4135 的「start 失败后 stop 仍写 completed」在本条一并由语义拆分根除（若确认重叠，可在实现时把 #4135 合入本条）。
4. 若评审认为该文件已被 `pretests-retirement-gate` 退役而无消费者，则另一合法终点是**删除该状态与其写入路径**，并由 evidence 链取代；但需先证明没有下游依赖，否则按方案 1 落地。

## 验收标准

- RED：在 `test-pre-merge-*` 工位执行「记录测试完成」的预期命令，当前不存在该命令（`freely help` 无入口 / 未知子命令退出非零）；同时断言 `daemon start|stop` 是当前唯一写入路径。
- GREEN：新命令在 test 工位写入 `TEST_STATUS=completed` + `LAST_TESTED_AT` + `LAST_TESTED_COMMIT=<HEAD>`，退出码 0；非 test 工位调用退出非零且不改文件。
- GREEN：三处写入路径（init / start / stop）与新命令共用同一实现，静态断言保证没有第二处 `cat > ...test-gate.env`。
- GREEN：`daemon start` 失败后 `daemon stop` 不再把未执行过测试的工位标为 `completed`（#4135 场景回归）。
