# Implementation Decision Note
- issue_id: I-20261110T064015Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20261110T064015Z/issues/I-20261110T064015Z-A.md
- decision: 四层贯通可选 `expected_state` CAS 并在启动 worker 前抢占；SSE 监督者不消费、三处 pid 写统一走 flock claim helper；不删 python watchdog、不再拆新 raw
- why_this: `a2a_task.py` 用 `parse_known_args()` 静默吞掉未登记的 `--expected-status`，server PATCH 与 DB handler 都没有条件更新，派发循环又在 worker 启动之后才写状态 → 同一 submitted 任务可被并发重复派发。SSE 侧三条启动路径、外层 while 包内层 while 的死代码、ensure 把自身 `$$` 写成 consumer pid、三处裸 `echo > pid`，让重复消费者既有路径也没有互斥。两面都属于「并发所有权」，共享同一套夹具与回归。
- alternatives_considered: ①只在 shell 里用 `mkdir` 做任务锁——引入与 DB 状态机不一致的第二套所有权，崩溃需额外回收；②删 python watchdog「只留一条链路」——前置评审证实它只处理 input-required，删掉会丢路由与 staleness 看护；③只加 flock 不动 watch-in-watch——挡不住死代码与 ensure 冒充 pid；④把 SSE 面拆成下一条 raw——同主题、同夹具，再拆会把普查与回归做两遍，且用户明确不要无限拆；⑤放宽 test-all / 改 `|| true` 语义 / 重写派发管线 / 动启动锁与 DB 单实例——分别属 #4157、R23.5、#4155，均超范围。
- boundary_non_goals: 不改 R23.5 的 JSON Lines / NUL 流契约、不改 R19 启动锁与 DB 单实例、不改 `|| true` 的其它容错语义、不改 A2A 六态词表、不删两个 watchdog 的既有事件语义；夹具不访问平台/真实 DB/真实 agent/本机进程。
- residual_risk: ①`cmd_ensure_sse_watchdog_watch` 与 `launch_sse_watchdog` 之间仍有「进程已 fork、pid 文件尚未写」的毫秒级窗口，第二个启动者会在 shell watchdog 内被 claim helper 拒绝，不会成为第二个 consumer，但会短暂存在进程；②CAS 抢占保留 `[[ -f "$_db_path" && -f "$_a2a_task_py" ]]` 守卫，DB/CLI 缺失时退回旧的容错路径（与改前一致），不新增失败模式；③`ps -p -o command=` 不可用时 owner 校验 fail-closed（拒绝接管），极端情况下需 ensure 循环清理 stale pid；④`ensure-sse-watchdog` 非 watch 模式（`:24789`）仍直接启动一次 shell watchdog，靠 claim helper 保证单消费者，未强行改成 detached 以免改变命令语义；⑤`bin/test-all` local 模式既有 `test-github-label-autocreate.py` 失败未处理（develop 基线同样失败）。
- verification: AT-001 基线 RED `2 ok / 18 failed` → 工位 GREEN `20 ok / 0 failed`；GREEN 首轮 `18 ok / 2 failed` 由真实 DB 行为断言抓到 `expected_state` 参数 append 顺序错误，修正后全绿；11 项回归 + 两个状态文件 lint 全绿；`bin/test-all --ci` `7 ok / 0 failed` 且确实执行新 AT。
- self_bootstrap_findings: ①开工前重做真源普查纠正了恢复点的一处错误结论（命令被拒 → 参数被静默吞掉）并否掉 issue 的一条假设（python watchdog 不是重复消费者），避免了照抄旧行号/旧猜测改坏代码；②必须在目标文件上直接 grep 并与调用方交叉验证，全仓 `grep -r .` 曾两次误导（历史教训复用）；③静态断言全绿不等于实现正确，本轮是真实 DB handler 行为测试抓到了 SQL 参数顺序 bug；④`git archive develop` 基线 + 只注入最终版 AT 才能拿到可信 RED，把实现文件一起拷进基线会全绿。

## Implementation Decision Note
- decision: 四层 CAS + SSE 单实例所有权，一轮闭合两面
- why_this: 静默重复派发 + 无互斥的 watchdog pid
- alternatives_considered: mkdir 锁 / 删 python 消费者 / 只加 flock / 再拆 raw / 越界改动
- boundary_non_goals: R23.5 契约、R19 单实例、六态词表、事件语义、容错语义均不动
- residual_risk: 启动竞态窗口、守卫回退、owner 校验失败关闭、one-shot 启动路径、既有 known-broken
