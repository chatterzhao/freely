---
local_id: raw-20260717T060903Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260717T060903Z-A
platform_ids:
  gitee:
    issue_id: IK1OJ0
    url: https://gitee.com/zhaoquan/freely/issues/IK1OJ0
    synced_at: ''
primary_platform: gitee
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-17T14:09:32+08:00'
updated_at: '2026-07-17T14:09:32+08:00'
intake_id: ''
author: platform
channel: gitee
session_refs: []
---

\n\n## 缺陷（raw-20260717T041435Z 附带段正式立案）
1. runtime_pid_file_for_role 的 acp_bridge 分支（runtime/freely ~L1803）：printf 未引 glob——多 bridge 时展开多参多行，调用方 clear_stale_runtime_pid_file_if_invalid 对多行路径 cat/rm 静默失败（pid 取空→无事件返回 0），单文件时才碰巧工作
2. clear_stale_runtime_pid_file_if_invalid 的 acp_bridge 广播清理（~L1838-1841）：任一 stale 即删 <hash> 全族 sock/pid——把其他工具活 bridge 的 socket/pid 一并删除，活进程失联成孤儿（与已修复的 raw-20260717T004654Z 泄漏形成叠加面）

## 修复方向
- self-heal 对 acp_bridge 逐文件枚举（每个 -tool.pid 独立判活清理）
- 清理 per-tool 化：仅清 stale 文件同工具的 sock/pid/pid.bin/pid.tool

## 实证
今日多轮实验中 /tmp 同 hash 下并存 claude/opencode/cline 三组文件；glob 展开行为 bash -c 可复现
