# Implementation Decision Note

## decision

新增 `harness_config.py` 做归一化/校验/原子 apply；`harness_status.py` 只加 `--role` 与 requirements；`bin/harness-select` 提供 CLI。只写 `{role}_slot`，不改全局 adapter。

## why_this

- UI/CLI/TUI 共用同一后端，不各自写 TOML。
- 先 validate 再备份/写/重读，失败不落盘。
- `fork=degraded` 保留真实信息，不伪装 native。
- 不碰 20K `freely` 单体。

## alternatives_considered

- 直接改 TOML：无校验，拒绝。
- 只做 --role 只读：不闭环。
- 做 UI：C-D 非目标，后续复用 JSON。

## boundary_non_goals

- 不做 `{role}_adapter`、model/effort、自动重启、UI。
- 不实现 DSH 插件（C-E）。

## residual_risk

- TOML 注释/格式在重写时可能变化；用最小行替换，不整文件重排。
- 运行中 session 不重启，需用户下次生效。
- reviewer fork degraded 允许但提示冷启动。
