# 预研头脑风暴：codex-account-active-probe-governance

## 背景

当前 Codex 账号可用性判断主要依赖本地 `codex-account-cooldowns.tsv`：

- 只有在 rate limit 已经命中后才写 cooldown
- cooldown 记录可能过时
- manager bootstrap 前虽然有 probe，但覆盖范围和触发时机都偏窄

## 问题定义

需要把“账号是否恢复可用”收敛成同一条真源：

- 显式代理下执行 `codex exec "hi"`
- 直接从返回内容提取 `try again at ...`
- 用 probe 结果更新 cooldown 账本

同时不能破坏 Freely 已有约束：

- 自动切号路径必须保留显式切号的校验与 `--dry-run` 语义
- 不能把 rate limit 但未成功解析 reset 时间的结果误判成账号可用
- 不引入高频 watch 轮询

## 目标

1. 统一用 `codex exec "hi"` 主动探测恢复时间
2. 显式设置代理，避免外层 runtime 环境破坏 `codex exec` 网络路径
3. 在 manager bootstrap 前和人工切号场景里都能使用同一套 probe/update 逻辑

## 候选方向

1. 让 probe 返回显式状态枚举，而不是靠“空输出/非空输出”隐式区分
2. 保留 cooldown TSV 兼容格式，同时补充 human-readable 列
3. `freely ai switch codex` 无指定账号时走自动 probe，但真正切换仍复用显式切号主路径

## 验收提示

- rate limit 返回里出现 `try again at ...` 时，能稳定写回 reset 时间
- 所有账号都限流时，会切到最早恢复账号而不是误报可用
- `test-freely-ai-account-switch`、`test-freely-ensure-manager` 继续通过

## 相关落点

- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- `docs/system/workspace/scripts/runtime/ai-cli`
- `docs/system/workspace/scripts/tests/test-freely-ai-account-switch`

