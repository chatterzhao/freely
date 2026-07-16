---
b1_id: B1-20260716T050053Z
phase_state: completed
source_raw: raw-20260716T050053Z
source_url: https://github.com/chatterzhao/freely/issues/3936
produced_candidate: C-20260716T050053Z-A
created_at: 2026-07-16
---

# B1_IBM: Daemon inline Python NameError + session lifecycle gaps

## Input
- 来源: raw-20260716T050053Z (GitHub #3936)
- 性质: fix — 修复 daemon 运行时错误和生命周期追踪缺陷

## Problem

### Bug A (已定位到精确影响点): 内联 Python NameError

daemon-launch.log 显示每次 Manager cycle 启动时，在 `session anchor persisted early` 和 `launching via acp` 之间出现:

```
Traceback (most recent call last):
  File "<stdin>", line 170, in <module>
NameError: name 're' is not defined
```

此错误出现在 daemon-launch.log 中超过 20 次 (July 14-16)。
但因为 `<stdin>` 行号稳定 (line 170)，可以确定是一个固定大小的内联 Python 脚本。
扫描了 freely、monitor-ai-acp.sh、run-acp-prompt.py、freely-db-cli、acp-bridge.py 等所有相关文件，未在其中找到来源。
下一步：在 daemon 运行时开启 stderr 捕获，定位具体脚本。

**影响**: 每次 AI session 启动前，session anchor 持久化脚本以 NameError 失败。虽然 `2>/dev/null || true` 可能吞掉错误，但部分 session 元数据可能丢失。

### Bug C: ACP bridge session 结束通知不可靠

AI session (Claude via ACP) 正常结束后，ACP bridge 进程继续存活但 idle。
Supervisor 依赖 `ai_cycle_finished` 事件来判断 session 结束，但 bridge 在 session 结束后不主动通知 supervisor。
Supervisor 只能依靠 90 秒 stall timeout 检测 → 误判为 stalled → recovery kill bridge → 重启循环。

**影响**: 正常 AI patrol 完成后，supervisor 总是经过 90s 超时才能继续，浪费等待时间。如果 bridge 重启失败，进入无限重启循环。

### Bug D: 重启循环无退避

`manager_launch_requested decision=none` 每 ~11 秒重试，无指数退避，无最大重试次数限制。

## Brainstorm

### Option A: 只修 NameError
快速修复但忽略 session 生命周期问题。

### Option B: 只修 session 生命周期
改善 session 结束检测但忽略 NameError。

### Option C (推荐): 修 NameError + session 生命周期 + 退避
完整修复三个关联问题。

## Decision: Option C

先定位并修复 NameError，再改善 session 生命周期追踪，最后添加退避。

## Candidate
- candidate_id: C-20260716T050053Z-A
- status: promoted
- milestone: M-20260716T050053Z-A
