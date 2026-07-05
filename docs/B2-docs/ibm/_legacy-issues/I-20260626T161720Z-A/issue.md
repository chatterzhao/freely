- issue_id: I-20260626T161720Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260626T161720Z-A
- source_raw: raw-20260626T161720Z20Z
- source_candidate: docs/B1-docs/raw-20260626T161720Z20Z/candidates.md#C-20260626T161720Z-A
- verification_artifact_dir: docs/B2-docs/kill-ai-tool-fallback/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260626T161720Z-A/issue.md
- title: 废弃 AI_TOOL，agent-table 唯一真相源
- pre_tests_path: docs/B2-docs/kill-ai-tool-fallback/verification/pre-tests.md

# I-20260626T161720Z-A: 废弃 AI_TOOL，agent-table 唯一真相源

- source_raw: raw-20260626T161720Z20Z
- source_candidate: docs/B1-docs/raw-20260626T161720Z20Z/candidates.md#C-20260626T161720Z-A
- pre_tests_path: docs/B2-docs/kill-ai-tool-fallback/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/kill-ai-tool-fallback/code-reviews

## 实现

- load_config: agent-table 解析 AGENT_AI_TOOL → 派生 AI_TOOL
- _ensure_acp_bridge_running: 移除 4 处 AI_TOOL 降级
- sync_tooling: 不写 AGENT_AI_TOOL，只写 agent-id.env
- bin/freely-review, bin/pr-review-guarded: AI_TOOL → AGENT_AI_TOOL
- _filtered_env[@]: bash 3.2 保护
- config.toml: 移除 AI_TOOL
- templates/agent-table.toml.example + freely init 生成
- tools.md: 更新文档
