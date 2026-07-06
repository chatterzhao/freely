# PRD: handoff.py evidence_paths REQUIRED_FIELDS 补齐

## 背景

`raw-20260519T004246Z46Z` (GitHub #581) 报告了 agent 文档 4 个致命问题。经 Brainstorm 验证（docs/B1-docs/raw-20260519T004246Z46Z/brainstorms.md），#2-#4 已在 `5b19bc25` 中修复，仅 #1（evidence_paths 必填/可选不一致）仍需修复。

**缺口**: handoff.py:30 REQUIRED_FIELDS['worker_done'] = ['completion_summary']，缺少 evidence_paths。runtime 的 validate_worker_exit_contract_for_project 要求 evidence_paths 为必填，导致 handoff.py 层不对缺失 evidence_paths 做校验，问题延迟到 runtime 才暴露。

## 方案

在 handoff.py REQUIRED_FIELDS['worker_done'] 增加 'evidence_paths'：

```python
'worker_done': ['completion_summary', 'evidence_paths'],
```

validate_handoff_json 函数已具备通用必填字段检测逻辑（第 494-509 行），遍历 REQUIRED_FIELDS.get(exit_kind, []) 并检查字段值是否为空。增加 REQUIRED_FIELDS 条目后，该函数自动对缺失 evidence_paths 的 worker_done JSON 返回 `(False, errors)`。

## 影响范围

### 文件变更

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `docs/system/workspace/scripts/runtime/handoff.py:30` | 修改 | REQUIRED_FIELDS['worker_done'] 增加 'evidence_paths' |

### 无需变更

- worker-agent.md — evidence_paths 表格已标注"必填"，互斥约束已存在 ✓
- manager-agent.md — handoff.py 调用路径已是完整路径 ✓
- DB schema — evidence_paths 列已存在 ✓

## 兼容性

- 不影响其他 exit_kind（delegate_workers / resume_manager / stop_ai / worker_blocked / worker_handoff_needed）的字段验证
- 不影响已存在的兼容路径（missing reason → fallback to completion_summary, missing next_action → 'see reason'）
- 不影响已有 DB 记录

## Eval Plan

1. 单元测试验证缺失 evidence_paths 的 worker_done 被拒绝
2. 单元测试验证带 evidence_paths 的 worker_done 通过
3. 单元测试验证其他 exit_kind 的必填字段不受影响
