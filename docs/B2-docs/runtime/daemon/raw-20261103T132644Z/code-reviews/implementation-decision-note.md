# Implementation Decision Note
- issue_id: I-20261103T132644Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20261103T132644Z/issues/I-20261103T132644Z-A.md
- decision: supervisor 无恢复路径时改 `exit 1` 并补 `exit_kind=degraded_no_recovery`；`bin/freely` 在 exec 前检查 Python >= 3.11；#4157 只做分项 1 + 6a
- why_this: `exit 0` 让 systemd/tmux 把 workcell 消失当正常停止、不触发重启；13 个模块依赖 `tomllib`，旧 Python 的首错是深处的 `ModuleNotFoundError`。两者都是「失败被表达成正常/不可诊断」。
- alternatives_considered: ①写 `.freely/run/degraded` 标记——当前无消费者，等于换个方式静默；②只改日志级别——不改退出码，外层仍不重启；③把版本检查放 `runtime/freely` 顶部——会改变被 source 的语义（R21 刚收口），且用户入口是 `bin/freely`；④用打包元数据 `python_requires`——本项目是裸脚本分发，没有 pip 元数据；⑤把 8 个分项全塞进本轮——RED 会失焦，且凭据/守护进程/120 调用点风险不成比例。
- boundary_non_goals: 不改 `append_runtime_event` 签名与其余调用点、不改 supervisor 其它退出路径、不改 `runtime/freely` source 语义、不改打包 allowlist/DB 迁移/凭据/日志轮转。
- residual_risk: ①`exit 1` 可能让某些外层包装器（当前仓库内未发现以 0 为前提的消费者）多打一条失败日志；②版本检查只覆盖 `bin/freely` 入口，直接 `bash runtime/freely` 仍会以 `ModuleNotFoundError` 失败（测试与高级用户路径，文档已注明入口约束）；③stub 只拦截 `-c` 里的 `version_info`/`realpath`，若将来入口改用其它探测方式需重述 AT；④其余 6 个分项依赖汇总 raw，若未及时排期会继续留在平台上。
- verification: AT-001 基线 RED `2 ok / 4 failed` → 工位 GREEN `6 ok / 0 failed`；11 项回归 + `test-all --ci` `9 ok / 0 failed`；local 仅既有 known-broken。
- self_bootstrap_findings: ①正文分项 5 的 output 守卫**早已由 #4158 落地**，照抄 issue 会做重复工，开工前必须逐项证伪；②AT 的 stub 必须精确匹配真实调用的参数位置（`python3 -c <code> <path>` 的路径是 `$3`），否则守卫项会误报，容易把夹具错误当成产品回归；③静态窗口断言要连注释一起检查——把旧值 `exit 0` 写进注释会让断言失败。

## Implementation Decision Note
- decision: exit 1 + exit_kind；入口 Python >= 3.11 前置；只做分项 1+6a
- why_this: 失败被记成正常 + 首错远离真实原因
- alternatives_considered: degraded 文件 / 只改日志 / runtime 顶层检查 / 打包元数据 / 8 项全做
- boundary_non_goals: 事件签名、其它退出路径、source 语义、打包/DB/凭据/轮转均不动
- residual_risk: 外层日志噪音、直接执行 runtime 的路径、stub 口径、剩余 6 项承接
