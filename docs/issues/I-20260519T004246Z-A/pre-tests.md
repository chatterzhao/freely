# Pre-tests: I-20260519T004246Z-A

## 测试场景

### TC1: 缺失 evidence_paths 的 worker_done 被拒绝

**输入**:
```json
{"exit_kind": "worker_done", "completion_summary": "task completed"}
```

**预期**: `validate_handoff_json` 返回 `(False, [{"field": "evidence_paths", "error": "required for worker_done, got ''"}])`

### TC2: 带 evidence_paths 的 worker_done 通过

**输入**:
```json
{"exit_kind": "worker_done", "completion_summary": "task completed", "evidence_paths": "/path/to/evidence.md"}
```

**预期**: `validate_handoff_json` 返回 `(True, [])`

### TC3: 带多条 evidence_paths CSV 的 worker_done 通过

**输入**:
```json
{"exit_kind": "worker_done", "completion_summary": "task completed", "evidence_paths": "/path/a.md\n/path/b.md"}
```

**预期**: `validate_handoff_json` 返回 `(True, [])`

### TC4: 其他 exit_kind 不受影响

**输入**:
```json
{"exit_kind": "worker_blocked", "reason": "blocked", "next_action": "check"}
```

**预期**: `validate_handoff_json` 返回 `(True, [])`，不因缺少 evidence_paths 而拒绝

### TC5: worker_done 同时缺失 completion_summary 和 evidence_paths

**输入**:
```json
{"exit_kind": "worker_done"}
```

**预期**: `validate_handoff_json` 返回 `(False, errors)`，errors 包含 completion_summary 和 evidence_paths 两条

## 环境

- handoff.py 的 validate_handoff_json 函数单元测试
- 无需 DB、无需网络
