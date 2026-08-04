---
b1_id: B1-20260724T024118Z
phase_state: completed
source_raw: raw-20260724T024118Z
source_url: https://github.com/chatterzhao/freely/issues/4071
produced_candidate: C-20260724T024118Z-A
created_at: 2026-08-04T10:10:00Z
---

# B1_IBM: command-wrapper 元数据生命周期边界

## Input

- 来源：`raw-20260724T024118Z`（GitHub #4071）。
- 现象：wrapper 命令（AI CLI 工具边界 wrapper，runtime/freely `project_tool_wrapper_dir`/`tool_boundary_wrapper_relpath`）与 verification 元数据的生命周期无统一契约——owner、phase、freshness、rejection 条件未定义，B1/B2 路由与 RED/GREEN 证据易歧义，可能接受 stale 或 ownerless 结果。

## Discovery

- wrapper 命令由 `docs/system/workspace/scripts/runtime/freely` 的 `project_tool_wrapper_dir`（L1672）与 `tool_boundary_wrapper_relpath`（L5786）管理，各工位 rematerialize `.codex/`/`.claude/` wrapper。
- 元数据（`platform_ids`、`phase_state`、`last_synced_comment_at`、`hash`、`session_refs`）散落在 issue frontmatter，无统一"谁创建、何时过期、何时拒绝"的规则声明。
- I-20260408-1205-A 曾完成 verification handoff 契约，并显式把 wrapper 采纳与 raw-command bypass 推迟到 follow-on（本 issue）。

## Brainstorm

### Option A：仅写契约文档
产出 `docs/system/workspace/command-wrapper-metadata-lifecycle.md` 声明 owner/phase/freshness/rejection；无执行校验，靠人工遵守。风险：文档漂移。

### Option B：契约文档 + 轻量校验测试
在 A 基础上，新增 `test-command-wrapper-metadata-contract.py`：断言契约文档结构完整（五要素齐全）+ 抽查 wrapper 元数据字段引用一致。变更面小、防漂移。采用。

### Option C：改 runtime 强约束
在 runtime/freely 加 wrapper 生命周期强制逻辑。改动面大、风险高（影响所有工位 rematerialize），超出本 issue 边界（raw 已排除 broad runtime supervision changes）。拒绝。

## Decision

采用 Option B：materialize 契约文档（intake 创建 → guarded-wrapper 传播 → issue-bound 持久化 → stale/ownerless 拒绝 → B1/B2 与 RED/GREEN 证据绑定），并附结构校验测试。

## Candidate

- candidate_id: `C-20260724T024118Z-A`
- status: promoted
- milestone: `M-20260724T024118Z-A`
- next_action: B2 物化契约文档与校验测试设计。
