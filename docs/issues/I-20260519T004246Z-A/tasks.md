# Tasks: I-20260519T004246Z-A

## T1: 修改 handoff.py REQUIRED_FIELDS

- [ ] 修改 REQUIRED_FIELDS['worker_done']:
  ```python
  # BEFORE
  'worker_done': ['completion_summary'],
  # AFTER
  'worker_done': ['completion_summary', 'evidence_paths'],
  ```

**验证**: `validate_handoff_json` 对 `{'exit_kind': 'worker_done', 'completion_summary': 'done'}` 返回 `(False, [{"field": "evidence_paths", ...}])`

## T2: 新增单元测试 — 缺失 evidence_paths 被拒绝

- [ ] 测试缺失 evidence_paths 的 worker_done 返回 `(False, errors)`，error 包含 `field: "evidence_paths"`
- [ ] 测试带 evidence_paths 的 worker_done 返回 `(True, [])`
- [ ] 测试其他 exit_kind（worker_blocked / worker_handoff_needed / delegate_workers 等）不受影响

## T3: 运行全部 handoff.py 测试

- [ ] `governance-check` 通过
- [ ] 所有 handoff.py 相关测试通过
