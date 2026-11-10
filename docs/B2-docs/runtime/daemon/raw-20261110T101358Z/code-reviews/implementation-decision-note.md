# Implementation Decision Note
- issue_id: I-20261110T101358Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20261110T101358Z/issues/I-20261110T101358Z-A.md
- decision: `a2a_task.py` 加 `from __future__ import annotations`；新增 CLI 冒烟 AT 并同时接入 `bin/test-all` 的 `CORE` 与 `CI_CORE`
- why_this: `:435` 把 `:446` 才定义的 `SSEPool` 用作返回类型标注，Python 3.13 在定义时求值 → 模块导入即 `NameError`。派发循环所有 `python3 a2a_task.py ... 2>/dev/null || true` 静默失败，worker 派发停摆；而 `test-all --ci` 全绿，因为没有任何测试真正执行该 CLI 入口。是 #4254 的前置阻塞。
- alternatives_considered: ①把标注改成引号 `'SSEPool'`——只修一处，将来再犯；②把 `SSEPool` 定义上移——要搬 200+ 行、可能改初始化顺序；③改 shell 侧删掉 `|| true` / `2>/dev/null`——属 #4157/R25 可观测性范畴，且不是根因；④重写 `a2a_task.py`——超出本条；⑤只加冒烟不修复 / 只修复不接 CI——前者不解决问题，后者会再次「全绿但起不来」。
- boundary_non_goals: 不改 `:435` 标注文本、不挪 `SSEPool` 定义、不改 SSEPool / A2AClient 实现；不改状态机语义、`--state`/`--status` 参数、`--expected-status`（那是 #4254）、派发循环、`2>/dev/null || true`；不碰 `runtime/freely`；不改 #4254 涉及文件。
- residual_risk: ①A2A Server 未启动时 CLI 仍返回业务错误（预期），派发循环的 `|| true` 容错语义未变，真实 daemon 不可用时仍表现为「没有任务」——这属 #4157/R25，本条只消除加载级根因；②`bin/test-all` local 模式仍有既有 `test-github-label-autocreate.py` 失败（develop 基线同样 `8 ok/1 failed`），本轮未处理；③`from __future__ import annotations` 让整个模块的注解都变成字符串，若将来有代码在运行时读 `__annotations__` 需重新评估（当前未发现此类用法）。
- verification: AT-001 基线 RED `2 ok / 6 failed`（`NameError: name 'SSEPool' is not defined`）→ 工位 GREEN `8 ok / 0 failed`；`bin/test-all --ci` 实际执行新冒烟且全绿；6 个相关测试 + `test-materialize-h1` 全绿。
- self_bootstrap_findings: ①缺陷由 R23.10 的「真源普查」顺带发现，证明「开工前重做普查」的价值；②立项前复核了安装态同样失败、develop 与工位 diff 为空、`git log -S` 定位引入提交，避免立假缺陷；③`bin/test-all` 的 `CORE(` 与 `CI_CORE(` 前缀相同，Edit 精确替换会命中 2 处，用 `replace_all` 恰好一次给两个列表都加上 —— 若只加 CORE，`--ci` 仍会漏掉冒烟；④local 模式的 `test-github-label-autocreate.py` 失败必须与发展基线对比才能确认非本轮引入。

## Implementation Decision Note
- decision: future import + 冒烟 AT 进 CORE/CI_CORE
- why_this: 模块加载即崩，派发链路静默停摆且 CI 无感知
- alternatives_considered: 引号标注 / 上移类定义 / 改 shell 容错 / 重写模块 / 只做一半
- boundary_non_goals: 状态机、参数、派发循环、freely、#4254 文件均不动
- residual_risk: daemon 不可用时仍静默、既有 known-broken、注解运行时读取
