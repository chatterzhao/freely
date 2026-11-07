# Brainstorms: raw-20261107T120208Z

## 问题

`.freely/run/test-gate.env`（`TEST_STATUS` / `LAST_TESTED_AT` / `LAST_TESTED_COMMIT`）回答的是「测试是否在当前 HEAD 跑过」，但它在三处同时错位：

1. **agent 没有合法写入路径**：全仓唯一写入者是 runtime 的 `_update_test_gate()`，调用点只有 `cmd_start`（写 `testing`）与 `cmd_stop`（写 `completed`）。`freely help` 里没有任何 test-gate 子命令；而 `cmd_stop` 的清理动作包含 `pkill -f run-acp-prompt.py` / `claude.*`，agent 调用会杀掉自己 → agent 完成验证后**只能手写该文件**（R10/R11 两轮实际发生）。
2. **daemon 生命周期冒充测试结果（#4135 的根因）**：`cmd_stop` 无条件写 `TEST_STATUS=completed` + `LAST_TESTED_COMMIT=HEAD`。于是「`daemon start` 失败 → `daemon stop`」也会把从未跑过测试的工位标成已完成；而门禁只判 `TEST_STATUS != not_tested` 且 commit 匹配 HEAD，直接放行。
3. **`start` 也在造假**：`cmd_start` 写 `testing` + 新鲜 `LAST_TESTED_AT` + 空 `LAST_TESTED_COMMIT`，门禁在 `_last_tested_commit` 为空时跳过新鲜度比对 → **只要 start 过就能过门禁**，比 stop 那条更隐蔽。

## 证据（本机实测，修复前）

- `grep -rn "test-gate.env" docs/system/workspace/scripts` 只命中 `runtime/freely`（写入）与 `quality/pretests-retirement-gate`（读取）；无任何 CLI 入口。
- `freely help` 全文无 `test-gate`/`test`/`pretests record` 子命令。
- R10（2026-11-07 10:55Z）与 R11（11:51Z）两轮收口时手工 `cat > .freely/run/test-gate.env` 写 `TEST_STATUS="completed"` —— 即伪造封装输出。
- 门禁源码 `pretests-retirement-gate:128` 只排除 `not_tested` 与 epoch 时间戳，`testing` 会通过。
- R12 收口时真实撞门：`pr-create-guarded` 报 `[pretests_not_tested] TEST_STATUS = not_tested`，而没有任何命令能把它变成已测 —— 直接阻塞本轮。

## 证伪（未被现有 open issue 覆盖）

- #4135 讲的是「stop 在 start 失败后仍写 completed」这一条**症状**；本条覆盖的是「状态没有任何显式写入者 + start 也造假 + 语义（测试结果 vs 守护进程状态）混在一起」的**命令面与所有权缺口**（#4135 可在本条语义拆分后按其症状回归）。
- #4151 是测试证据链可验证与替换 CI 桩，属「证据内容是否可信」；本条只保证「状态由谁、以什么命令写入」，不评估证据内容。
- #4186（四态幂等恢复）已修 `wt-create` 的初始化标记判定，未触及运行期写入。

## 关键设计

1. **新增显式命令**：`freely test-gate record [--worktree <abs>] --status started|completed|failed [--commit <sha>]`。仅接受 `test-pre-merge-*` 工位；`completed` 默认记录该工位 HEAD，`--commit` 必须是该仓库内的真实 commit；非法参数 rc=2 且不动文件。
2. **单一写入真源**：`_test_gate_write()` 是唯一写文件的实现，原子写（临时文件 + `mv`），字段集合只在此处定义。
3. **语义拆分**：`cmd_start` / `cmd_stop` 不再触碰 test-gate.env；守护进程状态属于 `workcell-state.env`（`write_workcell_state` 已在写）。删掉 `_update_test_gate` 这一「借测试状态记录运行时状态」的通道。
4. **fail-closed**：非 test 工位拒绝写入（rc=2），而不是 `return 0` 静默跳过 —— 后者会让 agent 以为记录成功。

## 被否决的替代方案

- 保留 `_update_test_gate` 只改 `stop` 那一处（`#4135` 的最小修法）：`start` 的 `testing` 仍能让门禁通过，等于没修根因。
- 让 agent 通过 `daemon start/stop` 记录：`stop` 会 `pkill` 掉 agent 会话，且 daemon 需要 manager/worker 行（鸡生蛋）。
- 把 test-gate 并入 `worker-verification-contract.env`：两者生命周期不同（契约由 manager 在 worker 启动时写），合并会让「谁拥有证据」再次模糊，属 #4151/#4162 的收口范围。
- 顺手把门禁的 `TEST_STATUS != not_tested` 收紧为 `== completed`：会影响历史工位与 #4151 的证据链改造，超出本条。
