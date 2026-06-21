---
local_id: raw-20260519T004246Z
kind: raw
priority: P0
phase_state: absorbed
source: feedback
created_at: '2026-05-19T00:42:46Z'
title: agent 文档致命修复：handoff 必填/互斥字段对齐 + 路径修正
platform_ids:
  github:
    issue_id: '581'
    url: https://github.com/chatterzhao/freely/issues/581
    synced_at: '2026-05-19T00:42:53Z'
updated_at: '2026-06-21T18:27:07Z'
primary_platform: github
platform_state: closed
---

## 发现

两份 subagent 审查报告了 4 个致命问题：

### 1. evidence_paths 必填/可选不一致 🔴
- `worker-agent.md` 第 126 行：`evidence_paths` 标注为"否"（可选）
- `freely` runtime `validate_worker_exit_contract_for_project`：`evidence_paths_csv` 为必填
- `handoff.py` REQUIRED_FIELDS：只要求 `completion_summary`
- 结果：worker 输出不带 evidence_paths 的 worker_done → 被 runtime 拒绝

### 2. Worker 互斥字段约束缺失 🔴
- `freely` 第 13732-13744 行：`worker_blocked` 不能带 `completion_summary`/`evidence_paths`；`worker_done` 不能带 `next_action`
- `worker-agent.md` 交接表格完全没提互斥约束
- 结果：worker 输出 "带 completion_summary 的 worker_blocked" → handoff.py 放行 → runtime 拒绝

### 3. handoff.py 路径错误 🔴
- `manager-agent.md` 第 209-211 行：`python3 handoff.py list ...`
- `worker-agent.md` 第 95 行：`python3 handoff.py list ...`
- 实际路径：`docs/system/workspace/scripts/runtime/handoff.py`
- 结果：AI 调用裸名 → 命令失败

### 4. $HP $DB 死引用 🔴
- `manager-agent.md` 第 324-326 行：`python3 $HP list --db $DB ...`
- `$HP` 和 `$DB` 从未定义
- 结果：空字符串替换 → 命令全是错的

## 涉及文件

- `docs/system/workspace/agents/worker-agent.md` — evidence_paths + 互斥字段
- `docs/system/workspace/agents/manager-agent.md` — 路径 + $HP/$DB
- `docs/system/workspace/scripts/runtime/handoff.py` — REQUIRED_FIELDS 增 evidence_paths
