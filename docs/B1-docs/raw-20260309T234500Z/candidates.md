# Candidates - 20260309-2345--governance-check-naming-alignment

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260309T234500Z-A: legacy issue
- title: Governance Check Naming and Runtime Alignment
- problem: `bmad-check` 仍作为治理检查命令名存在，与当前 `pre-brainstorm -> IBM -> dev-loop` 流程命名和脚本真实职责不一致，也会继续把历史 BMAD 概念投射为现行方法论。
- why_now: 该命令是 README、AGENTS、脚本说明和测试的入口名；若不尽快收敛，后续 hook、skill 和工作区门禁仍会沿用错误术语扩散。
- acceptance_hint: 将命令和脚本真源统一重命名为 `governance-check`；同步更新入口文案、脚本输出、测试引用；明确 `bmad` 仅保留为历史记录，不再作为现行治理术语。
- priority: P0
- status: absorbed
- adoption_type: supporting_evidence
- decision_reason: `governance-check` 命名、candidate v2 门禁与脚本回归已由 `I-20260320T050000Z` 吸收；本候选只保留为 supporting provenance。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260309T234500Z-A/issue.md
- milestone: M-20260309T234500Z-A
- session_refs:
  - tool: codex
  - session_id: unavailable
  - jsonl_path: unavailable://codex-cli-does-not-expose-jsonl-path-in-workspace
  - role: author
- sequencing_rank: 1

### C-20260309T234500Z-A: legacy issue
- title: Legacy Governance Fixture Cleanup
- problem: 测试夹具与部分当前事实表述仍引用旧 `docs/brainstorms`、`docs/planning`、`docs/validation`、`docs/continuity` 结构，会持续把过时工作流当成有效基线。
- why_now: 命名收敛若不同时处理测试基线，后续实现会继续在错误目录模型上回归，削弱本次治理修复的效果。
- acceptance_hint: 将直接依赖旧目录结构的测试迁移到当前活跃文档集合；把仍在陈述当前机制的旧事实表述改写为新结构与新命名。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: 旧目录模型夹具清理已被当前活跃目录模型与 `governance-check` 真源逐步取代，剩余历史引用只保留 provenance，不再作为 active candidate。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - AGENTS.md
  - docs/system/workspace/scripts/README.md
- session_refs:
  - tool: codex
  - session_id: unavailable
  - jsonl_path: unavailable://codex-cli-does-not-expose-jsonl-path-in-workspace
  - role: author
- sequencing_rank: 2
- depends_on:
  - C-20260309T234500Z-A
