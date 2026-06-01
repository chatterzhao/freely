---
local_id: raw-20260519T033529Z
kind: raw
phase_state: dropped
platform_ids:
  github:
    issue_id: '612'
    url: https://github.com/chatterzhao/freely/issues/612
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-19T03:35:43Z'
updated_at: '2026-06-01T11:48:42Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## raw-20260519T033529Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260519T033529Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-05-19T03:35:29Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260519T033529Z`。实现前请用 `wt-create --raw-key 20260519T033529Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P0
phase_state: proposed
source: feedback
created_at: "2026-05-19T03:35:29Z"
title: "Worker handoff JSON 损坏：ACP stream 混入乱码 + 部分 worker 不写 handoff"

## 根因分析

从 worker cycle log 中发现三个问题：

### 1. JSON 损坏（最致命）
```
AI 输出: "exit_kind": "completed_s_hint":uccess"
         "typeAN，commit": "commit"
         " commitblock 3 ing个变更": false：同步
```
ACP 协议 stream 中 tool_call_update 事件和 AI 回复文本混在一起，导致 JSON 不可解析。`parse_handoff_json_reply` 提取 handoff 块时拿到的是损坏的 JSON。

### 2. 部分 worker 不写 handoff
`stop_reason=end_turn` 但没有 `handoff` JSON 块。Worker 完成任务后直接结束，不输出交接。

### 3. exit_kind: "completed"
handler.py 已有 alias 映射 `completed→worker_done`，但前提是 JSON 能被成功解析。

## 影响
- Worker 完成了工作但 handoff 无法被 runtime 解析
- Handoff 被拒 → worker 被标记 stale_pid
- 历史上 0 个 worker 完成记录

## 修复方向
1. `run-acp-prompt.py`：提取 handoff JSON 前先做 stream 清理，去掉混入的 ACP 事件标记
2. `handoff.py`：增强 JSON 解析容错——尝试修复常见损坏模式
3. `worker-agent.md`：强调"必须输出 handoff 块"，stop_reason=end_turn 但无 handoff 是错误

## 涉及文件
- docs/system/workspace/scripts/runtime/run-acp-prompt.py
- docs/system/workspace/scripts/runtime/handoff.py
- docs/system/workspace/agents/worker-agent.md

## 验证结果（2026-05-18）

所有三个问题点均已通过已合并到 develop 的 fix 分支修复。

### 问题 1：JSON 损坏 ✅ 已修复
**Fix commit**: `61375ec0` — `fix: robust handoff block extraction — strip ACP events, JSON boundary detection`
- `handoff.py::extract_handoff_block()` 现在在提取前先剥离 ACP 事件行（`[ACP ...]`）和 CACHE/TIMING 元数据行
- 容缺失踪的 closing ``` fence
- 通过 `{}` 边界提取 JSON，可容忍尾部垃圾字符

### 问题 2：部分 worker 不写 handoff ✅ 已修复
**Fix commit**: `e0f5b8ee` — `fix: handoff JSON parse failure when stop_reason=end_turn on same line as`
- 发送 `stop_reason` 前增加 `print()` 确保换行
- 正则增加 `[^\n]*` 容错：`r'```handoff\s*\n(.*?)\n```[^\n]*'`
- 根因：`run-acp-prompt.py` 输出 AI 文本无尾部换行，`stop_reason=end_turn` 紧贴 ``` 导致不匹配

### 问题 3：`exit_kind: "completed"` 不被识别 ✅ 已修复
**Fix commit**: `ff0e9441` — `fix: map "completed" to "worker_done" in handoff validation`
- `handoff.py` 新增 `ALIAS_MAP = {'completed': 'worker_done'}`
- 在 `validate_handoff_json` 中防御性映射所有自然语言别名

### 合并的 fix 分支
以下分支均已合并到 develop，无额外 commit：
- `fix/handoff-block-clean`
- `fix/worker-completed-alias`
- `fix/handoff-required-fields-align`
- `fix/worker-reject-reason-handoff`
- `fix/worker-develop-intent-allow`
