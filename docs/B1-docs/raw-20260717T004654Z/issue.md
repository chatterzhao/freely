---
local_id: raw-20260717T004654Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260717T004654Z-A
platform_ids:
  github:
    issue_id: '3948'
    url: https://github.com/chatterzhao/freely/issues/3948
    synced_at: ''
  gitee:
    issue_id: IK1L7U
    url: https://gitee.com/zhaoquan/freely/issues/IK1L7U
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-17T00:47:17Z'
updated_at: '2026-07-17T00:47:17Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 现象
2026-07-16 17:16 重启实验（task_mode=wait）：三工具 bridge 每 ~15s 全量重生且旧进程不死，4 分钟累积 42 个 acp-bridge.py + 28 claude-agent-acp + 28 opencode + 71 cline，>1.2GB RSS，+12 进程/分钟无上限。当日 acp_bridge_started 事件共 252 次。

## 根因
1. _ensure_acp_bridge_running 健康检查失败路径（runtime/freely ~L14244-14250）只删 pid/socket 文件、不调 _stop_acp_bridge 杀旧进程 → 旧 bridge 成不被追踪的孤儿。
2. _acp_bridge_health_check 超时 5s（~L14065）< claude-agent-acp 冷启动 ~8s（代码注释 ~L14365）→ 新 bridge 首查必败 → 再次重生 → 循环。
3. 触发面：主循环 per-cycle 对 manager/worker/reviewer 三 slot 的 base_tool 全量 ensure（~L22540-22557）。task_mode=wait/listen 下主循环空转（10s/轮），每轮触发一次；与 lazy-start 设计（raw-20260708T202424Z, d43c4af01）冲突。

## 修复方向
- 健康检查失败路径先 _stop_acp_bridge（或 kill 旧 pid）再重生
- 健康检查给冷启动宽限（首查延迟或超时>冷启动）
- per-cycle ensure 尊重 lazy-start：非 manager 工具不 eager 重生

## 证据
runtime-events.log 2026-07-17T00:16-00:22 段；对照 00:33 auto 模式（AI cycle 阻塞主循环）bridge 稳定 4 个不累积
