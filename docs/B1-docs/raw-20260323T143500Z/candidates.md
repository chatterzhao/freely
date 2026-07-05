# Candidates - 20260323-1435--interactive-init-bootstrap-and-force-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260323T143500Z-A: legacy issue
- title: Interactive init bootstrap and fine-grained force/skip governance
- problem: `freely init` 当前缺少“目录接管 + 空仓 bootstrap + 逐项 skip/force + 非交互 CLI contract + 项目级工具配置 bootstrap + tool adapter 分层”这条统一语义，导致实现退化成了“重写 `.freely/config.env` 的命令”，既不能正确处理空目录 bootstrap，也不能安全地对待已有项目配置，也无法把 `.codex/config.toml` 这类应随 worktree 继承的项目级工具配置与 Claude/Kiro/IfLow 这类参数注入型工具区分对待。
- why_now: 这次狗粮讨论已经明确，`init` 是人工触发的正式接管入口；如果不先把它的 bootstrap 语义写稳，后续再往里塞项目级 Codex 配置、context policy 或 worktrees 访问设置，只会继续扩大偏差，甚至把 Freely 推向不该碰的用户 home 配置。
- acceptance_hint:
  - `init` 先判目录 / git root / repo root，再决定是否 `git init`
  - 非 git 项目可完成 `main -> initial bootstrap commit -> develop`
  - 已有项目上每个 managed item 默认独立 skip，并打印 reason + manual hint
  - 同一套决策必须可由显式 CLI 参数表达，AI / 脚本不依赖交互式问答也能做对
  - `--force` 仅覆盖 Freely-managed bootstrap items，而不是粗暴重写全部项目文件
  - 现有 `main/develop` hook 保护仍成立，bootstrap commit 通过受控路径完成
  - `.codex/config.toml` 等项目级工具配置被版本化并随 worktree 带出
  - Freely 不自动改写用户 `~/.codex/config.toml`，如确有工具前提只输出 manual hint
  - `init` 对不同 AI 工具走统一 adapter contract：项目级配置型工具和参数注入型工具边界清楚
- priority: P0
- status: proposed
- decision_reason: 这是 Freely 自己的正式接管入口定义问题，不是某个局部配置项的小修。它决定 `init` 将来能否稳定承接 `.gitignore`、context policy、project-local tool config 等所有 bootstrap 能力，同时守住“不改用户 home 配置”的边界。
- promoted_issue_path: `pending://interactive-init-bootstrap-and-force-governance`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- next_action: 继续 pre-brainstorm，先冻结 `init` 的 step graph、bootstrap commit 豁免边界、非交互参数面、tool adapter contract，以及每个 managed item 的 skip/force contract；这些边界稳定前，不直接在现有 `init` 上继续堆局部 patch
- revisit_trigger: 当 `init` 的目录接管入口、repo bootstrap 语义、非交互 CLI contract 与细粒度 skip/force 输出 contract 可以被冻结成独立 issue scope 时，重新进入 materialization 判断
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
