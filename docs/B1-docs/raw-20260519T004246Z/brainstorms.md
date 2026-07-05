# Brainstorm: agent 文档致命修复 — handoff 字段对齐 + 路径修正

## Discovery

Raw issue `raw-20260519T004246Z` (GitHub #581) 报告了 agent 文档中 4 个致命问题：

### 1. evidence_paths 必填/可选不一致

- `handoff.py` REQUIRED_FIELDS (`handoff.py:30`): `'worker_done': ['completion_summary']` — **缺少 `evidence_paths`**
- `worker-agent.md:139`: evidence_paths 表格标注为"是"（必填）— 文档已正确
- runtime `validate_worker_exit_contract_for_project`: evidence_paths_csv 为必填
- 缺口：handoff.py 的 REQUIRED_FIELDS 没把 evidence_paths 列为 worker_done 必填，导致 handoff.py 层不做验证

### 2. Worker 互斥字段约束

- `worker-agent.md:119-121`: 已写明硬性 JSON 约束：`worker_done` 不可带 `next_action`，`worker_blocked`/`worker_handoff_needed` 不可带 `completion_summary`/`evidence_paths`
- `worker-agent.md:140`: 表格"互斥"行已存在
- **当前文档已修复** — 原始 issue 报告时的版本缺了这部分

### 3. handoff.py 路径错误

- `manager-agent.md:211-213`: 已使用完整路径 `python3 docs/system/workspace/scripts/runtime/handoff.py`
- `worker-agent.md:101`: 已使用完整路径 `python3 docs/system/workspace/scripts/runtime/handoff.py`
- **当前文档已修复**

### 4. $HP $DB 死引用

- manager-agent.md 和 worker-agent.md 中 **不存在** $HP/$DB 引用
- **当前文档已修复**

## Research Verdict

4 个问题中，**#1 仍未修复**（handoff.py REQUIRED_FIELDS），**#2-#4 在当前版本中已修复**。

这合理，因为 `5b19bc25` (hygiene checkpoint) 可能在 issue 创建后部分修复了文档路径和互斥约束，但没有修补 handoff.py 的验证逻辑。

## 剩余修复范围

### 必须修

1. **`handoff.py:30` — REQUIRED_FIELDS 增加 evidence_paths**
   ```python
   'worker_done': ['completion_summary', 'evidence_paths'],
   ```

### 验证（已修复，但确认）

2. **worker-agent.md 表格列 evidence_paths 为必填** — 第 139 行已标"是" ✓
3. **worker-agent.md 互斥约束已写清** — 第 119-121, 140 行 ✓
4. **manager-agent.md handoff.py 调用已使用完整路径** — ✓
5. **worker-agent.md handoff.py 调用已使用完整路径** — ✓
6. **$HP $DB 已不存在** — ✓

### decision: 验收即推进

handoff.py 一行改动 + 对应测试更新即可关闭此 issue。不需要额外 pre-brainstorm 循环。
