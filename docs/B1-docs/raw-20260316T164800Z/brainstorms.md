# 研究：Codex reasoning effort 运行时对齐

## Context

- 日期：2026-03-16 16:48 America/Los_Angeles
- 触发：Freely 已能通过 `--ai codex:<model>:auto` 指定 Codex 工具、模型和模式，但在实际狗粮启动时，`medium` 这类 reasoning effort 只能依赖用户全局 `~/.codex/config.toml`，不能由 Freely 项目级运行时显式携带。
- 会话现状：当前仓库已在 dedicated worktree 内启动 `freely start`，并成功拉起 `codex:gpt-5.4:auto`。但 reasoning effort 没有进入 `.freely/config.env`、`freely baseline-status` 或 `monitor-ai-cli.sh` 的显式参数面。
- 约束：
  - 宪法仍规定 Freely 的核心 AI 规格是 `tool:model:mode`，不应把 reasoning effort 塞回这个三段式规范并破坏现有兼容性。
  - Freely 正处于研究优先阶段；来自 chat / session evidence 的新缺口应先进入 `pre-brainstorm`，再决定最小实现。
  - 运行时修改必须保持对现有 `--ai` 调用兼容，不能破坏 `iflow` / `kiro-cli` / `test-sleep` 现有链路。

## 现状观察

1. Freely 只显式保存了 tool / model / mode
- `docs/system/workspace/scripts/runtime/freely` 的 `write_config()` 仅写入 `AI_TOOL`、`AI_MODEL`、`AI_MODE`。
- `cmd_status()` 也只打印三段信息，项目级状态里没有 reasoning effort。

2. Codex CLI 支持用配置覆盖显式传入 reasoning effort
- 本机 `codex exec --help` 支持 `-c key=value` 覆盖配置。
- 本机 `~/.codex/config.toml` 当前已有 `model = "gpt-5.4"` 与 `model_reasoning_effort = "medium"`，说明 CLI 已支持该配置键，只是 Freely 还没接线。

3. 当前狗粮链路依赖“用户全局状态”而不是“项目运行时状态”
- 这会导致 Freely 的自举行为在换机、换账号或切换全局 Codex 配置时产生隐式漂移。
- 也使得 `freely baseline-status` 无法完整表达项目当前到底是以什么模型强度在运行。

## 方案比较

### 1. 把 reasoning effort 塞进 `--ai` 三段式

例如改成 `tool:model:reasoning:mode`

优点：
- 表面上最集中

缺点：
- 直接冲击宪法里已有的 `tool:model:mode` 规范
- 会破坏现有解析和文档约定

结论：
- 不采用，成本太高且不必要

### 2. 继续完全依赖 `~/.codex/config.toml`

优点：
- 零改动

缺点：
- Freely 无法把项目运行配置显式化
- 无法保证狗粮行为可复现

结论：
- 不足以满足“Freely 用 Freely 规则开发自己”的目标

### 3. 给 `freely init` 增加可选 reasoning effort 输入，并在项目状态里显式传播

形式：
- 保持 `--ai tool:model:mode` 不变
- 新增可选 `--reasoning-effort <effort>`
- 写入 `.freely/config.env`
- `freely baseline-status` 显示该值
- `monitor-ai-cli.sh` 仅在 `tool=codex` 时把它翻译成 `-c model_reasoning_effort="<effort>"`

优点：
- 不破坏现有 AI spec
- 项目级运行配置显式、可检查、可复现
- 对其他工具保持兼容

缺点：
- 需要更新 runtime、monitor 和测试

结论：
- 作为最小可行实现面

## 收敛结论

1. 本缺口可以稳定界定为“Codex reasoning effort 项目级运行时显式化”。
2. 最小实现面采用“保留三段式 `--ai` + 新增可选 `--reasoning-effort`”。
3. 首批落点应限制在：
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/monitor-ai-cli.sh`
- 相关回归测试与最小入口文案
4. `iflow` / `kiro-cli` 当前不需要强行接入 reasoning effort，只要求保持向后兼容。
