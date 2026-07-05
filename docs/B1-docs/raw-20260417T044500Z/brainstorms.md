# Brainstorms - 20260417-0445--runtime-start-stop-process-lifecycle-and-leak-contract

## Context

`freely` 当前暴露出的不是单一“某个子进程忘了 kill”的问题，而是一个跨三层的 runtime 生命周期缺口：

1. AI 子进程层：
   - `iflow` 在本地状态目录 `.iflow/config` / `.iflow/history` 写失败时会快速退出
   - supervisor 过去会把这类失败当成普通退出并继续盲重启
   - AI 进程如果再 fork 子孙进程，旧逻辑只盯住单个 pid，清理不完整
2. supervisor / watchdog 层：
   - 根项目现场出现多个 `ensure-manager --watch`
   - `stop` 后仍可看到残留的 watchdog / dispatcher / `iflow`
   - 杀掉下游进程后，上游 watcher 还会重新把整套 runtime 拉起
3. CLI 入口语义层：
   - 用户显式执行 `freely start`
   - 用户显式执行 `freely daemon start`
   - 重复启动时，当前实现更偏向“attach / repair / reuse”
   - 这和用户的实际预期冲突：已经运行就应先 `stop`，否则拒绝启动，而不是静默复用

因此这条线的核心不是“再补几个 kill”，而是把 `start / daemon start / stop` 的 CLI-first 生命周期契约钉死，再让 runtime 和 watchdog 服从这个契约。

## Reproduced Facts

### 1. `iflow` 本地状态写失败会触发 fast-exit，但过去会被误判成可盲重启

现场日志已看到：

- `HistoryError: Failed to update project metadata: Error: EPERM: ... /Users/zhaoyu/.iflow/config/projects.json`
- 以及同族的 `.iflow/history/...` 权限失败

这不是用户任务正常结束，而是 tool runtime failure。

这条线已经有最小修复：

- `monitor-ai-cli.sh` 现在会把这类 `.iflow` 本地状态失败归类为 `tool_runtime_failure`
- 不再把它当成普通退出后立即盲重启

### 2. AI 子进程树过去只按单 pid 清理，子孙进程可能残留

对 `monitor-ai-cli.sh` 的分析和回归测试表明：

- 旧逻辑只直接 `kill "$child_pid"`
- 若 AI 进程 fork 出长活子进程，父进程退出后子孙进程可继续留存

当前 worktree 已补了：

- 递归收集 descendant pid
- runtime failure 时 terminate 整棵进程树
- 对应回归测试已通过

因此“AI 子进程树清理不完整”是已确认问题，且已形成一版最小修复。

### 3. 现场真正导致“杀了又来”的不是单个 `iflow`，而是上游 watcher 重复存在

现场实测看到多条常驻：

- `runtime/freely ensure-manager --project <root> --watch --interval 10`

并且不止一个。

这意味着：

- 下游 `iflow` / `monitor-ai-cli` 被杀后
- 上游 `ensure-manager --watch` 仍会继续拉起新的 runtime

所以如果不把 watcher 生命周期收口，单纯修 AI 子进程泄漏只能止一部分血，不能解决“进程风暴”。

### 4. `launch_manager_watchdog` / `launch_interruption_dispatcher` 当前是“无条件再拉一个”

现有实现关键特征：

- `launch_manager_watchdog()` 直接 `nohup ... ensure-manager --watch`
- `launch_interruption_dispatcher()` 直接 `nohup ... ensure-interruption-dispatch --watch`
- 拉起前没有先做“同项目是否已有真实活跃 watcher / dispatcher”的权威发现

而对应的 `manager_watchdog_pid_for_project()` / `interruption_dispatcher_pid_for_project()` 又主要依赖 pid 文件。

这带来两个问题：

1. pid 文件漂了，但旧 watcher 还活着时，可能再拉出一个新的 watcher
2. `stop` 只按 pid 文件杀一份时，额外活着的 watcher 可以漏掉

### 5. `stop_project_runtime()` 目前更像“优先按 pid 文件收尾”，不是“同项目 runtime 全量收敛”

当前 `stop` 会处理：

- `ai.pid`
- `ensure-manager.pid`
- `interruption-dispatch.pid`
- `supervisor.pid` / discover 到的 supervisor

但 watchdog / dispatcher 的发现仍然偏 pid-file first，而不是 authoritative same-project full discovery。

这和用户的真实契约冲突：

- 只要用户执行 `freely stop`
- 不论当前是前台启动、后台启动、daemon 启动、还是 watcher 恢复出来的
- 都不应留下同项目的 supervisor / watchdog / dispatcher / AI 子进程

### 6. 用户显式 CLI 的预期已经明确，不应再继续漂移

用户给出的预期非常清楚：

- 正常重复执行 `freely start`
- 正常重复执行 `freely daemon start`

若检测到已经有运行中的 runtime：

- 要么先要求 `stop`
- 要么直接拒绝启动
- 不应静默 attach / repair / reuse

同时：

- `stop` 必须真的 stop 完整
- 不管是前台还是后台启动
- “项目不允许 stop 没有 stop 完整”

这应被提升为明确的 CLI-first 契约，而不是仅仅当成某次现场抱怨。

## Problem Statement

当前缺的不是单个 kill，而是一个一致的 runtime 生命周期合同：

- 谁可以复用已有 runtime
- 谁必须拒绝重复启动
- stop 的完成定义是什么
- watcher / dispatcher / supervisor / AI 各层如何遵守同一合同

如果没有这个合同，任何局部修复都会继续出现：

- 用户手动 `start` 以为是“启动”
- 实际上 CLI 偷偷 attach 到一个半残 runtime
- `stop` 以为“停了”
- 实际上 watcher 还活着并在几秒后重新拉起

## Required Contract

### A. CLI-first start contract

对用户显式执行的：

- `freely start`
- `freely daemon start`

默认契约应是：

1. 若同项目 runtime 已运行，直接拒绝启动
2. 输出明确错误，告诉用户先执行 `freely stop --project <project>`
3. 若用户明确传 `--force`，才允许执行“先 stop，再 start”

这意味着：

- “attach / reuse / repair”不再是默认用户语义
- 若内部 control-plane 需要复用已有 runtime，应走 internal-only path，而不是复用用户 CLI 语义

### B. stop completeness contract

`freely stop --project <project>` 成功的定义必须是：

在一个有界收敛窗口内，同项目不存在活跃的：

- supervisor
- `ensure-manager --watch`
- `ensure-interruption-dispatch --watch`
- `monitor-ai-cli.sh`
- AI 主进程
- AI 子孙进程

如果还有任何同项目 runtime 进程存活，就不算 stop 完成。

### C. foreground / daemon symmetry contract

不应出现：

- 前台启动能 stop 干净，daemon 启动 stop 不干净
- 或 daemon stop 干净，但前台 supervisor 残留 watcher

用户不应该为“当初是怎么启动的”承担不同的 stop 语义。

### D. internal-runtime contract

watchdog / recovery / control-plane 可以保留内部复用能力，但必须显式和用户 CLI 区分：

- 用户 CLI：默认 reject-if-running
- internal runtime recovery：可走 attach / reuse / repair

否则用户对 CLI 的心智模型会持续错乱。

## Success Criteria

这条线的成功标准必须是可执行、可回归的，而不是“感觉不卡了”。

### 1. Repeated start rejection

在项目已经运行时：

- 再执行一次 `freely start --project <project>`
- 命令应非 0 退出
- 输出中必须明确提示“已运行，先 stop”
- 不得新增第二套 supervisor / watchdog / dispatcher / AI

### 2. Repeated daemon start rejection

在项目已经运行时：

- 再执行一次 `freely daemon start --project <project>`
- 命令应非 0 退出
- 输出中必须明确提示“已运行，先 stop”
- 不得新增第二套 daemon / supervisor / watcher

### 3. Force restart semantics remain explicit

当用户显式执行：

- `freely start --project <project> --force`
- 或 `freely daemon start --project <project> --force`

允许的唯一语义是：

- 先 stop 完整
- 再启动一套新的 runtime

而不是 silently attach。

### 4. Stop convergence

执行：

- `freely stop --project <project>`

在 bounded window 内应满足：

- 同项目 supervisor 数量为 0
- 同项目 `ensure-manager --watch` 数量为 0
- 同项目 `ensure-interruption-dispatch --watch` 数量为 0
- 同项目 AI / AI descendants 数量为 0

### 5. Fast-exit containment

当 `iflow` 因本地 `.iflow` 状态写失败 fast-exit 时：

- supervisor 不应进入 blind relaunch storm
- failure 应被 materialize 为 runtime failure
- 不应留下一棵悬空 AI 子进程树

### 6. Worktree ownership correctness

根项目 runtime 不应长期被 feature worktree 路径下的 runtime script 托管。

至少对用户可见层面，应满足：

- root project 的活跃 runtime entrypoint 必须与 root tooling 一致
- 不允许 feature worktree 的旧 watcher 持续监督 root project

## Design Options

### Option A: 继续保留用户 CLI 默认 attach / reuse

好处：

- 兼容现有部分 attach 测试和行为
- 一些重复 start 操作表面上更“省事”

坏处：

- 和用户预期冲突
- runtime 半残时更难判断应该 attach 还是 repair
- 容易把“重复启动”误变成“静默复用脏状态”

结论：

- 不适合作为这次修复的主方向

### Option B: CLI-first reject-if-running，内部 runtime 保留 attach / reuse

好处：

- 用户语义清晰
- 可以把复杂的 attach / repair 仅留给内部 runtime
- 与 `--force` 形成明确对偶

坏处：

- 需要把用户 CLI 和内部调用路径分开
- 一些现有测试要调整

结论：

- 这是当前最稳妥的主方案

### Option C: stop only by pid files

好处：

- 实现简单

坏处：

- pid 文件漂移时无效
- 已被现场事实否定

结论：

- 不可接受

### Option D: authoritative same-project process discovery + bounded tree termination

好处：

- 能处理 pid 文件漂移
- 能收掉同项目的多份 watchdog / dispatcher / supervisor
- 与 stop completeness contract 一致

坏处：

- 需要更谨慎的 project ownership 校验，防止误杀

结论：

- 这是 stop 侧必须补的能力

## Proposed Direction

第一阶段最小安全修复应同时满足两条：

1. 用户显式 CLI 默认 reject-if-running
2. stop 改为 authoritative same-project full convergence

具体建议：

- 对 `cmd_start` / `cmd_daemon_start`
  - 默认检测同项目是否已有 active runtime
  - 若已有则拒绝启动，并提示先 stop
  - `--force` 走 stop-then-start
- 对内部 runtime 路径
  - 保留 internal-only attach / reuse 能力
  - 不把这层复杂语义暴露给用户默认 CLI
- 对 watchdog / dispatcher
  - 补真实发现函数，不只信 pid 文件
  - `launch_*` 前先查重
  - `stop` 时按同项目所有发现结果逐个收敛
- 对 AI 子进程
  - 保持已经补上的 process-tree termination

## Boundary

这次 pre-brainstorm 不做以下扩 scope：

- 不把所有 runtime 命令统一重构成全新进程管理框架
- 不先做全仓库 daemon / foreground 入口统一抽象重写
- 不先碰和本问题无直接关系的 account / slot / auth-change 机制
- 不把 `memark` 的 launchd 定时任务和 `freely` runtime 混为同一个 bug

`memark` 是独立问题：

- 它由 launchd 定时触发
- 不是 `freely start` 直接拉起的 runtime 子进程
- 它会加重机器负载，但不应和 `freely` 的 stop/start 合同混在一起定义

## Initial Decision

这条线应进入 issue-bound 实施，且 owner 必须围绕以下目标收敛：

1. 明确用户 CLI-first 生命周期契约
2. 禁止默认重复 start / daemon start 的静默 attach
3. 让 stop 对同项目 runtime 进程全量收敛
4. 保持内部 runtime recovery 仍可使用受控 attach / repair
5. 用可回归测试验证“拒绝重复启动”和“完整 stop”
