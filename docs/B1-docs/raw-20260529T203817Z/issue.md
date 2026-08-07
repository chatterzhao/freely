---
local_id: raw-20260529T203817Z17Z
kind: raw
- phase_state: dropped
platform_ids:
  github:
    issue_id: '2315'
    url: https://github.com/chatterzhao/freely/issues/2315
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-29T20:38:31Z'
updated_at: '2026-05-29T20:38:31Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

monitor-ai-acp.sh 的 _detect_acp_failure() 与 freely 的 _acp_bridge_has_fatal_error() 使用**不一致**的 regex 模式集。Codex bridge 崩溃时的实际错误（Transport channel closed, stream disconnected, worker quit with fatal, server stdout closed）在 _acp_bridge_has_fatal_error 中有定义，但 _detect_acp_failure 中没有。

## 故障链

1. Codex bridge 因网络问题崩溃
2. monitor-ai-acp.sh 的 _detect_acp_failure 无法匹配实际错误日志
3. run-acp-prompt.py 在 bridge socket 关闭后可能挂死
4. supervisor 被阻塞等 monitor 返回
5. ensure-manager 无法重启（孤儿 monitor 进程阻挡）
6. 切槽逻辑从未触发

## 修复方案

### 1. monitor-ai-acp.sh: 统一 _detect_acp_failure 的错误模式
- 将 _acp_bridge_has_fatal_error 的模式同步到 _detect_acp_failure 中
- 保持两套检测逻辑一致

### 2. monitor-ai-acp.sh: 添加 child process 看门狗超时
- 监控 log file mtime，如果 child 还活着但 N 秒无输出，视为卡死
- 超时后写 marker 文件并 kill child

### 3. freely: ensure-manager 处理僵尸进程
- 在 manager_launch_requested 阻塞时，清理孤儿 monitor-ai-acp.sh 进程
- 允许强制重启被僵尸进程阻挡的 supervisor

## 证据

- acp-bridge.log: Transport channel closed / stream disconnected before completion / server stdout closed / worker quit with fatal
- monitor-ai-acp.sh PID 83908: 孤儿进程，bridge 崩溃后持续运行 18+ 分钟
- lifecycle-trace: supervisor 68639 卡在 L040，从不推进到 L041/L042
- ensure-manager: manager_launch_requested ok=0 持续循环
