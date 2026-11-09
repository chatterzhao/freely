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
- **拆成 5 个 issue**：共享同一锁语义，拆开会导致实现不一致且无法端到端验证。
