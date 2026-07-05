# Brainstorm: supervisor bash rc=0 crash

Key: `raw-20260517T082453Z53Z`
Date: 2026-05-17 08:25 UTC
Source: chat-inbox (github raw issue #503)

## 0. 价值与时效性审视

**提出时间**: 2026-05-17T08:24:53Z（今日）
**来源**: chat-inbox（GitHub issue #503），来自运行时监控上报
**当前相关性**: 高。本 issue 描述了 supervisor 监控到 bash 进程以 rc=0 退出后标记为 crash。该现象直接影响 auto-loop 的进程生命周期管理——如果正常退出被错误分类为 crash，会导致不必要的重启风暴或恢复开销。

**已有相关覆盖**:
- `20260308-1930--business-block-vs-system-crash-recovery` 讨论了 blocked_* 与 system crash 分层，但未关注 rc=0 正常退出的分类问题
- `M-20260508T225041Z-A` (ACP bridge restart storm) 处理了 ACP bridge 的快速重启，但聚焦于 cooldown，未区分 rc=0 语义
- `20260324-0405--watchdog-restart-storm-and-process-churn-detection` 讨论了重启风暴检测，未涉及退出码歧义

**判定**: 值得投入。rc=0 表示 bash 进程正常退出，但 supervisor 将其标记为 "crash"——这存在分类歧义，需要澄清是 supervisor 误报还是预期的生命周期事件。

## 1. 背景与来源

raw issue 数据:

| 字段 | 值 |
|------|-----|
| title | "supervisor crash: bash rc=0" |
| body | supervisor crash: bash at freely:18777 (rc=0) |
| last_exit_reason | set_e_exit_cmd=bash@freely:18777_rc_0 |
| tool | cc-ds-flash-auto |
| adapter | acp |
| launch_kind | prompt |
| priority | P2 |

## 2. 现场分析

### 2.1 关键信号

- **rc=0**: bash 以退出码 0 退出，即正常退出
- **`set_e_exit_cmd`**: 注释指明 exit 由 bash `set -e` 触发
- **`bash@freely:18777`**: 上下文是 PID 18777 的 bash 进程
- **tool=cc-ds-flash-auto**: Claude Code DeepSeek Flash 自动模式
- **adapter=acp**: 使用 ACP (Agent Communication Protocol) 适配器
- **launch_kind=prompt**: 一次性 prompt 启动（非 resume）

### 2.2 rc=0 with set -e 矛盾分析

`set -e` (errexit) 仅在命令返回非零时触发。如果 bash 以 rc=0 退出，有两种可能：

1. **set -e 触发后，进程树中的某个 sub-shell 返回了 rc=0**: `set_e_exit_cmd` 仅是 exit 原因的溯源标签，不一定对应最终的 shell exit code。
2. **正常执行完毕**: bash 完成所有命令后以最后的 rc=0 退出，但 supervisor 预期进程应该持续运行，因此将任何 exit 都标记为 crash。

### 2.3 监控脚本 (monitor-ai-cli.sh) 行为

监控流程:
```
1. 启动 tool 进程作为子进程
2. 在 while kill -0 循环中监控存活
3. 进程退出后，wait 获取 child_rc
4. 若 child_rc != 0，发送 KILL 到进程树
5. 退出时传递 child_rc
```

关键点：监控脚本本身**不区分 rc=0 vs rc!=0 的语义**——它仅传递退出码。crash 分类由上层 supervisor 控制面完成。

## 3. 发散

### 3.1 可能性 A: 预期正常退出被误分类为 crash

cc-ds-flash-auto 完成任务后 bash 正常退出 (rc=0)。上层 supervisor 将 "进程不再运行" 一律视为 crash，未识别正常退出的生命周期语义。

**支持信号**: rc=0, launch_kind=prompt（一次性启动预期会终止）

### 3.2 可能性 B: 非预期提前退出

bash 在 AI CLI 会话尚未完成时意外退出。set -e 触发导致进程链断裂，但最终 shell 仍返回了 rc=0 因为上层捕获处理。

**支持信号**: set_e_exit_cmd 表明存在 set -e 触发

### 3.3 可能性 C: ACP 适配器行为差异

ACP 适配器的进程生命周期管理不同于其他适配器。ACP bridge 使用 stdio transport，断开后 bash 进程可能因管道关闭而退出，但退出码仍为 0。

**支持信号**: adapter=acp, 已知 ACP restart storm 历史

## 4. 收敛

### 4.1 最可能解释

**可能性 A 最可能**。理由：
1. rc=0 强信号：正常退出几乎不可能被误报为异常退出码
2. `launch_kind=prompt` 是一次性启动，完成后退出是预期行为
3. supervisor 将 "进程不存在" 与 "进程异常终止" 混为一谈

### 4.2 但仍然需要解决的问题

1. supervisor 是否应该区分 "进程正常退出 (rc=0)" 和 "进程异常退出 (rc!=0)"？
2. 如果 `launch_kind=prompt` 的一次性任务完成后退出是预期的，supervisor 为什么要报告 crash？
3. `set_e_exit_cmd` 注释来自哪里？是 ACP 适配器的退出溯源还是监控框架的？
4. 对于 `launch_kind=prompt` 的场景，是否需要单独的 "completed" 生命周期状态，而不是统一归入 crash？

## 5. 决策

### 5.1 问题边界

核心问题：**supervisor 未区分进程正常退出 (rc=0) 和异常崩溃 (rc!=0)**，导致正常完成的结果被统一标记为 crash，可能触发不必要的恢复/重启路径。

### 5.2 影响范围

- auto-loop 的进程生命周期管理
- restart storm 触发判据（rc=0 退出不应计入重启风暴）
- supervisor 日志噪声（正常完成 vs 真实 crash 难以区分）

### 5.3 下一跳

1. 创建 candidate 进入 milestone，标记为 `needs_research`
2. 补充证据：查阅 ACP adapter 的退出溯源代码，确认 `set_e_exit_cmd` 的实际含义
3. 确定 supervisor crash 分类的修复范围（仅 ACP adapter 还是全局）
4. 若确认是全局误分类，产出入 `I-*` issue 进入 B2_IBM

### 5.4 排除项

- 不是 cc-ds-flash-auto 特有的问题（与具体 AI 工具无关）
- 不是 chat-inbox 特有的问题（与来源无关）
- 不是需要修改 raw issue 格式的问题
