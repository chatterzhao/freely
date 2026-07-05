# PRD: foreground-background-runtime-entrypoint-semantics-governance

## Goal

把 Freely runtime 的 foreground attached mode 与 background daemon mode 明确拆开，消除用户把 `freely start` 误当长期后台入口的语义歧义，同时保留现有 foreground command contract 和 shared runtime truth。

## Why Now

近期 dogfooding 已经复现两件事同时成立：

1. 当前 `freely start` 是前台 supervisor，会跟随调用会话结束而停机
2. Freely 的产品 intent 和未来 UI/TUI 又需要一个默认可持续运行、不会因关闭前端而自动停机的后台对象

若继续把这两套心智压在同一命令上，用户会把 foreground stop 误判成 runtime bug；而若直接偷改 `start` 默认行为，又会破坏现有 command semantics、event-log、stop、status 与 ownership tests。

## Product Surface

- `docs/system/workspace/scripts/runtime/freely`
- `bin/freely`
- `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `docs/system/workspace/scripts/tests/test-freely-runtime-supervisor-event-log`
- `docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`
- new daemon-focused runtime tests
- `docs/PROJECT_INTENT.md`

## Non-Goals

- 不修复与入口 contract 无直接因果关系的 rate-limit recovery gap
- 不新增 UI 私有 runtime state store
- 不在首轮做全命令面 rename 或 shell 文案大迁移
- 不用 daemon 入口绕开现有 protected-branch / governance / test-lane 约束

## Non-Negotiables

- `freely start` 仍是 foreground attached mode
- 只有显式 `daemon` 前缀才表示后台 runtime control plane
- `stop/status/live-status/fleet-status` 观察的 runtime truth 必须保持单一
- foreground tests 保持有效；daemon 增加独立测试，不替换 foreground 保护面
- UI/TUI 默认关闭前端时不得隐式停止后台 runtime

## Prototype Path

1. 保留现有 `start/restart/stop/status` 实现与基本测试预期
2. 新增 `daemon start|stop|status|logs`
3. `daemon start` 在命令返回后保持 runtime 持续运行
4. `daemon status` / `daemon logs` 继续消费现有 runtime truth 与日志面
5. `daemon stop` 走显式后台停止路径
6. 用 focused regressions 验证父会话结束不会再把 daemon runtime 带死

## Eval Plan

成功：

- foreground `start` 的现有语义与测试仍成立
- daemon 启动后 shell/PTY 结束，runtime 仍保持运行
- daemon 停止、状态、日志附着都能基于 shared runtime truth 正常工作
- daemon 运行时不再把父会话结束误记成 foreground `operator_stop`

失败：

- 为了 daemon 引入而改变 `start/restart/stop/status` 的既有 contract
- foreground 和 daemon 对同一 project runtime 产生两套状态解释
- daemon 仍会在调用会话退出时停机
- 实现顺手掺入 unrelated runtime recovery 逻辑，导致 owner 边界失控

## Dev-Loop Handoff

先把入口 contract 和回归保护面落稳，再决定 daemon restart、短别名、或更大命令面迁移是否值得另开 follow-on。
