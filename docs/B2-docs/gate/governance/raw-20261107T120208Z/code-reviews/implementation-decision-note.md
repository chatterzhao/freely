# Implementation Decision Note
- issue_id: I-20261107T120208Z-A
- decision: 新增 `freely test-gate record` 作为测试证据的唯一显式写入命令；`_test_gate_write` 为唯一写入实现（原子替换）；删除 `_update_test_gate` 及守护进程启停对 test-gate.env 的写入
- why_this: `test-gate.env` 是门禁判断「是否在当前 HEAD 跑过测试」的唯一输入，却没有任何命令能合法写它；唯一写入者是 `cmd_start`（写 `testing` + 新鲜时间戳 + 空 commit → 门禁因 commit 为空跳过新鲜度检查而放行）与 `cmd_stop`（无条件写 `completed` + HEAD）。结果是两个方向的失真：没跑测试也能过门，agent 想合法记录又无路可走（R10/R11 只能手写文件，R12 直接被 `pretests_not_tested` 卡住）。
- alternatives_considered: ① 只改 `cmd_stop`（#4135 的最小修法）—— `start` 的 `testing` 仍能过门，等于没修根因；② 让 agent 通过 `daemon start/stop` 记录 —— `stop` 会 `pkill` 掉 agent 会话，且 daemon 需要 manager/worker 行（鸡生蛋）；③ 把 test-gate 并入 `worker-verification-contract.env` —— 两者生命周期不同，合并会让「谁拥有证据」更模糊（属 #4151/#4162）；④ 顺手把门禁判定收紧为 `== completed` —— 影响历史工位与 #4151 的证据链改造。
- boundary_non_goals: 不改 `pretests-retirement-gate` 判定逻辑；不改 `wt-create` 的初始化标记写入（`not_tested` 是「工位初始化完成」的标记，不是测试结果）；不改 `daemon start/stop` 的进程清理、`write_workcell_state` 落盘与锁顺序；不改 `worker-verification-contract.env` 通道。
- residual_risk: ①门禁仍只排除 `TEST_STATUS=not_tested`，`failed`/`testing` 也会通过 —— 历史工位兼容与证据链改造属 #4151，本轮不收紧（但已不可能再产生新的 `testing`：该写入路径已删）。②`test-gate.env` 仍有两个写入者：`wt-create` 的初始化（`not_tested`）与本命令（测试结果），语义不同、脚本不同，未强行统一（跨脚本引入依赖的收益不足以抵消风险）。③真实 daemon 启停行为未被端到端跑过（会杀掉 agent 会话），只做源码级断言 + 引用删除；`test-command-lifecycle-wt-close.py` 的 1 项预存红与基线一致。④`--commit` 只校验「是该仓库的 commit」，不校验「是否本次测试实际运行的树」，后者属证据内容可信度（#4151）。
- verification: AT-001 develop 基线快照 RED `5 ok / 15 failed` → 工位 GREEN `20 ok / 0 failed`；7 个相关回归 worktree/baseline 退出码全 MATCH；真实自举：用本命令给本轮 test 工位记录 `completed`，`pr-create-guarded` 由 `pretests_not_tested` 变为通过。
- self_bootstrap_findings: 本条即自举产物（R10/R11 手写状态 → 立项）；实现期间复现 R12 被该缺口阻塞，构成「命令解决自己门禁」的真实闭环。未发现其他未被 open issue 覆盖的新缺陷。

## Implementation Decision Note
- decision: test-gate 证据只由 `freely test-gate record` 写，daemon 启停不再写；单一写入实现 + 原子替换
- why_this: 唯一写入者是守护进程生命周期动作，导致「没跑测试能过门」与「agent 只能手写」两个方向的失真
- alternatives_considered: 只改 stop；让 agent 走 daemon；并入 worker contract；收紧门禁判定（#4151）
- boundary_non_goals: 门禁判定、wt-create 初始化标记、daemon 清理与状态写盘、worker contract 通道均不动
- residual_risk: 门禁仍接受 failed/testing（归 #4151）；两个写入者语义分立；daemon 仅源码级验证；commit 不校验实际测试树
