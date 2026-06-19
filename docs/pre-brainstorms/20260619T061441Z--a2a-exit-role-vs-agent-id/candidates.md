# Candidates: a2a-exit --agent-id vs --role 参数不匹配

## Candidate 1: 修正 prompt 模板 + handler 向后兼容 + 修复 config_bool_enabled

**Decision: promote** (选择方案 B)

### Acceptance Criteria
1. `manager-agent.md` 中所有 `--agent-id worker` → `--role worker`（4 处）
2. `acp-a2a-architecture.md` 中所有 `--agent-id=worker` → `--role=worker`（2 处）
3. `a2a_task.py` a2a-exit handler 添加 `--agent-id` → `--role` fallback 映射
4. `freely` 第 3975 行 `config_bool_enabledconfig_bool_enabled()` → `config_bool_enabled()`
5. 三个 loop 文档更新：接口约定、trace 检查点、已知陷阱
6. 不影响现有 `list --role worker --status submitted` 查询逻辑

### Promotion Gate
- [x] 修复方案已在 fix worktree 中实现并提交（2 commits）
- [x] config_bool_enabled 函数名修复验证通过
- [x] a2a-exit --role worker 和 --agent-id worker 均正确创建 task
- [ ] pr-create-guarded 通过
- [ ] pr-review-guarded 通过
- [ ] pr-merge-guarded 通过

### Open Questions
- 无。根因明确，修复范围清晰。

### Acceptance Reviews
- 待 pr-review-guarded 6 维 review

---

## Candidate 2: 仅修改 handler，不改 prompt 模板 (方案 C)

**Decision: drop** 

理由：与 Runtime 内部 `--role` 约定不一致，且 `--agent-id` 在 a2a-exit handler 中未被定义为已知参数，需要额外添加。方案 B 更简洁。
