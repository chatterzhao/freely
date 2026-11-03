---
issue_id: I-20261102T130603Z-A
issue_path: docs/B2-docs/platform/platform-handler-probe/raw-20261102T130603Z/issues/I-20261102T130603Z-A.md
phase_state: completed
---

- issue_id: I-20261102T130603Z-A
- issue_path: docs/B2-docs/platform/platform-handler-probe/raw-20261102T130603Z/issues/I-20261102T130603Z-A.md

## Implementation Decision Note

- decision: 成功探活进程内缓存；探活走 `_retry_read` 有界重试；新增 `_ensure_handler` 并在 `guarded_pr_update` 执行循环中对 None 结构化失败。
- why_this: 探活是网络动作且会抖动，失败不应把平台判死，也不能在 execute 阶段解引用 None；收敛在注册层可单测且不改消费方。
- alternatives_considered: 只看配置不探活（把不可用误判为可用）；调用方各自重试（18 处消费漂移）。
- boundary_non_goals: 不改平台 handler 实现/注册表/configured_platforms/gate 语义。
- residual_risk: 进程内缓存不会感知运行中凭据失效；需要新进程或失败后的显式刷新（当前在每次 CLI 进程内天然刷新）。
