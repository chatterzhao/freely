# 预研头脑风暴：cli-command-audit-regressions

## 背景

Freely 当前进入 `cli first` 审计阶段，本轮在 dedicated feature worktree 与临时仓库上把 `bin/` 目录中的所有入口都做了真实执行，而不是只看脚本存在性。

审计结果说明当前问题不是单点缺陷，而是三类不同边界的问题同时存在：

1. 面向任意 `--project` 的项目归属与 bootstrap 契约有漂移。
2. runtime / intake / control-plane 在真实启动与恢复路径上仍有脆弱点。
3. 若干 CLI wrapper / test wrapper 的打包与回归入口本身不稳，导致命令不可执行或测试结果不稳定。

## 观测到的直接证据

### 项目归属与 bootstrap

- `freely baseline-status --project <non-root-project>` 返回 0，但 `project:` 指向 root repo。
- `freely status --project <non-root-project>` 的 baseline 段同样漂移到 root repo。
- `freely sync-tooling --source-project <repo> --project <fresh-project>` 后，`freely init` 仍因缺失 `.githooks` 失败，需要手工复制 `.githooks` 才能初始化成功。
- `freely ensure-interruption-dispatch --project <project>` 在 `.freely/intake` 不存在时退出 0，但直接打印原始 `find: ... No such file or directory`。

### runtime / intake / control-plane

- `freely start`、`restart`、`stop`、`restore-work` 在审计 worktree 上暴露 stale pid 修复、control-plane readiness 不稳与 stop 时强制 hard-kill 回退。
- `freely chat --project <audit-worktree> 'cli audit ping'` 记录并 claim intake 后未能干净完成。
- `freely intake status` 在 claim / resolve 后出现 `items: none`，但 `active_items`、`classified_items`、`absorbed_items` 仍不一致。

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

- `freely sync-tooling --source-project /Users/zhaoyu/Downloads/code/my-freely/freely --project <fresh-git-project>`
  - 结果：成功返回，但目标项目仍缺少 `.githooks`
- `freely init --project <fresh-git-project> --intent ... --constitution ... --ai codex:gpt-5.4:auto --accept-default-autonomy --force`
  - 结果：在 fresh git project 上仍因缺失 `.githooks` 失败；手工复制 `.githooks` 后可成功初始化
- `freely baseline-status --project <initialized-project>`
  - 结果：仍返回 0，但 baseline 段 `project:` 继续漂回 Freely root，而不是目标项目
- `freely status --project <initialized-project>`
  - 结果：`live` 段指向目标项目，但 `baseline` 段仍漂回 Freely root；因此 `status` 只部分尊重 `--project`
- `freely ensure-interruption-dispatch --project <initialized-project>`
  - 结果：当前通过 doc gate 显式失败，报缺失 `docs/PROJECT_INTENT.md` / `docs/CONSTITUTION.md` / `docs/LAWS.md` / `docs/B1-docs/raw-*`，没有再泄漏原始 `find: ... No such file or directory`

### 收敛结论

1. `baseline-status --project <x>` 的 baseline 面仍错误地指向 Freely root，因此“项目归属已经修好”这个判断是错误的。
2. `status --project <x>` 目前是 split behavior：`live` 段正确，`baseline` 段仍漂移；这说明 `--project` contract 仍未完整闭合。
3. `ensure-interruption-dispatch` 的“原始文件系统噪音”当前不再复现；残留的是合理的 doc gate 阻断，应降级为非回归守卫，而不是 candidate A 的主问题。
4. 当前仍稳定复现、且都发生在 fresh-project first-hop bootstrap 链上的核心缺口有两项：
   - `sync-tooling` 没有为后续 `init` materialize `.githooks`
   - `baseline-status` / `status` 的 baseline 面没有稳定尊重 `--project`
5. 因此 `C-20260405-2358-A` 若继续推进，不应再只缩成 fresh-project hook/bootstrap owner；更准确的边界应是 fresh-project bootstrap 与 baseline scoping followthrough，并把 `ensure-interruption-dispatch` 保留为非回归守卫。

## 2026-04-06 command-surface followthrough

在后续的 canonical CLI surface audit 中，又出现了一组不适合塞回 `C-20260405-2358-A` 或 `C-20260405-2358-B` 的命令契约问题。

### 已重放的命令

- `./bin/freely`
  - 结果：打印 usage，但返回码为 1；当前更像“缺参数 usage”而非标准 help surface。
- `freely wt-create --help`
  - 结果：没有进入 help 分支，而是把 `--help` 当成 branch 名继续执行，最终落到 `git branch`/`invalid reference` 错误。
- `./bin/wt-enter --help`
  - 结果：返回 `Please run with: source bin/wt-enter <branch>`，没有标准 `--help` 契约。
- `./bin/wt-add --help`
  - 结果：返回 `Please run with: source bin/wt-add [branch] -- <git-add-args>`，没有标准 `--help` 契约。
- `freely pr-merge-guarded --help`
  - 结果：打印 usage，但退出码仍为 1，而不是 clean help 成功返回。
- `./bin/ai list --format json`
  - 结果：成功列出保存的 slots。
- `./bin/ai whoami codex --format json`
  - 结果：成功显示当前 active slot 为 `apikey-custom-2`。
- `./bin/ai status codex --format json`
  - 结果：成功显示 auth present 和 slot cache 信息。
- `./bin/ai login codex apikey --dry-run --yes --format json`
  - 结果：成功走 dry-run，打印将保存到新 slot 的路径。
- `./bin/ai switch codex --dry-run --format json`
  - 结果：在当前 active apikey slot 明明存在的情况下仍返回 `No slots found or all probing failed`；说明 dry-run switch 的 fallback/probe/JSON contract 仍不稳定。

### 收敛结论

1. 这组问题已经不再是“wrapper 可执行位”本身，而是 help / usage / dry-run / exit-code contract 的一致性缺口。
2. `wt-create --help` 的问题具备副作用风险，因为它会误走 branch/worktree 创建路径，而不是停在帮助输出。
3. `pr-merge-guarded --help`、`wt-enter --help`、`wt-add --help` 暴露的是 command ergonomics 与 CLI-first contract 不一致，不应继续依赖操作者记忆。
4. `ai switch codex --dry-run --format json` 的失败不适合归到 fresh-project bootstrap，也不应直接等同于 runtime/control-plane 生命周期问题；它更像 ai command surface 的 follow-on contract 漂移。
5. 因此这批证据应独立成新的 candidate，而不是继续扩大 `C-20260405-2358-A/B/C` 的边界。

## 明确不做

1. 不把本轮审计直接扩大成一次“全面 CLI 重构”。
2. 不因为 runtime 问题就重开整个 routing foundation 总体架构。
3. 不把 wrapper 可执行位问题与 runtime 语义问题混成同一 issue。

## 初步结论

Freely 目前已经具备较多可运行 CLI 能力，但“命令存在”不等于“命令契约稳定”。本轮全量审计已经给出足够证据，下一步应按三条窄链路分别 materialize，而不是继续无治理地边测边修。
