# Candidate: Agent docs fix — evidence_paths REQUIRED_FIELDS

## C-20260519T004246Z-A

- **status**: `needs_research`
- **premerge**: allowed
- **priority**: P0
- **title**: handoff.py 增加 evidence_paths 为 worker_done 必填字段，对齐 agent 文档与 runtime 验证
- **source_raw**: `raw-20260519T004246Z` (GitHub #581)

### acceptance_criteria

1. handoff.py REQUIRED_FIELDS (`worker_done`) 增加 `evidence_paths`
2. handoff.py 已有 validate 函数（`validate_handoff_json`）准确拒绝缺少 evidence_paths 的 worker_done JSON
3. 不影响已存在的兼容路径（`validate_handoff_json` 对缺失 evidence_paths 的正确处理：若 AI 产出不含 evidence_paths 的 worker_done，handoff.py 层拒绝，runtime 不会放行到 consume）
4. 不影响其他 exit_kind 的字段验证
5. worker-agent.md 和 manager-agent.md 中其他问题已验证当前版本已修复（#2-#4）

### promotion_gate

- [ ] handoff.py 单元测试覆盖缺失 evidence_paths 的 worker_done
- [ ] 所有 handoff.py 相关测试通过
- [ ] governance-check 通过

### open_questions

- evidence_paths 在 handoff.py 做硬校验还是软 warning？建议硬拒绝（与 runtime 行为一致）
- 是否需要清理 DB 中已有的缺失 evidence_paths 的 worker_done 记录？

### acceptance_reviews

- None yet
