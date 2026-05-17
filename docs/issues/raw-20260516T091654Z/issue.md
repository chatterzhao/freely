---
local_id: raw-20260516T091654Z
kind: raw
phase_state: completed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '362'
    url: https://github.com/chatterzhao/freely/issues/362
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T09:17:07Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-16T09:32:29Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## raw-20260516T091654Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260516T091654Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-16T09:16:54Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260516T091654Z`。实现前请用 `wt-create --raw-key 20260516T091654Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-16T09:16:54Z"
title: "restart_storm_pause 假阳性：PROCESS_CHURN_PEAK=3 低于正常运行进程数，配置热更新缺失"

## 根因分析

`restart_storm_signal_reason_for_window()` 有两个阈值：

```bash
if (( ${process_peak:-0} >= ${PROCESS_CHURN_PEAK:-3} )); then
    printf 'process_churn_peak_threshold\n'
fi
```

`process_peak` 是 30s 窗口内活跃进程数的峰值，`PROCESS_CHURN_PEAK=3`。

**正常运行时进程数：** supervisor(1) + manager_watchdog(1) + interruption_dispatcher(1) + AI(1) + ACP bridge(1) = **≥5 个进程**。

所以每次 AI cycle 结束，`peak >= 3` 必然成立 → 触发 `restart_storm_pause` → 30s 暂停 → watchdog 重启 supervisor → 丢失 worker 委派。

### 为什么 Phase 1（adapter=direct）崩溃后 Phase 2（adapter=acp）仍受影响

- Phase 1：adapter=direct 导致 ACP bridge 起不来 → supervisor 每 8s 崩溃 → 真风暴（restart_count 应该触发才是对的）
- Phase 2：adapter 修好后，restart_count 已过期（窗口=30s），但 `process_peak >= 3` 仍然触发
- 这不是状态残留——是阈值本身就有问题

## 修复

1. **PROCESS_CHURN_PEAK 默认值提到 10**：正常 5 进程 + 安全余量。`RESTART_STORM_COUNT` 负责防崩溃风暴，`PROCESS_CHURN_PEAK` 应该只防真异常（进程数突然激增）
2. **set-tool 应提示重启或自动重启**：改了 AI_TOOL/ADAPTER 等运行时关键配置后，当前没有机制让 daemon 重新加载。`freely set-tool` 应该：
   - 检测 daemon 是否在运行
   - 如运行中：提示 "配置已更新，需执行 freely restart 生效"
   - 或支持 `--restart` 标志自动重启 daemon

## 范围

- `freely` 脚本：`PROCESS_CHURN_PEAK` 默认值 3 → 10
- `bin/freely set-tool`：加 daemon 检测 + 重启提示
