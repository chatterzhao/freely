---
raw_id: raw-20261103T132644Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 前置评审：8 个分项里本轮只做 2 个

#4157 正文明确「分项可各自独立合并」。逐项核对 develop `502496df1` 后：

| 分项 | 现状 | 处理 |
|---|---|---|
| 1. `will now stop` 后 `exit 0` | **仍成立**（`runtime/freely:24144-24149`） | **本轮修复** |
| 2. `bin/freely-watchdog` 失效无人发现 | 成立，但涉及守护进程生命周期 | 汇总 raw |
| 3. `append_runtime_event` 缺 severity/trace_id、88 个调用点无 raw_key | 成立，改动面 120+ 调用点 | 汇总 raw |
| 4. `cycle-*` / `crash-*` 无轮转 | 成立 | 汇总 raw |
| 5. `--output /` / `~` 无守卫 | **已过时**：`bin/freely-package:95-108` 已有 `refuse_dangerous_output`（#4158 已落地） | 不再做 |
| 5b. 打包带出 `__pycache__` / `*.bak.py` | 成立（`cp -R` 后无排除） | 汇总 raw |
| 6a. 无 Python 版本前置检查 | **仍成立**（`bin/freely` 顶部直接 exec） | **本轮修复** |
| 6b. DB 无 `schema_version` / 迁移吞错 | 成立，涉及 DB 迁移协议 | 汇总 raw |
| 7. 凭据进 argv / URL query | 成立，安全类 | 汇总 raw（P1） |
| 8. `.env.example` / `skills/README.md` 文档 | 成立 | 汇总 raw |

选 1 + 6a 的理由：两者都是「失败被表达成正常」且都在单点、可测、无并发语义。
其余分项在 closeout 后由**一条汇总 raw**承接，不逐项建 issue，也不在关闭 #4157 时丢掉。

## 面 1：supervisor 把失败写成 exit 0

`runtime/freely` 的 workcell supervisor 在「没有可用自动恢复路径」时：

```
log_warn "... no auto-recovery path is ready, so local runtime will now stop"
append_runtime_event ... "supervisor_stopping" "reason=$auto_recovery_reason"
_trace_l042_out "TERM"
exit 0
```

外层（systemd / tmux / ensure-manager）看到 0 就不会应用重启策略，于是 workcell 消失
被记成「正常停止」。日志里唯一的异常线索是一行 warn。

### 方向 A：`exit 1` + 事件带 `exit_kind=degraded_no_recovery`（选中）
- 最小改动，外层立即有机会按失败处理；
- 事件里补 `exit_kind`，排障时不必从 warn 文本反推；
- 不新增状态文件，不改变 supervisor 的其它退出路径。

### 方向 B：写 `.freely/run/degraded` 标记文件（否决）
当前没有任何消费者读它；写了也仍是「无人知道」，而且需要额外清理语义。

### 方向 C：只改日志级别（否决）
日志级别不改变进程退出码，systemd 仍然不重启。

## 面 2：缺 Python 版本前置

13 个模块 `import tomllib`（3.11+）。`bin/freely` 是所有 CLI 的唯一入口，但它直接把参数
exec 给 `runtime/freely`，后者在深处才崩。3.8/3.9 上用户看到的是
`ModuleNotFoundError: No module named 'tomllib'` 加一长串 traceback，离真实原因很远。

### 方向 A：`bin/freely` 最前面检查 `sys.version_info >= (3, 11)`（选中）
- 单一入口、最早失败、文案明确；
- 同时检查 `command -v python3`，避免 set -e 直接丢一个无解释的非零；
- 不改变 runtime 内部任何逻辑。

### 方向 B：在 `runtime/freely` 顶部检查（否决为主）
`runtime/freely` 会被测试直接 source/执行，插入硬退出会改变 sourced 语义（R21 刚收口）；
而且 `bin/freely` 才是用户入口，覆盖它即可。

### 方向 C：用 `python_requires` / 打包元数据（否决）
本项目是 shell + 裸 Python 脚本分发，没有 pip 元数据；运行时检查才是唯一可靠点。

## 被否决
改 `append_runtime_event` 签名、动 120 个调用点、加日志轮转、改凭据传递、改打包
allowlist、改 DB 迁移协议 —— 都属于汇总 raw 的独立分项，混进本轮会让「失败语义」这一
主题失焦，也让 RED 无法聚焦。

## fidelity 基线

- RED 必须证明：`will now stop` 分支仍是 `exit 0`；`bin/freely` 无版本检查；stub 旧版本时
  CLI 仍能跑到 runtime（rc=0，无 Python 报错）。
- GREEN 必须证明：静态三处接线；stub 旧版本 → 非零 + 文案含 `Python >= 3.11`；stub 新版本
  与真实环境 → `--help` 正常（rc=0）。
- RED 的 2 项 PASS 是守卫：stub 新版本与真实环境在改前也应正常。

## 价值判定

- 不过时：两处均在 develop `502496df1` 上实测。
- 不重叠：#4158 只做 output 守卫；#4165/#4179 做证据链与投影一致性；均不覆盖「失败退出码」
  与「Python 前置」。
- 价值：前者决定「出事会不会被重启」，后者决定「新机器首跑能不能看懂报错」。
