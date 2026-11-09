---
raw_id: raw-20261103T132622Z
status: brainstormed
created_at: 2026-11-09
---

# Brainstorms

## 覆盖域（逐个核对 raw issue 的点）

| # | issue 指出的问题 | develop 实测（2026-11-09） | 结论 |
|---|---|---|---|
| 1 | 启动锁 TOCTOU：`mkdir` 后下一行才写 `state.env`，等待方读到 `state_file_missing` 就 `rm -rf` | `state_file_missing` 在 `freely:540` 设置、`:712` 消费；`rm -rf "$lock_dir"` 出现在 `:593,:610,:666,:721,:831` 五处 | 仍成立 |
| 2 | 回收无 age / owner 校验 | `:712` 只看「有无活跃 runtime 进程」，没有锁目录 age、没有 owner_pid/cmdline 校验 | 仍成立 |
| 3 | DB daemon 无单实例 | `freely_db_manager.py` 中 `flock` / `O_EXCL` **零命中**；`_generate_chat_id` 仍写「Single-writer daemon」假设 | 仍成立 |
| 4 | `_cleanup` 删 pid/socket 不校验 owner | 同一文件内 `_cleanup` 未比对 pid 文件内容 | 仍成立 |
| 5 | 派发非幂等（先起 worker 后写状态） | 需在 `freely` 内定位 `launching/working` 更新点 | 待 B2 精确到行 |
| 6 | 第二个派发器（TSV 通道） | 同上 | 待 B2 精确到行 |
| 7 | SSE 三重实例 + watch-in-watch 死代码 | 待 B2 精确到行 | 待 B2 精确到行 |
| 8 | PID 复用（`kill -0` 即判 active） | `project_has_active_runtime_processes` 是判据，需核 cmdline | 待 B2 精确到行 |
| 9 | `pkill -f` 前未转义 `$project` | 待核 | 待 B2 精确到行 |

## scope 判定：一个根因，五个后果面

根因只有一个：**并发安全靠「pid 文件 + 时间戳 + 先检查后动作」，没有原子性原语**。五个面是同一根因的不同出口：

- 启动锁（Bash 文件系统互斥）
- DB daemon 单实例（进程级互斥）
- 派发抢占（状态机 CAS）
- SSE 单链路（避免同一条事件被注入两次）
- PID 复用识别（防止「锁被无关进程占住」）

它们共享同一个解法族（flock / CAS / owner 校验），因此**不拆 issue**——拆开会导致「各修一半、锁语义不一致」，反而更难验证。但 B2 内部按面拆 task，验收按面给 AT。

## 方案方向

### 方向 A：全 flock（推荐）

- 启动锁：`exec {fd}>"$lock_file"; flock -n $fd`，fd 继承给 supervisor 子进程；等待方阻塞在 flock 上而不是轮询 `state.env`。
- DB daemon：`flock -n` 抢 pid 文件，抢到才 bind socket；`_cleanup` 前校验 pid 文件内容 == 自己。
- SSE / sqlite 写入：同一 flock 原语。
- 优点：语义单一、可移植（macOS/Linux 都有 flock）、无需额外进程。
- 风险：`flock` 在 NFS 上语义弱（本项目都在本地盘，可接受）。

### 方向 B：O_EXCL 原子创建

- `mkdir` 本身就是原子的，问题不在创建而在「回收」。可以做 `mkdir` + owner 文件（pid + 启动时间 + cmdline）一次写入（写临时文件后 rename）。
- 优点：不依赖 flock，跨平台一致。
- 缺点：回收判定仍需「owner 是否活着」，而 owner 存活的判定本身有 PID 复用问题——绕不开方向 A 的 owner 校验。

### 方向 C：只加 age 校验，不改锁原语

- 最小改动：`state_file_missing` 分支要求 `age >= stale_secs` 才回收。
- 缺点：把竞态窗口从毫秒级缩到秒级，没有消除；且 DB daemon / 派发 / SSE 三个面完全没覆盖。

**选 A + 必要的 owner 校验**：flock 提供原子性，owner 校验（pid 文件内容 == 自己 + cmdline 匹配）解决 PID 复用。

## 实现约束复核（2026-11-09，开发前）

### 约束 1：macOS 没有 `flock` 命令

```
$ command -v flock   → 不存在
$ python3 -c "import fcntl"  → ok
$ perl -MFcntl=:flock -e 1   → ok
```

issue 方案 1 原文「启动锁改 `flock` 持有 fd 并继承给 supervisor 子进程」在 macOS 上**无法用 shell 直接实现**。项目内已有 canonical 范式：`freely:1621-1650` 用 `python3 - <<'PY'` + `fcntl.flock` 包住「读 seq → 写日志 → 写 seq」临界区。本 issue 复用同一范式，不引入新原语。

**同时否决「fd 继承给 supervisor」**：那会把锁语义从「启动窗口互斥」变成「运行期独占」，导致 `stop` / `restart` / 多实例检测全部改变，超出本 issue 边界。启动锁只需覆盖「启动动作」本身。

### 约束 2：真正常态的 TOCTOU 只有一个窗口

`mkdir`（631）与写 `state.env`（632-636）之间是毫秒级窗口；等待方在 712 读到 `state_file_missing` 就 `rm -rf`（721）。**修复点是回收判定，不是创建方式**：

- 目录锁保留 `mkdir`（它本身就是原子原语）；
- `state_file_missing` 分支必须先看**目录 age**：`age < stale_secs` 视为「对方正在写 state」，继续等待；`age >= stale_secs` 且无活跃进程才回收。

这一条就能把「两个 supervisor 都过门」堵死，且改动面只有 712 一处判定。

### 约束 3：PID 复用需要 cmdline 校验

`kill -0` 成功只证明「这个 pid 存在」，不证明「它是我们的锁持有者」。回收 `stale` 分支前需校验 `owner_pid` 的 cmdline 含本工具路径/关键参数；不匹配则视为 PID 复用，按 stale 处理（而不是无限等待）。

## scope 收敛（本轮 vs 后续）

issue 列了 5 个面。5 面共享同一根因，但同时改会让 AT 无法收敛（并发测试各自需要隔离环境）。按后果严重度收敛：

| 面 | 后果 | 本轮 |
|---|---|---|
| 启动锁 TOCTOU | 双 supervisor、状态文件互相覆盖 | ✅ 本轮 |
| DB daemon 无单实例 | **全项目 DB 不可用** + 自激（5s 重试再起一个） | ✅ 本轮 |
| 派发非幂等（两条派发器） | worker 重复拉起 | ➡ 拆出（见下） |
| SSE 三重实例 + 死代码 | 同一条 state_update 注入两次 | ➡ 拆出 |
| `pkill -f` 未转义 | 误杀同前缀项目 | ➡ 拆出（与 #4156 同族） |

拆出理由：①前两面的后果是「整体不可用/控制面分裂」，后三面是「局部重复/误伤」；②派发与 SSE 需要改状态机与事件链，与锁语义正交，混在同一 PR 会让 AT 覆盖 4 套隔离环境、review 无法聚焦；③issue 原文亦标注 #4156 同族，说明 pkill 属于另一条线。

拆出的三面用 `freely feedback` 单独立项并排进 goal（P1），本 issue 的 candidate 明确写「不覆盖」，避免门禁误判已完成。

## fidelity 基线

candidate 的验收必须能回答「并发下真的只有一个实例吗」，而不是「代码里有 flock 字样」。因此：

- RED 必须**背靠背 / 并发**跑两次真实启动，断言「第二个明确拒绝」而不是「两个都起来了」。
- 不接受「静态断言 flock 存在」作为唯一验收——那只能证明写了关键字。
- 每个面至少一条行为断言；静态断言只做补充。

## 价值判定

- 不过时：9 个证据点里 4 个已实测仍成立，其余待 B2 精确定位。
- 不被覆盖：#4236 / #4148 属文档与门禁，与进程并发无关；#4163（DB 单写者被直连破坏）是本 issue 的下游，**本 issue 是它的前置**（issue 原文亦如此标注）。
- 高价值：后果是「AI 行为怪异」而非崩溃，现场极难定位；且 R20 #4163 依赖本条。

## 被否决

- **只修启动锁**：DB 双 daemon 会导致整个项目 DB 不可用，后果比启动锁更重。
- **引入外部锁服务（Redis/etcd）**：本工具是单机 CLI，引入外部依赖违背「零配置可用」。
- **用 PID 文件 + `kill -0` 作为唯一互斥**：PID 复用会让无关进程永久占锁，`freely start` 30s 后无原因失败——这正是 issue 里的一条。
- **一次性改完 5 个面**：并发测试各自需要隔离环境，混在一个 PR 里 AT 无法收敛、review 无法聚焦；改为本轮两面 + 其余拆独立 issue。
- **`flock` fd 继承给 supervisor**：会把「启动窗口互斥」变成「运行期独占」，改变 stop/restart/多实例检测语义，超出边界；且 macOS 无 `flock` 命令。
