- issue_id: I-20260625T153111Z-A
- kind: feat
- phase_state: completed
- milestone: M-20260625T153111Z-A
- source_candidate: docs/B1-docs/raw-20260625T153111Z11Z/candidates.md#C-20260625T153111Z-A
- verification_artifact_dir: docs/B2-docs/agent-table/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260625T153111Z-A/issue.md
- source_raw: raw-20260625T153111Z11Z
- pre_tests_path: docs/B2-docs/agent-table/verification/pre-tests.md
- title: agent-table.toml 多 agent 分身注册

# I-20260625T153111Z-A: agent-table.toml 多 agent 分身注册

- source_candidate: docs/B1-docs/raw-20260625T153111Z11Z/candidates.md#C-20260625T153111Z-A
- verification_artifact_dir: docs/B2-docs/agent-table/code-reviews
- pre_tests_path: docs/B2-docs/agent-table/verification/pre-tests.md

## 实现

### 1. agent-table.toml 格式
- .freely/agent-table.toml
- [[agents]]: 单例声明（manager_id + manager_slot + worktree）
- [[agent_pools]]: 池声明（count=N → worker_01..N ↔ reviewer_01..N）

### 2. Python 解析器 bin/agent-table-query
- 查询: --list role=worker, --get worker_01, --get-slot worker_01, --get-reviewer worker_01
- 空闲检测: --next-available worker

### 3. wt-create 集成
- 读 agent-table 取空闲 worker_id
- 将 worker_slot 写入工位 .freely/config.toml 的 AI_TOOL

### 4. TDD review skill
- docs/system/workspace/skills/freely-tdd-review/SKILL.md
- 四问: RED→GREEN→ADEQUACY→REFACTOR
