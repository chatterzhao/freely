# Implementation Decision Note
- issue_id: I-20261105T122053Z-A
- decision: 读通道记录 read_health，聚合层在读失败时产出 __degraded__ 并复用 scan 既有降级消费者；parity 降级跳过；健康路径零变化
- why_this: 「读取失败」被压成空字典后，生命周期扫描会把 57 条真实 GitHub open issue 当作不存在，parity 报出假差异，可能据此误推进或误清理。用户要求「优秀的 freely」，平台故障与平台无 issue 必须在结果里可区分。
- alternatives_considered: 改 scan 的 `get_platform_open_issues()`（评审发现多余，scan `:773` 已消费 `__degraded__`）；把聚合结果改成包裹结构（破坏所有调用方与验收标准）；删除 REST 回退（丢失独立通道）；让聚合层抛异常（中断调用方）；把失败标记当普通 issue 记录（污染集合）；改 `pull_raw_issue()` 或写通道（越界到 R6 / R11）。
- boundary_non_goals: 不改 `task-lifecycle-scan.py` 真源；不改 `pull_raw_issue()` 读源选择（R6）、写通道、`_discover_one` 的 unknown/missing/ambiguous 语义；不夹带 R11/#4149、R8/#4146、#4151。
- residual_risk: ①`__degraded__` 是 dict 中的保留键，若未来换成分页流式接口需另开 issue 调整传递方式。②parity 在降级时返回 0（SKIP），调用方若把 0 解读为「parity 已验证通过」需自行看输出；当前文案明确写 NOT evaluated。③平台写通道静默失败仍待 R11/#4149。
- verification: AT-001 基线 RED 5 失败 / 4 既有能力 PASS → GREEN 9 项全通过；健康路径 fixture 107 条与真实双平台 102 条均无 `__degraded__`；handler 异常不产生假记录；13 个回归全 PASS，12 个回归以未修改 develop HEAD 基线对比 0 新增失败；check-epics-map 对齐。
- self_bootstrap_findings: 本轮未发现「现有 open issue 未覆盖」的新缺陷；相邻现象已被 R11/#4149、R8/#4146、#4151 覆盖或由 R6 完成，未重复立项。
