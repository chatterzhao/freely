# Implementation Decision Note
- issue_id: I-20261110T052506Z-A
- issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261110T052506Z/issues/I-20261110T052506Z-A.md
- decision: plan 透传真实 error；recovery 由 `pr_lifecycle.recovery_for_plan()` 单一真源分类；三处 git 调用共用单一 timeout 常量与 helper
- why_this: R23 收口亲历 GitHub 502/超时导致 3m40s 无诊断失败，重试即成功——fail-closed 是对的，缺的是可观测性；把 timeout 分散到三个调用点会再造一份口径（#4154 同族）。
- alternatives_considered: ①三处各写 timeout 字面量；②recovery 分类内联 adapter；③一个平台失败仍推另一个（破坏双平台一致性）；④自动重试 fetch；⑤放宽 fail-closed。
- boundary_non_goals: 不改 `classify_branch` / 状态集合 / `aggregate_results` / all-or-nothing / 成功路径；不做 failover、自动重试；不修 #4136 噪音。
- residual_risk: ①30s 阈值在极慢网络下可能把可成功的 fetch 判为环境不可用（与既有平台调用 30s 口径一致，fail-closed 方向安全，重试即可恢复）；②recovery 分类依据是 plan 里的 `branch_state`/`error`，若未来新增状态需同步扩充 `recovery_for_plan()` 的失败集合；③`gh api` 与 git 传输通道可能走不同代理，`ls-remote`/`ssh` 探测命令是排障提示而非自动修复。
- verification: AT-001 基线 RED `6 ok / 12 failed` → GREEN `18 ok / 0 failed`；64 组状态矩阵 + 9 组聚合逐项 0 差异；`py_compile`、`check-epics-map`、`bin/test-all --ci`、8 个相关回归基线对比 0 新增失败。
- self_bootstrap_findings: ①基线快照缺 `.freely/tool-boundary-bootstrap.md` 会让打包类回归假 DIFF；②`test-platform-open-parity.py` 在无平台配置的快照里输出 `0 keys` 看似 PASS，实为读通道降级，必须用**未修改 develop 主仓全环境**复跑才能判定，真实失败是 R59 GitHub 副本缺失（goal 已登记）；③既有 `test-command-lifecycle-pr-update.py` 的 mock 用 `**_kwargs` 吸收参数，加 timeout 不需要改夹具；④`gitee` 在 FailingHandler 夹具里拿到 `unsupported` 而非 `absent`，说明 `_handler_for` 返回 None 时观测状态与真实平台不同，AT 断言因此只针对 github 平台。
