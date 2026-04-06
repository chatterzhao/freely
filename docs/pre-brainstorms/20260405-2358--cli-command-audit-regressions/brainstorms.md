# 预研头脑风暴：cli-command-audit-regressions

## 背景

Freely 当前进入 `cli first` 审计阶段，本轮在 dedicated feature worktree 与临时仓库上把 `bin/` 目录中的所有入口都做了真实执行，而不是只看脚本存在性。

审计结果说明当前问题不是单点缺陷，而是三类不同边界的问题同时存在：

1. 面向任意 `--project` 的项目归属与 bootstrap 契约有漂移。
2. runtime / intake / control-plane 在真实启动与恢复路径上仍有脆弱点。
3. 若干 CLI wrapper / test wrapper 的打包与回归入口本身不稳，导致命令不可执行或测试结果不稳定。

## 观测到的直接证据

### 项目归属与 bootstrap

- `./bin/freely baseline-status --project <non-root-project>` 返回 0，但 `project:` 指向 root repo。
- `./bin/freely status --project <non-root-project>` 的 baseline 段同样漂移到 root repo。
- `./bin/freely sync-tooling --source-project <repo> --project <fresh-project>` 后，`freely init` 仍因缺失 `.githooks` 失败，需要手工复制 `.githooks` 才能初始化成功。
- `./bin/freely ensure-interruption-dispatch --project <project>` 在 `.freely/intake` 不存在时退出 0，但直接打印原始 `find: ... No such file or directory`。

### runtime / intake / control-plane

- `./bin/freely start`、`restart`、`stop`、`restore-work` 在审计 worktree 上暴露 stale pid 修复、control-plane readiness 不稳与 stop 时强制 hard-kill 回退。
- `./bin/freely chat --project <audit-worktree> 'cli audit ping'` 记录并 claim intake 后未能干净完成。
- `./bin/freely intake status` 在 claim / resolve 后出现 `items: none`，但 `active_items`、`classified_items`、`absorbed_items` 仍不一致。

### wrapper / 测试打包 / 回归入口

- `./bin/check-tauri-probe-host`、`./bin/tauri-probe-dev`、`./bin/test-freely-fleet-status`、`./bin/test-rust-toolchain-preflight` 直接执行时报 `permission denied`，用 `bash <script>` 才能运行。
- `./bin/ai --help` 能打印 usage，但前置冒出 `mode: command not found`、`apikey: command not found`、`account: command not found`。
- `./bin/test-ai-cli-switch-triggers-auth-change-wake` 在 audit worktree 首次运行失败（缺失 `wake.log`），在 root worktree 复跑通过，说明至少存在 worktree / 环境耦合或用例非稳态问题。

## 路由判断

这些问题不应强行收敛成一个 owner：

1. `--project` 归属漂移与 bootstrap 缺口，属于 project targeting / setup contract。
2. runtime / intake / restore-work 脆弱点，属于 supervision / control-plane contract。
3. wrapper 可执行性与测试入口不稳，属于 CLI packaging / regression-surface contract。

最合理的方式是在同一预研条目下拆成多个 candidate，各自 materialize 成窄 owner。

## 明确不做

1. 不把本轮审计直接扩大成一次“全面 CLI 重构”。
2. 不因为 runtime 问题就重开整个 routing foundation 总体架构。
3. 不把 wrapper 可执行位问题与 runtime 语义问题混成同一 issue。

## 初步结论

Freely 目前已经具备较多可运行 CLI 能力，但“命令存在”不等于“命令契约稳定”。本轮全量审计已经给出足够证据，下一步应按三条窄链路分别 materialize，而不是继续无治理地边测边修。
