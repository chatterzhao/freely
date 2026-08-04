# Command-Wrapper Metadata Lifecycle

> 本契约定义 wrapper 命令（AI CLI 工具边界 wrapper，见 `docs/system/workspace/scripts/runtime/freely` 的 `project_tool_wrapper_dir` / `tool_boundary_wrapper_relpath`）与 verification 元数据的生命周期边界，作为 B1/B2 路由与 RED/GREEN 证据的唯一声明式依据。

## Owner

- 元数据 owner 是当前 issue 链：raw issue（`raw-{key}`）→ candidate（`C-{key}-A`）→ milestone（`M-{key}-A`）→ I-* issue（`I-{key}-A`）。
- wrapper 传播路径的 owner 是创建工位的 wt-create；工位内 rematerialize 的 `.codex/` / `.claude/` wrapper 归属该工位的 raw key。
- 无 owner（缺失 raw key 或游离工位）的元数据不得进入 B1/B2 路由与证据判定。

## Phase

- 元数据 phase 与 issue 生命周期绑定：`proposed` → `absorbed`（raw）与 `in_b2_ibm` → `done_b2_ibm` → `in_dev` → `completed`（I-*）。
- wrapper 产生的验证结果只允许写入与当前 phase 匹配的证据面（RED 证据在 RED 阶段、GREEN 证据在 dev/test 阶段）。
- phase 流转由 `freely-doc-B1_IBM-execution` / `freely-doc-B2_IBM-execution` / `freely-test-RED-execution` / `freely-dev-loop-execution` / `freely-test-execution` 驱动。

## Freshness

- 引用 wrapper 元数据前必须校验 `last_synced_comment_at`、`hash` 与 `updated_at`。
- 平台副本与本地不一致（reconciliation gate 的 `content_diverged` / `missing` / `ambiguous`）时，视为 stale，禁止作为证据。
- 证据必须来自当前工位 HEAD（test-gate.env `LAST_TESTED_COMMIT` 与工位 HEAD 一致）。

## Rejection

- stale（平台/本地不一致）或 ownerless（无 raw key / 无 canonical issue 绑定）的元数据一律拒绝进入路由与证据判定。
- `platform_ids`、`phase_state`、`last_synced_comment_at`、`hash`、`session_refs` 任一缺失或与真相源冲突时拒绝。
- 拒绝路径必须是 fail-closed：报告明确错误，不降级为空清单或默认值。

## Evidence

- B1/B2 证据：brainstorms、candidates、milestone 条目、I-* issue 文档与 IDN。
- RED/GREEN 证据：pre-tests 的 `red-green-status`、`actual_RED_output`、`actual_output`、`evidence_file`，以及 test-gate.env。
- 所有证据必须可追溯到 owner issue（`issue_id` / `issue_path`），并在同一 diff 或同一条 verification 链内。
