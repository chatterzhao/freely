---
issue_id: I-20260630T224941Z-A
issue_path: docs/B2-docs/config/config-toml/raw-20260630T224941Z/issues/I-20260630T224941Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260630T224941Z-A
- issue_path: docs/B2-docs/config/config-toml/raw-20260630T224941Z/issues/I-20260630T224941Z-A.md

## Implementation Decision Note

- decision: config.toml.example 为唯一配置真源 + init 只负责复制和代填已知值 + merge lock 写 PID 做死锁诊断
- why_this:
  1. example 与代码默认值长期不一致——修正 example 消除误导
  2. init 不能创建 config.toml 导致 get_config 报错——init 自举解决
  3. merge lock 静默等 300 秒无法区分死锁——PID 检查解决
- alternatives_considered:
  - 在代码中加字段逻辑: 被否决——字段增减应通过编辑 example 实现，不应改代码
  - 懒下载 ACP binary: 体验差，daemon start 卡住
- boundary_non_goals:
  - 不修改 agent-table.toml 结构
  - 不修改 ACP bridge 逻辑
  - 不实现多 tool 同时运行的 ACP bridge
- residual_risk:
  - PROJECT_ROOT 等代填值依赖 git 仓库——非 git 目录需手动填
  - 交互式确认依赖 stdin——CI 环境需 --auto
  - merge lock PID 检查依赖进程表——容器环境可能不准确
