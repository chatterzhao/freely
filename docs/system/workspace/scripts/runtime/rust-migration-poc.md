# Rust 迁移 PoC：边界、成本与回滚

- 状态：**PoC 文档，未迁移任何代码**。宪法 §4 要求核心运行时/编排器/监控/恢复使用
  Rust；本文件只回答「从哪里切、要花多少、怎么回滚」，不宣称已完成迁移。
- 关联：`split-plan.md`（cmd_* 依赖矩阵）、raw-20261104T075849Z / #4160。

## 1. 先拆 shell，再谈 Rust（顺序不可颠倒）

27k 行单体里，`cmd_*` 只是入口；真正难迁的是 944 个函数之间靠隐式全局变量传状态。
直接重写成 Rust 等于把「隐式耦合」翻译成「显式但错误的耦合」。

因此顺序是：

1. 按 `split-plan.md` 的 phase 1 → 2 把子命令外移到 `bin/<cmd>`，每步行为不变、有测试。
2. 外移完成后，每个 `bin/<cmd>` 的**输入/输出/状态读写**已经是文件级契约（见
   `contracts/cross-process/contract.yaml` 的同类声明），这时才有可描述的函数边界。
3. 只对边界稳定的模块做 Rust 重写，其余继续 shell。

## 2. 候选边界（按可迁移性排序）

| 面 | 现状 | 进 Rust 的理由 | 迁移难度 |
|---|---|---|---|
| 状态文件读写 + 迁移 | `state_file.py`（Python，已有白名单与 TAB+JSON 协议） | 纯函数、有协议、无进程管理，最容易等价验证 | 低：Rust 实现同一协议，双跑比对 |
| 调度决策（slot 选择、重启风暴、退避） | `runtime/freely` 内联，纯计算 + 读状态 | 纯逻辑、可穷举测试 | 中：需要把决策函数与副作用分开 |
| supervisor 循环 | 循环 + spawn + 日志 | 进程管理是 Rust 强项 | 中高：涉及信号、子进程回收 |
| daemon 控制面 | start/stop/status + pid 文件 + flock | 并发与生命周期正确性 | 高：与 shell 版必须能互相接管 |
| A2A / SSE 服务 | Python `a2a_server.py` | 长连接、并发 | 高：协议面大 |
| prompt 模板 / TUI | 字符串拼装 | **不迁**：模板改动频繁，shell/文本更合适 | — |

结论：**第一块进 Rust 的应该是状态文件读写**，因为它有现成协议、有 Python 参考实现、
可以双跑比对，且失败时回滚成本最低。

## 3. 边界形态（三选一，PoC 需要实测）

1. **子进程**：`freely` 调 `freely-state`（Rust 二进制），stdin/stdout 走 JSON。
   优点：零 FFI 风险、可独立发布、回滚=切回 Python 版；缺点：多一次进程启动。
2. **C ABI + shell 调用**：Rust 出 `cdylib`，shell 用一个小 C 包装调用。
   优点：无进程开销；缺点：ABI 脆弱、崩溃会带走调用方，shell 侧难以捕获。
3. **完整重写入口**：`bin/freely` 变 Rust，shell 只留 skill / 脚本。
   优点：终局形态；缺点：一次性风险最大，必须等 1、2 都验证过。

PoC 建议先用 **形态 1**：它和现有 `contracts/cross-process` 的错误信封天然对齐
（退出码 0/3/4、`{"ok": false, "error": {...}}`），不需要新协议。

## 4. 成本（按当前仓库规模估算，含验证）

| 项 | 估算 | 说明 |
|---|---|---|
| 状态文件读写 Rust 化 + 双跑比对 | 3–5 人日 | 协议已定，工作量在边界测试与迁移脚本 |
| 调度决策函数抽离 + Rust 化 | 8–12 人日 | 先要在 shell 内把纯函数与副作用分开 |
| supervisor 循环 Rust 化 | 15–25 人日 | 进程/信号/回收，回归面最大 |
| daemon 控制面 Rust 化 | 20–30 人日 | 需要与 shell 版互相接管、灰度切换 |
| 打包/发布/自举链路改造 | 5–10 人日 | `bin/freely-package`、安装态、`FREELY_PACKAGED_FROM` |

未计入：CI 时长增加（双跑期需要跑两套）、跨平台（macOS 沙箱内 `ps` 已不可用，
Rust 侧要避免依赖被禁的 syscall）。

## 5. 回滚路径

1. **形态 1 的回滚**是一行：把 `bin/<cmd>` 里的 `exec freely-state ...` 换回原 shell 实现。
   前提：shell 实现不删除，只移出调用路径，至少保留一个发布周期。
2. **双跑期**同时保留两套实现，用 `FREELY_STATE_IMPL=shell|rust` 切换；不一致即
   记 `state_impl_mismatch` 事件并 fail-closed 到 shell 版。
3. **形态 3 的回滚**不可行，所以它必须最后做，且必须先有形态 1/2 的线上数据。

## 6. 本轮不做的事（明确）

- 不新增 Rust crate、不改 `Cargo.toml`、不引入 `cdylib`。
- 不迁移任何 `cmd_*` 到 Rust；本轮只是把 3 个子命令从 shell 单体移到 `bin/<cmd>`。
- 不宣称「已按宪法 §4 迁移」——宪法 §4 的一致性仍由后续轮次推进，本文件只给路径。

## 7. 下一步（可直接排期的 PoC）

1. 在 `bin/` 增加 `freely-state` 的 Rust 骨架，只实现 `read` / `values` / `write`，
   协议对齐 `state_file.py`。
2. 增加双跑比对测试：同一批 fixture 分别走 Python 与 Rust，比对 stdout 与退出码。
3. 比对全绿后，把 `state_file.py` 的调用点切到 `FREELY_STATE_IMPL`，灰度一个发布周期。
4. 再评估形态 2，决定是否值得去掉进程开销。
