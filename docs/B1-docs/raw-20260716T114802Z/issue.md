---
local_id: raw-20260716T114802Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260716T114802Z-A
platform_ids:
  github:
    issue_id: '3944'
    url: https://github.com/chatterzhao/freely/issues/3944
    synced_at: ''
  gitee:
    issue_id: IK1K39
    url: https://gitee.com/zhaoquan/freely/issues/IK1K39
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-16T11:48:25Z'
updated_at: '2026-07-16T11:48:25Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 描述修正（2026-07-16 排查）
原描述称 PR #3943 的 debug log 检查 return 0 反向。经 git log -L 核实：453ed81a7 合入 develop 的代码即为正确的 return 1（manager_ai_stalled_without_runtime_progress，runtime/freely ~L14595-14606），该前提不成立。但**误杀确实在修复合入后仍复发**：

## 实际现象
2026-07-16 13:10:16Z manager AI 启动（ai_launch_begin）→ 13:11:47Z（91 秒后）runtime_stalled_ai_recovery_triggered reason=manager_ai_stalled_without_runtime_progress → recovery 连锁杀死 bridge session → AI rc=1。crash log stdout 证明 AI 当时正持续执行 tool call（活跃）。

## 修正后的根因假设（B1 需验证）
1. ACP prompt 等待期间 cycle.debug.log 不持续 flush（缓冲/仅落盘于阶段边界），mtime 检查无法证明活跃 AI 的存活 → debug mtime 检查失效
2. 兜底 _ai_shows_liveness 链在该场景同样未判 alive（Signal 1 同为 debug mtime；bridge 存活信号为何未生效需查）
3. direct 模式 _ai_shows_liveness_pid_signals（~L14000-14014）仅 debug mtime + kill -0，信号更薄弱

## 修复方向
- 让 liveness 有真实数据源：ACP 侧持续写活跃信号（tool_call 事件即 touch），或 stall 判定改问 bridge session 状态而非文件 mtime
- 90s 阈值对「首轮 prompt 长思考」过短的问题一并评估

## 关联
前史：raw-20260716T113637Z（453ed81a7）、raw-20260531T212016Z（684787bc5，曾移除 debug mtime 误报又加回）。本 issue 原工位 fix/raw-20260716T114802Z-return-value-fix 仍在，直接在其上走 B1→B2→dev→test。