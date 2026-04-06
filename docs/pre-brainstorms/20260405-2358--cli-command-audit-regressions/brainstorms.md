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

## 2026-04-06 canonical followthrough

在 canonical `develop` 上重新回放 `C-20260405-2358-A` 的 CLI 之后，结论已经从“原始全量审计快照”收窄成更明确的 followthrough，但并没有像上一版草稿那样只剩 `.githooks` 一项。

### 已重放的命令

- `./bin/freely sync-tooling --source-project /Users/zhaoyu/Downloads/code/my-freely/freely --project <fresh-git-project>`
  - 结果：成功返回，但目标项目仍缺少 `.githooks`
- `./bin/freely init --project <fresh-git-project> --intent ... --constitution ... --ai codex:gpt-5.4:auto --accept-default-autonomy --force`
  - 结果：在 fresh git project 上仍因缺失 `.githooks` 失败；手工复制 `.githooks` 后可成功初始化
- `./bin/freely baseline-status --project <initialized-project>`
  - 结果：仍返回 0，但 baseline 段 `project:` 继续漂回 Freely root，而不是目标项目
- `./bin/freely status --project <initialized-project>`
  - 结果：`live` 段指向目标项目，但 `baseline` 段仍漂回 Freely root；因此 `status` 只部分尊重 `--project`
- `./bin/freely ensure-interruption-dispatch --project <initialized-project>`
  - 结果：当前通过 doc gate 显式失败，报缺失 `docs/PROJECT_INTENT.md` / `docs/CONSTITUTION.md` / `docs/LAWS.md` / `docs/pre-brainstorms/*`，没有再泄漏原始 `find: ... No such file or directory`

### 收敛结论

1. `baseline-status --project <x>` 的 baseline 面仍错误地指向 Freely root，因此“项目归属已经修好”这个判断是错误的。
2. `status --project <x>` 目前是 split behavior：`live` 段正确，`baseline` 段仍漂移；这说明 `--project` contract 仍未完整闭合。
3. `ensure-interruption-dispatch` 的“原始文件系统噪音”当前不再复现；残留的是合理的 doc gate 阻断，应降级为非回归守卫，而不是 candidate A 的主问题。
4. 当前仍稳定复现、且都发生在 fresh-project first-hop bootstrap 链上的核心缺口有两项：
   - `sync-tooling` 没有为后续 `init` materialize `.githooks`
   - `baseline-status` / `status` 的 baseline 面没有稳定尊重 `--project`
5. 因此 `C-20260405-2358-A` 若继续推进，不应再只缩成 fresh-project hook/bootstrap owner；更准确的边界应是 fresh-project bootstrap 与 baseline scoping followthrough，并把 `ensure-interruption-dispatch` 保留为非回归守卫。

## 明确不做

1. 不把本轮审计直接扩大成一次“全面 CLI 重构”。
2. 不因为 runtime 问题就重开整个 routing foundation 总体架构。
3. 不把 wrapper 可执行位问题与 runtime 语义问题混成同一 issue。

## 初步结论

Freely 目前已经具备较多可运行 CLI 能力，但“命令存在”不等于“命令契约稳定”。本轮全量审计已经给出足够证据，下一步应按三条窄链路分别 materialize，而不是继续无治理地边测边修。
